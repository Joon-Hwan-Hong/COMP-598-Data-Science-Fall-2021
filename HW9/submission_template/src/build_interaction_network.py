#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# imports
import re
import json
import argparse
import pandas as pd
from collections import Counter


# functions
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--script_input', type=str, required=True)
    parser.add_argument('-o', '--interaction_network', type=str, required=True)
    args = parser.parse_args()

    return args.script_input, args.interaction_network


def get_a_to_b(dic_df, list_episodes):
    df_return = {}
    regex = re.compile(r'(?:\W|^)others(?:\W|$)|(?:\W|^)ponies(?:\W|$)|(?:\W|^)and(?:\W|$)|(?:\W|^)all(?:\W|$)')
    for episode in list_episodes:
        tmp = dic_df[episode].copy()
        tmp['pony2'] = tmp.copy().shift(1)
        tmp = tmp[['pony2', 'pony']].rename(columns={'pony': 'pony2', 'pony2': 'pony'}).dropna()
        # filter: any containing 'others', 'ponies', 'and' & speaking to oneself
        tmp = tmp[~tmp['pony'].str.lower().str.contains(regex)]
        tmp = tmp[~tmp['pony2'].str.lower().str.contains(regex)]
        df_return[episode] = tmp[tmp['pony'] != tmp['pony2']]

    return df_return


def get_lists(dic_df, list_ep, num_top=101):
    list_all_chars = set()
    for ep in list_ep:
        set_ep_chars = set(dic_df[ep].pony).union(set(dic_df[ep].pony2))
        list_all_chars = list_all_chars.union(set_ep_chars)
    tmp = dict.fromkeys([*list_all_chars], 0)
    for ep in list_ep:
        for row in dic_df[ep].itertuples(index=False):
            tmp[row[0]] += row[2]
            tmp[row[1]] += row[2]

    return [*list_all_chars], [character for (character, count) in Counter(tmp).most_common(num_top)]


def get_json(dic_df, list_ep, list_top, dir_output):
    dic_json = {char: dict.fromkeys(list_top, 0) for char in list_top}
    for ep in list_ep:
        for row in dic_df[ep].itertuples(index=False):
            dic_json[row[0]][row[1]] += row[2]
            dic_json[row[1]][row[0]] += row[2]
    dic_json = {char: {other_char: val for other_char, val in dic_json[char].items() if val} for char in list_top}
    with open(dir_output, 'w') as file:
        json.dump(dic_json, file, indent=4)


# main block
def main():
    # init data
    dir_script, dir_output = get_args()
    df = pd.read_csv(dir_script, usecols=['title', 'pony'],encoding='utf-8')

    # df raw --> df per episode -> df {cols= pony1, pony2} --> df {cols= pony1, pony2, directed weight}
    dic_df = dict(tuple(df.groupby('title')))
    dic_df = {ep: dic_df[ep].drop('title', axis=1) for ep in dic_df}
    list_ep = [*dic_df]
    dic_df = get_a_to_b(dic_df, list_ep)
    dic_df = {ep: pd.DataFrame({'wgt': dic_df[ep].groupby(['pony', 'pony2']).size()}).reset_index() for ep in list_ep}

    # filter out if either pony or pony2 countains a non-top 101 character
    list_all, list_top = get_lists(dic_df, list_ep)
    dic_df = {ep: dic_df[ep][dic_df[ep]['pony'].isin(list_top)] for ep in list_ep}
    dic_df = {ep: dic_df[ep][dic_df[ep]['pony2'].isin(list_top)] for ep in list_ep}

    # create json dictionary & export
    get_json(dic_df, list_ep, list_top, dir_output)


if __name__ == "__main__":
    main()
