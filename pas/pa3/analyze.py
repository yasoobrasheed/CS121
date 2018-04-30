# CS121: Analyzing Election Tweets
# Part 2: Tasks 1-7
# By: Yasoob Rasheed

import argparse
import emoji
import json
import string
import sys
import unicodedata
from util import sort_count_pairs, grab_year_month, pretty_print_by_month, get_json_from_file
from basic_algorithms import find_top_k, find_min_count, find_frequent

##################### DO NOT MODIFY THIS CODE ##################### 

# Find all characters that are classifed as punctuation in Unicode
# (except #, @, &) and combine them into a single string.
def keep_chr(c):
    return (unicodedata.category(c).startswith('P') and \
                (c != "#" and c != "@" and c != "&"))
PUNCTUATION = " ".join([chr(i) for i in range(sys.maxunicode) if keep_chr(chr(i))])

# When processing tweets, ignore words, symbols, and emoji in this set.
WORDS = ["a", "an", "the", "this", "that", "of", "for", "or", 
         "and", "on", "to", "be", "if", "we", "you", "in", "is", 
         "at", "it", "rt", "mt", "with"]

SYMBOLS = [chr(i) for i in range(sys.maxunicode) if 
           unicodedata.category(chr(i)) in ("Sm", "Sc", "Sk", "So")] + ["\n"]

EMOJI = list(emoji.UNICODE_EMOJI.keys())

STOP_WORDS = set(WORDS + SYMBOLS + EMOJI)

# When processing tweets, ignore words that start with a prefix that
# appears in this tuple.
STOP_PREFIXES  = ("@", "#", "http", "&amp")

#####################  MODIFY THIS CODE ##################### 


def make_entity_array(tweets, entity_key):
    '''
    Helper method to reduce code-repetition, creates the array of
    specific entities like hashtags or screen_names

    Inputs:
        tweets: a list of tweets
        entity_key: a pair ("hashtags", "text"), 
          ("user_mentions", "screen_name"), etc

    Variables:
		entity_array = holds all the hastags or screen_names

    Returns: list of entities
    '''
    entity_array = []
    for i in range(0, len(tweets)): 
        entities = tweets[i]['entities'][entity_key[0]]
        for entity in entities:
            entity_array.append(entity[entity_key[1]].lower())
    return entity_array


# Task 1
def find_top_k_entities(tweets, entity_key, k):
    '''
    Find the K most frequently occuring entitites

    Inputs:
        tweets: a list of tweets
        entity_key: a pair ("hashtags", "text"), 
          ("user_mentions", "screen_name"), etc
        k: integer

    Variables:
		entity_array = holds all the hastags or screen_names

    Returns: list of entity, count pairs
    '''

    entity_array = make_entity_array(tweets, entity_key)
    return find_top_k(entity_array, k)


# Task 2
def find_min_count_entities(tweets, entity_key, min_count):
    '''
    Find the entitites that occur at least min_count times.

    Inputs:
        tweets: a list of tweets
        entity_key: a pair ("hashtags", "text"), 
          ("user_mentions", "screen_name"), etc
        min_count: integer 

    Variables:
		entity_array = holds all the hastags or screen_names

    Returns: list of entity, count pairs
    '''
    
    entity_array = make_entity_array(tweets, entity_key)
    return find_min_count(entity_array, min_count)


# Task 3
def find_frequent_entities(tweets, entity_key, k):
    '''
    Find entities where the number of times the specific entity occurs
    is at least fraction * the number of entities in across the tweets.

    Input: 
        tweets: a list of tweets
        entity_key: a pair ("hashtags", "text"), 
          ("user_mentions", "screen_name"), etc
        k: integer

    Variables:
		entity_array = holds all the hastags or screen_names

    Returns: list of entity, count pairs
    '''

    entity_array = make_entity_array(tweets, entity_key)
    return find_frequent(entity_array, k)


def subtract_arrays(array_1, array_2):
    '''
    Helper function for pre_process, subtracts array_2 from array_1

    Input: 
        array_1: array we want to subtract from
        array_2: array we want to subtract from array_1

    Variables:
		new_array: holder array for the subtracted array_1

    Returns: array
    '''

    new_array = []
    for word in array_1:
       if word not in array_2:
           new_array.append(word)
    return new_array


