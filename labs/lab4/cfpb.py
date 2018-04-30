import json

cfpb_16 = json.load(open("cfpb16_1000.json"))

# Task 1
def count_complaints_about(complaints, company_name):
    count = 0:
    for complaint in complaints:
        count += complaint[company_name]
    return count


# Task 2
def find_companies(complaints):
    s = set()
    for complaint in complaints:
        if complaint[complaint['Company']] >= 1:
            s.add(complaint['Company'])
    return list(s)


# Task 3
def count_by_state(complaints):
    # Your code goes here
    # replace {} with a suitable return value
    return {}


# Task 4
def state_with_most_complaints(cnt_by_state):
    # Your code goes here
    # replace "" with a suitable return value
    return ""


# Task 5
def count_by_company_by_state(complaints):
    # Your code goes here
    # replace {} with a suitable return value
    return {}
        

# Task 6
def complaints_by_company(complaints):
    # Your code goes here
    # replace {} with a suitable return value
    return {}    
