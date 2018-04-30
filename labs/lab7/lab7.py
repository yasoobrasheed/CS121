import pandas as pd
import numpy as np

morg_filename="../pa6/data/morg_d07.csv"

ethnic_categories = ['Non-Hispanic', 'Mexican', 'PuertoRican', 
                     'Cuban', 'Dominican',
                     'Salvadoran', 'CentralAmericanExcludingSalvadoran', 
                     'SouthAmerican',  'OtherSpanish']

status_categories = ['Working',
                     'With a job but not at work',
                     'Layoff',
                     'Looking',
                     'Others1',
                     'Unable to work or disabled',
                     'Others2']

# TASK 1
# Load the morg_d07.csv data set here
# Note: The rest of the code in this file will not work until 
# you've done this.

## YOUR CODE HERE ##
morg_df = pd.read_csv(morg_filename, index_col='h_id')

# TASKS 2-5
# For each of the tasks, print the value requested in the task.

# 2
#print(morg_df['age'])

# 3
#print(morg_df.loc['1_2_2'])

# 4
#print(morg_df[:4])

# 5
#filter = morg_df.hours_worked_per_week < 35
#print(morg_df[filter])

## YOUR CODE HERE ##

# Required before tasks 6-8
morg_df["ethnicity_code"] = morg_df["ethnicity_code"].fillna(0)
morg_df["ethnicity_code"] = pd.Categorical.from_codes(morg_df["ethnicity_code"], ethnic_categories)
morg_df.rename(columns={"ethnicity_code":"ethnicity"}, inplace=True)

# TASKS 6-8

## YOUR CODE HERE ##

# 6
morg_df['employment_status_code'] = morg_df['employment_status_code'].fillna(0)
morg_df["employment_status_code"] = pd.Categorical.from_codes(morg_df["employment_status_code"] - 1, status_categories)
morg_df.rename(columns={"employment_status_code":"employment"}, inplace=True)

# 7
#filter = morg_df.employment != "Working"
#print(morg_df[filter])

# 8
#filter = (morg_df.employment != "Working") & (morg_df.hours_worked_per_week < 35)
#print(morg_df[filter])

# Example use of cut()
boundaries = range(16, 89, 8)
morg_df["age_bin"] = pd.cut(morg_df["age"], 
                            bins=boundaries,
                            labels=range(len(boundaries)-1),
                            include_lowest=True, right=False)

# TASKS 9 and 10

## YOUR CODE HERE ##

# 9
bounds = range(0, 100, 10)
morg_df["hours_bin"] = pd.cut(morg_df['hours_worked_per_week'], bins=bounds, labels=range(len(bounds) -1), include_lowest=True, right=False)

# 10
print(morg_df['hours_bin'].value_counts())
print(morg_df.groupby("hours_bin").size())