def pre_process(tweet):
    '''
    Remove punctuation, stop_prefixes, and stop_words from each
    word in the tweet

    Input: 
        tweet: one singular tweet (dictionary) from tweets used as a parameter in 
        find_top_k_ngrams, find_min_count_ngrams, and find_frequent_ngrams
        functions

    Variables:
		delete_list: list of strings we want to subtract from the word_array list
        word_array: list of words in a tweet lowercased and split

    Returns: list of strings in tweet "simplified"
    '''

    delete_list = []
    # VERY IMPORTANT: Without removing empty strings, code does not run properly
    delete_list.append("")
    # LOWERCASE AND SPLIT
    word_array = tweet['text'].lower().split()
    for i in range(0, len(word_array)):
        # STRIP PUNCTUATION
        word_array[i] = word_array[i].strip(PUNCTUATION)
        # DELETE PREFIX WORDS
        for prefix in STOP_PREFIXES:
            if word_array[i].startswith(prefix) and word_array[i] not in delete_list:
                delete_list.append(word_array[i])
		# DELETE SYMBOLS, EMOJIS, SPECIAL WORDS
        for stop_word in STOP_WORDS:
            if word_array[i] == stop_word and word_array[i] not in delete_list:
                delete_list.append(word_array[i]) 
        
    return subtract_arrays(word_array, delete_list)
   

def make_n_grams(tweet, n):
    '''
    Create an n-length tuple with combinations of words in a tweet. Will do this
    by turning a list into a tuple

    Input: 
        tweet: one singular tweet (dictionary) from tweets used as a parameter in 
        find_top_k_ngrams, find_min_count_ngrams, and find_frequent_ngrams
        functions
        n: number of elements in the tuple

    Variables:
		tuple_array: use preprocess to create a list of the words in the tweet
        n_gram_array: actual array of tuples

    Returns: list of strings in tweet "simplified"
    '''

    tuple_array = pre_process(tweet)
    n_gram_array = []
    for i in range(0, len(tuple_array) - (n - 1)):
        conversion_array = []
        for j in range(0, n):
            conversion_array.append(tuple_array[i + j])
        n_gram_array.append(tuple(conversion_array))
    return n_gram_array


def make_big_ngram_array(tweets, n):
    '''
    Helper method to create a list of all the ngrams in tweets
    
    Inputs:
        tweets: a list of tweets
        n: integer

    Variables:
        big_ngram_array: list of tuples called ngrams

    Returns: list of ngrams
    '''

    big_ngram_array = []
    for i in range(0, len(tweets)):
        big_ngram_array += make_n_grams(tweets[i], n)
    return big_ngram_array


# Task 4
def find_top_k_ngrams(tweets, n, k):
    '''
    Find k most frequently occurring n-grams
    
    Inputs:
        tweets: a list of tweets
        n: integer
        k: integer

    Variables:
        big_ngram_array: list of tuples called ngrams

    Returns: list of ngram/value pairs
    '''
    
    big_ngram_array = make_big_ngram_array(tweets, n)
    return find_top_k(big_ngram_array, k)


# Task 5
def find_min_count_ngrams(tweets, n, min_count):
    '''
    Find n-grams that occur at least min_count times.
    
    Inputs:
        tweets: a list of tweets
        n: integer
        min_count: integer

    Variables:
        big_ngram_array: list of tuples called ngrams

    Returns: list of ngram/value pairs
    '''

    big_ngram_array = make_big_ngram_array(tweets, n)
    return find_min_count(big_ngram_array, min_count)


# Task 6
def find_frequent_ngrams(tweets, n, k):
    '''
    Find frequently occurring n-grams

    Inputs:
        tweets: a list of tweets
        n: integer
        k: integer

    Variables:
        big_ngram_array: list of tuples called ngrams

    Returns: list of ngram/value pairs
    '''
    
    big_ngram_array = make_big_ngram_array(tweets, n)
    return find_frequent(big_ngram_array, k)


# Task 7

