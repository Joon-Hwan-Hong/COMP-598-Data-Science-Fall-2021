#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# header metadata
__author__ = 'Joon Hwan Hong'
__version__ = '1.0'
__maintainer__ = 'Joon Hwan Hong'
__email__ = 'joon.hong@mail.mcgill.ca'

# imports
import pandas as pd
import argparse
import json


# functions
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output_file', type=str, required=True)
    parser.add_argument('-d', '--data_file', type=str, required=True)
    args = parser.parse_args()

    return args.output_file, args.data_file


def get_files(file_data, dir_stop, list_p, no_punc):
    # dialog df
    df = pd.read_csv(file_data, encoding='utf-8')[['pony', 'dialog']]
    df = df[df['pony'].str.lower().isin(list_p)]
    df['dialog'] = df['dialog'].str.lower().str.translate(no_punc).str.split()
    # list_stop
    with open(dir_stop) as file_stop:
        list_stop = file_stop.read().splitlines()[6:]

    return df, list_stop


def get_list_words(df, list_stop):
    # flatten list-of-lists to list, apply stop words and strip filter.
    list_diag = df['dialog'].to_list()
    words_all = [word for sublist in list_diag for word in sublist if word not in list_stop and word.isalpha()]
    wc = pd.Series(words_all).value_counts()
    wc = wc[wc >= 5]

    return wc.index.tolist()


def get_wcs(list_p, list_words, df):
    wordcount_p = {}
    for pony in list_p:
        list_d = df[df['pony'].str.lower() == pony]['dialog'].to_list()
        words_p = [word for dialog in list_d for word in dialog if word in list_words]
        wordcount_p[pony] = pd.Series(words_p).value_counts().to_dict()

    return wordcount_p


def save_json(wordcount_p, file_output):
    with open(file_output, 'w') as file:
        json.dump(wordcount_p, file, indent=4)


# main block
def main():
    # init vars
    file_output, file_data = get_args()
    no_punc = str.maketrans('()[],-.?!:;#&', ' ' * 13)
    list_p = ('twilight sparkle', 'applejack', 'rarity', 'pinkie pie', 'rainbow dash', 'fluttershy')

    # get init data
    df, list_stop = get_files(file_data, '../data/stopwords.txt', list_p, no_punc)

    # get individual word counts
    list_words = get_list_words(df, list_stop)
    wordcount_p = get_wcs(list_p, list_words, df)

    # save to json output
    save_json(wordcount_p, file_output)


if __name__ == "__main__":
    main()
