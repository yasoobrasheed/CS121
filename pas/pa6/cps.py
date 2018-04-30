# CS121: Current Population Survey (CPS) 
#
# Functions for mining CPS data 
#
# Name: Yasoob Rasheed

import pandas as pd
import numpy as np
import csv
import os
import sys
import math
import tabulate

# Constants 
HID = "h_id" 
AGE = "age"
GENDER = "gender" 
RACE = "race" 
ETHNIC = "ethnicity" 
STATUS = "employment_status"
HRWKE = "hours_worked_per_week" 
EARNWKE = "earnings_per_week" 

FULLTIME_MIN_WORKHRS = 35

# CODE_TO_FILENAME: maps a code to the name for the corresponding code
# file
CODE_TO_FILENAME = {"gender_code":"data/gender_code.csv",
                    "employment_status_code": "data/employment_status_code.csv",
                    "ethnicity_code":"data/ethnic_code.csv",
                    "race_code":"data/race_code.csv"}


# VAR_TO_FILENAME: maps a variable-of-interest to the name for the
# corresponding code file
VAR_TO_FILENAME = {GENDER: CODE_TO_FILENAME["gender_code"],
                   STATUS: CODE_TO_FILENAME["employment_status_code"],
                   ETHNIC: CODE_TO_FILENAME["ethnicity_code"],
                   RACE: CODE_TO_FILENAME["race_code"]}


def build_morg_df(morg_filename):
    '''
    Build the dataframe from a given .csv file (morg_filename)

    Inputs:
        morg_filename: string path to the csv file

    Variables:
        morg_df: morg dataframe from morg_filename
        g_df: gender data from gender file
        s_df: status data from status file
        e_df: ethnicity data from ethnicity file
        r_df: race data from race file
    
    Return:
        morg_df with new column labels and column data
    '''

    if not os.path.exists(morg_filename):
        return None

    morg_df = pd.read_csv(morg_filename)

    g_df = pd.read_csv(VAR_TO_FILENAME[GENDER])
    s_df = pd.read_csv(VAR_TO_FILENAME[STATUS])
    e_df = pd.read_csv(VAR_TO_FILENAME[ETHNIC])
    r_df = pd.read_csv(VAR_TO_FILENAME[RACE])

    for key in VAR_TO_FILENAME.keys():
        morg_df[key + "_code"] = morg_df[key + "_code"].fillna(0)

    gs = g_df['gender_string']
    gc = 'gender_code'
    morg_df[gc] = pd.Categorical.from_codes(morg_df[gc] - 1, gs)
    ess = s_df['employment_status_string']
    esc = 'employment_status_code'
    morg_df[esc] = pd.Categorical.from_codes(morg_df[esc] - 1, ess)
    es = e_df['ethnic_string']
    ec = 'ethnicity_code'
    morg_df[ec] = pd.Categorical.from_codes(morg_df[ec], es)
    rs = r_df['race_string']
    rc = 'race_code'
    morg_df[rc] = pd.Categorical.from_codes(morg_df[rc] - 1, rs)

    for key in VAR_TO_FILENAME.keys():
        morg_df.rename(columns={key + "_code":key}, inplace=True)

    return morg_df


def calculate_weekly_earnings_stats_for_fulltime_workers(df, gender, race, ethnicity):
    '''
    Calculate statistics for different subsets of a dataframe.

    Inputs:
        df: morg dataframe
        gender: "Male", "Female", or "All"
        race: specific race from a small set, "All", or "Other",
            where "Other" means not in the specified small set
        ethnicity: "Hispanic", "Non-Hispanic", or "All"

    Variables:
        hours_bool: boolean that defines a full time worker
        gender_bool: boolean that checks if the actual gender = the param gender
        race_bool: boolean that checks if the actual race = the param race
        ethnicity_bool: boolean that checks if the actual ethnicity = the param ethnicity
        filtered_df: new dataframe with the rows that fit the specific criteria

    Returns: (mean, median, min, max) for the rows that match the filter
             (0, 0, 0, 0) if the dataframe is empty
    '''

    hrs = df.hours_worked_per_week
    status = df.employment_status
    hours_bool = ((hrs >= FULLTIME_MIN_WORKHRS) & (status == 'Working'))

    gender_bool = True
    if gender != "All":
        gender_bool = (df.gender == gender)

    race_bool = True
    races = ["WhiteOnly", "BlackOnly", "AmericanIndian/AlaskanNativeOnly",
                 "AsianOnly", "Hawaiian/PacificIslanderOnly"]
    if race != 'All' and race != 'Other':
        race_bool = (df.race == race)
    elif race == 'Other':
        race_bool = (df.race.isin(races))

    ethnic_bool = True
    if ethnicity == 'Non-Hispanic':
        ethnic_bool = (df.ethnicity == 'Non-Hispanic')
    elif ethnicity == 'Hispanic':
        ethnic_bool = (df.ethnicity != 'Non-Hispanic')
        
    filter = hours_bool & gender_bool & race_bool & ethnic_bool

    filtered_df = df[filter]

    if filtered_df.empty:
        return (0, 0, 0, 0)

    mean = filtered_df[EARNWKE].mean()
    median = filtered_df[EARNWKE].median()
    minimum = filtered_df[EARNWKE].min()
    maximum = filtered_df[EARNWKE].max()
    return (mean, median, minimum, maximum)
    