def find_top_k_ngrams_by_month(tweets, n, k):
    '''                                                                                                            
    Find the top k ngrams for each month.

    Inputs:
        tweets: list of tweet dictionaries
        n: integer
        k: integer

    Variables:
        by_month_array: list of tuples in the form:
        ((year,  month), (sorted top-k n-grams for that month with their counts))
        big_ngram_array: list of the tweets on a monthly basis 
        (clears when it reaches the next month)
        the_last_date: tuple holder variable for the last month

    Returns: sorted list of pairs.  Each pair has the form: 
        ((year,  month), (sorted top-k n-grams for that month with their counts))
    '''

    by_month_array = []
    big_ngram_array = []
    the_last_date = None

    for i in range(0, len(tweets)):
        last_tuple = grab_year_month(tweets[i - 1]['created_at'])
        this_tuple = grab_year_month(tweets[i]['created_at'])
        the_last_date = this_tuple

        if len(big_ngram_array) == 0:
            big_ngram_array.append(tweets[i])
        else:
            if this_tuple == last_tuple:
                big_ngram_array.append(tweets[i])
            else:
                find_top_k_by_month = find_top_k_ngrams(big_ngram_array, n, k)
                by_month_array.append((last_tuple, find_top_k_by_month))
                big_ngram_array = []
                big_ngram_array.append(tweets[i])

    if the_last_date != None:
        find_top_k_by_month = find_top_k_ngrams(big_ngram_array, n, k)
        by_month_array.append((the_last_date, find_top_k_by_month))

    return sorted(by_month_array)


def parse_args(args):
    '''                                                                                                                
    Parse the arguments

    Inputs:
        args: list of strings

    Result: parsed argument object.

    '''
    s = 'Analyze presidential candidate tweets .'
    parser = argparse.ArgumentParser(description=s)
    parser.add_argument('-t', '--task', nargs=1, 
                        help="<task number>", 
                        type=int, default=[0])
    parser.add_argument('-k', '--k', nargs=1, 
                        help="value for k", 
                        type=int, default=[1])
    parser.add_argument('-c', '--min_count', nargs=1, 
                        help="min count value", 
                        type=int, default=[1])
    parser.add_argument('-n', '--n', nargs=1, 
                        help="number of words in an n-gram", 
                        type=int, default=[1])
    parser.add_argument('-e', '--entity_key', nargs=1, 
                        help="entity key for task 1", 
                        type=str, default=["hashtags"])
    parser.add_argument('file', nargs=1, 
                        help='name of JSON file with tweets')

    try:
        return parser.parse_args(args[1:])
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)


def go(args):
    '''
    Call the right function(s) for the task(s) and print the result(s).

    Inputs:
        args: list of strings
    '''

    task = args.task[0]
    if task <= 0 or task > 7:
        print("The task number needs to be a value between 1 and 7 inclusive.",
              file=sys.stderr)
        sys.exit(1)

    if task in [1, 2, 3]:
        ek2vk = {"hashtags":"text", 
                 "urls":"url", 
                 "user_mentions":"screen_name"}

        ek = args.entity_key[0]
        if ek not in ek2vk:
            print("Invalid entitity key:", ek)
            sys.exit(1)
        entity_type = (args.entity_key[0], ek2vk.get(ek, ""))

    tweets = get_json_from_file(args.file[0])

    if task == 1:
        print(find_top_k_entities(tweets, entity_type, args.k[0]))
    elif task == 2:
        print(find_min_count_entities(tweets, entity_type, args.min_count[0]))
    elif task == 3:
        print(find_frequent_entities(tweets, entity_type, args.k[0]))
    elif task == 4:
        print(find_top_k_ngrams(tweets, args.n[0], args.k[0]))
    elif task == 5:
        print(find_min_count_ngrams(tweets, args.n[0], args.min_count[0]))
    elif task == 6:
        print(find_frequent_ngrams(tweets, args.n[0], args.k[0]))
    else:
        result = find_top_k_ngrams_by_month(tweets, args.n[0], args.k[0])
        pretty_print_by_month(result)
        

if __name__=="__main__":
    args = parse_args(sys.argv)
    go(args)



