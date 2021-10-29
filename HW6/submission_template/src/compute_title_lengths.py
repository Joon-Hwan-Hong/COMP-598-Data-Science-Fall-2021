#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Given an input JSON lines file from reddit posts from collect.py, return the average title length as number of
characters. The script is called like: python3 compute_title_lengths.py <input_file>.
"""

# header metadata
__author__ = 'Joon Hwan Hong'
__version__ = '1.0'
__maintainer__ = 'Joon Hwan Hong'
__email__ = 'joon.hong@mail.mcgill.ca'

# imports
import pandas as pd
import json
import sys


# functions
def load_json(file_input):
    # read JSON line format
    with open(file_input) as f:
        lines = f.read().splitlines()
    # load each line into a pandas df
    df_tmp = pd.DataFrame(lines)
    df_tmp.columns = ['json']
    # apply json loads function and normalize to convert into a flat table
    df = pd.json_normalize(df_tmp['json'].apply(json.loads))

    return df['data.title']


def main():
    # load and get data.title for both samples
    file_name = sys.argv[1]
    df = load_json(file_name)

    # print mean character count for the file
    print(df.str.len().mean())


if __name__ == "__main__":
    main()
