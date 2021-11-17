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
from math import log10
from re import sub
import pandas as pd
import argparse
import json


# functions
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--pony_counts', type=str, required=True)
    parser.add_argument('-n', '--num_words', type=int, required=True)
    args = parser.parse_args()

    return args.pony_counts, args.num_words


def get_tf_idfs(tf_all, list_p, num_words):
    dic_out = {}
    for pony in list_p:
        list_w_tf = []
        # make tuple of all words and its tf-idf, then make df and sort by tf-idf value.
        for word in tf_all[pony].keys():
            tf_idf = tf_all[pony][word] * log10(len(list_p) / len([0 for p in list_p if word in tf_all[p].keys()]))
            list_w_tf.append((word, tf_idf))
        # make temp df to sort by tf-idf values given a pair of word and tf-idf ([0] and [1] respectively)
        tmp = pd.DataFrame(list_w_tf).sort_values(by=[1], ascending=False)
        dic_out[pony] = tmp[0].to_list()[0:num_words]

    return dic_out


def pretty_print(dic_out):
    data_json = json.dumps(dic_out, indent=4)
    data_json = sub(r'\[\n {7}', '[', data_json)
    data_json = sub(r'(?<!\]),\n {7}', ',', data_json)
    data_json = sub(r'\n {4}\]', ']', data_json)
    print(data_json)


# main block
def main():
    # init & load data
    list_p = ('twilight sparkle', 'applejack', 'rarity', 'pinkie pie', 'rainbow dash', 'fluttershy')
    file_json, num_words = get_args()
    with open(file_json, 'r') as file:
        tf_all = json.load(file)

    dic_out = get_tf_idfs(tf_all, list_p, num_words)

    pretty_print(dic_out)


if __name__ == "__main__":
    main()
