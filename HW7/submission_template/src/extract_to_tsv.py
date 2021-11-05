#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""

# header metadata
__author__ = 'Joon Hwan Hong'
__version__ = '1.0'
__maintainer__ = 'Joon Hwan Hong'
__email__ = 'joon.hong@mail.mcgill.ca'

# imports
import json
import pandas as pd
import argparse


# functions
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--out_file', type=str)
    parser.add_argument('json_file', type=str)
    parser.add_argument('num_posts_to_output', type=int)
    script_arg = parser.parse_intermixed_args()
    return script_arg.out_file, script_arg.json_file, script_arg.num_posts_to_output


def load_json(file_input):
    # read JSON line format
    with open(file_input) as f:
        lines = f.read().splitlines()
    # load each line into a pandas df
    df_tmp = pd.DataFrame(lines)
    df_tmp.columns = ['json']
    # apply json loads function and normalize to convert into a flat table
    df = pd.json_normalize(df_tmp['json'].apply(json.loads))

    return df[['data.author_fullname', 'data.title']]


def main():
    # get input arguments
    out_file, json_file, num_posts_to_output = get_args()

    # load json lines into a df
    df = load_json(json_file)
    df.columns = ['Name', 'title']
    df = df.reindex(columns=['Name', 'title', 'coding'])

    # num post conditional
    if num_posts_to_output > len(df.index):
        df.to_csv(out_file, sep='\t', index=False)
    else:
        df.sample(num_posts_to_output).to_csv(out_file, sep='\t', index=False)


if __name__ == "__main__":
    main()
