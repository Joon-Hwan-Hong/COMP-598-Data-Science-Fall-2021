#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File Structure:
-- imports
-- functions
-- main()

Data processing script for nyc_311_limit.csv (assumes .csv file is in same directory)
1. Filters incorrect/missing datapoints
2. Extract information on month and duration of police incidents given all entries
3. Calculate the monthly average incident in hours per ZIP code
4. Obtain list of total unique ZIP codes available for the Dropdown
5. Obtain Monthly Average for every ZIP
6. Obtain monthly average for ALL ZIP codes
7. Save data as JSON to export & use on Bokeh Ubuntu server on AWS
"""

# header metadata
__author__ = 'Joon Hwan Hong'
__version__ = '1.0'
__maintainer__ = 'Joon Hwan Hong'
__email__ = 'joon.hong@mail.mcgill.ca'

# imports
import json
import numpy as np
import pandas as pd
from datetime import datetime
from math import isnan


def data_preprocess():
    # get raw value of incident creation, closed, ZIP, and status
    df_raw = pd.read_csv('nyc_311_limit.csv', usecols=[1, 2, 8, 19], header=None, low_memory=False)

    # filter: get indicents opened in 2020
    df_2020 = df_raw[df_raw[1].str.contains('2020')]

    # filter: get only closed incidents
    df_closed = df_2020[df_2020[19].str.match('Closed')]
    del df_closed[19]

    # filter: get only incidents with a ZIP code & any other missing data
    df_nan = df_closed.dropna()

    # reformat: convert open and close to datetime datastructures
    pd.set_option('mode.chained_assignment', None)  # supressing warning
    df_nan[1] = pd.to_datetime(df_nan[1], format='%m/%d/%Y %I:%M:%S %p')
    df_nan[2] = pd.to_datetime(df_nan[2], format='%m/%d/%Y %I:%M:%S %p')

    # filter: only keep datapoints if close date > open date
    df_cleaned = df_nan[df_nan[1] < df_nan[2]]

    # pretty print
    df_cleaned.columns = ['Open', 'Close', 'ZIP']
    df_cleaned = df_cleaned.reset_index(drop=True)

    return df_cleaned


def data_process(df_cleaned):
    # create month column
    df_processed = df_cleaned
    df_processed['Month'] = df_processed['Close'].dt.month

    # calculate difference in datetimein hours
    df_processed['Duration (h)'] = (df_processed['Close'] - df_processed['Open']).dt.total_seconds() / 3600

    # pretty print
    del df_processed['Open']
    del df_processed['Close']

    return df_processed


def data_monthly(df_processed):
    list_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    Month = {}
    for i in range(1, 13):
        # filter for the month
        tmp_df = df_processed[df_processed['Month'] == i]
        del tmp_df['Month']
        # group by ZIP code then calculate mean duration
        Month[list_months[i - 1]] = tmp_df.groupby('ZIP', as_index=False)['Duration (h)'].mean()

    return Month, list_months


def data_zip(unique_zips, list_months, Month):
    zip_dict = {}
    for zip_code in unique_zips:
        zip_arr = np.array([])
        for month in list_months:
            curr_zip = Month[month][Month[month]['ZIP'] == str(zip_code)]  # really inefficient
            if curr_zip.empty:
                month_val = 0
            else:
                month_val = curr_zip.values[0, 1]
            zip_arr = np.append(zip_arr, month_val)
        zip_dict[int(zip_code)] = zip_arr
    return zip_dict


def data_export(unique_zips, zip_dict, monthly_all):
    # change np arrays to list for json compatibility
    new_zip_dict = {k: v.tolist() for k, v in zip_dict.items()}

    # reformatting unique_zips
    unique_zips[0] = '83'
    tuple_zips = [(x, x) for x in unique_zips]

    # export
    with open('data_loaded.json', 'w') as f:
        json.dump([tuple_zips, new_zip_dict, monthly_all], f)


def main():
    # =========== 1. ===========
    df_cleaned = data_preprocess()

    # =========== 2. ===========
    df_processed = data_process(df_cleaned)

    # =========== 3. ===========
    Month, list_months = data_monthly(df_processed)

    # =========== 4. ===========
    unique_zips = sorted(df_processed['ZIP'].unique().tolist())

    # =========== 5. ===========
    zip_dict = data_zip(unique_zips, list_months, Month)

    # =========== 6. ===========
    monthly_all = [Month[x]['Duration (h)'].mean() if not isnan(Month[x]['Duration (h)'].mean()) else 0
                   for x in list_months]

    # =========== 7. ===========
    data_export(unique_zips, zip_dict, monthly_all)


if __name__ == "__main__":
    main()