def create_histogram(df, var_of_interest, num_buckets, min_val, max_val):
    '''
    Compute the number of full time workers who fall into each bucket
    for a specified number of buckets and variable of interest.

    Inputs:
        df: morg dataframe
        var_of_interest: one of EARNWKE, AGE, HWKE
        num_buckets: the number of buckets to use.
        min_val: minimal value (lower bound) for the histogram (inclusive)
        max_val: maximum value (lower bound) for the histogram (non-inclusive).
    
    Variables:
        filter: filter for the definition of full time
        lin: linear spacing using min_val, max_val, and num_buckets
        dfcut: cut the dataframe into num_buckets bins
        cut_list: empty list that we will add the dfcut codes to    
    
    Returns:
        list of integers where ith element is the number of full-time workers who fall into the ith bucket.
        empty list if num_buckets <= 0 or max_val <= min_val
    '''

    has_worked = df.hours_worked_per_week >= FULLTIME_MIN_WORKHRS
    working = df.employment_status == 'Working'
    filter =  (has_worked) & (working)
    df = df[filter]

    if num_buckets <= 0 or max_val <= min_val:
        return []

    lin = np.linspace(min_val, max_val, num_buckets + 1)
    col = df[var_of_interest]
    dfcut = pd.cut(col, bins=lin, include_lowest=True, right=False)
    
    cut_list = [0] * num_buckets
    for i in dfcut.cat.codes:
        if i >= 0:
            cut_list[i] += 1

    return cut_list

    
def calculate_unemployment_rates(filenames, age_range, var_of_interest):
    '''
    Calculate the unemployment rate for participants in a given age range (inclusive)
    by values of the variable of interest.

    Inputs:
        filenames: (list of tuples) list of (year, morg filename) tuples (both strings)
        age_range: (pair of ints) (lower_bound, upper_bound)
        var_of_interest: one of "gender", "race", "ethnicity"

    Variables:
        var_df: the dataframe associated with the specific var_of_interest
        df_array: array of each dataframe and its unemployment data
        col_array: array of unemployment data (floats)
        new_df: dataframe using the data from col_array
        con: dataframe from concatenation with all in df_array

    Returns:
        DataFrame with indices as vars_of_interest and columns as filename years
    '''
    filenames = set(filenames)
    filenames = sorted(filenames)

    if len(filenames) == 0 or age_range[1] < age_range[0]:
        return None

    var_df = pd.read_csv(VAR_TO_FILENAME[var_of_interest])
    df_array = []
    for file_i in filenames:
        df = build_morg_df(file_i[1])
        col_array = filter_method(df, var_df, age_range, var_of_interest)
        if var_of_interest == 'ethnicity':
            var_of_interest = 'ethnic'
        rows = var_df[var_of_interest + "_string"]
        new_df = pd.DataFrame(col_array, index=rows, columns=[file_i[0]])
        if var_of_interest == 'ethnic':
            var_of_interest = 'ethnicity'
        new_df.index.name = var_of_interest
        df_array.append(new_df)

    con = pd.concat(df_array, axis=1)
    con = con.sort_index()
    return con
    

def filter_method(df, var_df, age_range, var_of_interest):
    '''
    Calculate the unemployment rate for participants in a given age range (inclusive)
    by values of the variable of interest.

    Inputs:
        df: dataframe object
        var_df: dataframe of the var_of_interest
        age_range: (pair of ints) (lower_bound, upper_bound)
        var_of_interest: one of "gender", "race", "ethnicity"

    Variables:
        col_array: array of unemployment data (floats)
        working_count: (int) number of people working
        not_working_count: (int) number of people unemployed
        age_bool: (boolean) checks if the individual is in the age_range

    Returns:
        array with the unemployment values (list of floats)
    '''
    col_array = []
    if var_of_interest == 'ethnicity':
        var_of_interest = 'ethnic'
    for var in var_df[var_of_interest + "_string"]:
        if var_of_interest == 'ethnic':
            var_of_interest = 'ethnicity'
        working_count = 0
        not_working_count = 0
        age_bool = ((age_range[0] <= df.age) & (df.age <= age_range[1]))
        filter = age_bool & (df[var_of_interest] == var) & \
                 (df.employment_status == 'Working') 
        working_count = len(df[filter])
        filter = age_bool & (df[var_of_interest] == var) & \
                            ((df.employment_status == 'Layoff') | \
                            (df.employment_status == 'Looking'))
        not_working_count = len(df[filter])
        if not_working_count == 0 or not_working_count == 0:
            col_array.append(0.0)
        else:
            labor_force = (working_count + not_working_count)
            col_array.append(not_working_count / labor_force)
    return col_array