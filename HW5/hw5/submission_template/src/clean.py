#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to clean up incorrect/messy JSON entries, cleaning files containing user posts recorded as JSON data.

Assumption:
each line in file is a JSON object as a single post.

Function:
1. remove all posts without 'title' or 'title_text' field
2. rename all 'title_text field' to 'title'
3. standardize all times to UTC timezone according to ISO 8601 date and time format
4. remove all posts of createdAt time that can not be parsed into ISO 8601 date and time format
5. remove all posts that are not dictionaries
6. remove all posts that have 'author' field as 'null', None, '', 'N/A', or field does not exist
7. remove all posts with 'total count' field that is not an integer, float, or string
8. keep post if 'total_count' field does not exist
9. separate all words within the list field 'tags' with <<space>> as the delimiter
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
from datetime import datetime, timezone


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
            if key_val in dic:                                      # only if total_count exists
                assert isinstance(dic[key_val], (int, float, str))  # can only be int, float, or str (also 8)
                dic[key_val] = int(dic[key_val])                    # typecast to int (7)
        except:
            list_json.remove(dic)

    return list_json


def filter_author(list_json, key_val='author'):
    for dic in list_json:
        try:
            if key_val in dic:                                          # author needs to exist
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
        if key_val in dic:                  # set comprehension for each word in string items into a list (9)
            dic[key_val] = [*{word for line in dic[key_val] for word in line.split()}]
            # if they wanted to keep duplicate tags for some dumb reason
            # dic[key_val] = [word for line in dic[key_val] for word in line.split()]

    return list_json


def filter_datetime(list_json, key_val='createdAt'):
    for dic in list_json:
        try:
            if key_val in dic:
                test = datetime.strptime(dic[key_val], '%Y-%m-%dT%H:%M:%S%z')       # convert into ISO 8601
                dic[key_val] = test.astimezone(timezone.utc).isoformat()            # convert to UTC timezone
        except:
            list_json.remove(dic)

    return list_json


def reorder_keys(list_json, pref_order):
    new_list = []
    for dic in list_json:
        new_dic = {}
        for key in pref_order:
            try:
                new_dic[key] = dic[key]
            except:
                pass
        new_list.append(new_dic)
    return new_list


def main():
    # get script arguments
    str_i, str_o = get_args()

    # get list of JSON dictionaries
    list_json = filter_invalid(str_i)               # filter for 5
    list_json = filter_total_count(list_json)       # filter for 7, 8
    list_json = filter_author(list_json)            # filter for 6
    list_json = filter_title(list_json)             # filter for 1, 2
    list_json = filter_tags(list_json)              # filter for 9
    list_json = filter_datetime(list_json)          # filter for 3, 4

    # pretty print reordering (not necessary, I just like how it looks)
    pref_order = ['title', 'createdAt', 'text', 'author', 'total_count', 'tags']
    list_json = reorder_keys(list_json, pref_order)

    # save one JSON dictionary per line
    with open(str_o, 'w') as f:
        f.write('\n'.join(json.dumps(i) for i in list_json))


if __name__ == "__main__":
    main()
