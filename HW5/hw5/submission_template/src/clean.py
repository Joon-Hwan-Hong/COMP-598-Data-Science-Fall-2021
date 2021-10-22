#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DOCSTRING
"""

# header metadata
__author__ = 'Joon Hwan Hong'
__version__ = '1.0'
__maintainer__ = 'Joon Hwan Hong'
__email__ = 'joon.hong@mail.mcgill.ca'

# imports
import json
import argparse
import ast
import pandas as pd
import numpy as np


# functions
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str)
    parser.add_argument('-o', '--output', type=str)

    return parser.parse_args().input, parser.parse_args().output


def filter_invalid(input_string):
    list_json = []
    with open(input_string, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            try:                                                # remove posts with invalid dictionary format (5)
                line_dict = ast.literal_eval(lines[i])
                assert type(line_dict) is dict
                list_json.append(line_dict)
            except:
                pass

    return list_json


def filter_total_count(list_json, key_val='total_count'):
    for dic in list_json:
        try:
            assert isinstance(dic[key_val], (int, float, str))      # can only be int, float, or str (also 8)
            dic[key_val] = int(float(dic[key_val]))                 # typecast to int (7)
        except:
            list_json.remove(dic)

    return list_json


def filter_author(list_json, key_val='author'):
    for dic in list_json:
        try:
            assert key_val in dic                                   # author needs to exist
            assert dic[key_val] not in ('', 'N/A', 'null', None)    # author can't be empty, N/A or null (6)
        except:
            list_json.remove(dic)

    return list_json


def filter_title(list_json, key_val=('title', 'title_text')):
    for dic in list_json:
        try:
            if key_val[0] in dic:
                continue
            elif key_val[1] in dic:
                dic[key_val[0]] = dic.pop(key_val[1])               # rename title_text field to title (2)
            else:
                raise Exception                                     # remove all without title or title_text (1)
        except:
            list_json.remove(dic)

    return list_json


def filter_tags(list_json, key_val='tags'):
    for dic in list_json:
        if key_val in dic:      # set comprehension for each word in string items into a list (9)
            dic[key_val] = [*{word for line in dic[key_val] for word in line.split()}]

    return list_json


def main():
    # get script arguments
    str_i, str_o = get_args()

    # get list of JSON dictionaries
    list_j = filter_invalid(str_i)              # filter for 5
    list_js = filter_total_count(list_j)        # filter for 7, 8
    list_jso = filter_author(list_js)           # filter for 6
    list_json = filter_title(list_jso)          # filter for 1, 2
    list_json_o = filter_tags(list_json)        # filter for 9

    # TODO: finish filters for # 3, 4

    # DEBUGGING
    for i in range(len(list_json_o)):
        print(list_json_o[i])
    print(len(list_json_o))


if __name__ == "__main__":
    main()
