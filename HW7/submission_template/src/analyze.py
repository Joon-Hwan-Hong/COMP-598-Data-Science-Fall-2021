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
    parser.add_argument('-i', '--coded_file', type=str, required=True)
    parser.add_argument('-o', '--output_file', type=str, required=False)
    args = parser.parse_args()

    return args


def main():
    # get input arguments
    args = get_args()

    # tsv --> pandas series --> value counts --> dict
    dic = pd.read_csv(args.coded_file, sep='\t', header=0)['coding'].value_counts().to_dict()

    # rename keys for pretty print
    pref_order = ['course-related', 'food-related', 'residence-related', 'other']
    default_keys = ['c', 'f', 'r', 'o']
    for i in range(len(default_keys)):
        dic[pref_order[i]] = dic.pop(default_keys[i], 0)

    # either save to output file or print to stdout
    if args.output_file is None:
        print(dic)
    else:
        json.dump(dic, open(args.output_file, 'w'), indent=4)


if __name__ == "__main__":
    main()
