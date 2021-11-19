#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This could've been a lot simpler but I wanted to play around with the networkx library so I had the unnecessary
steps of going from df --> dir graph --> undir graph when it could all be done in pandas in reality
"""

# header metadata
__author__ = 'Joon Hwan Hong'
__version__ = '1.0'
__maintainer__ = 'Joon Hwan Hong'
__email__ = 'joon.hong@mail.mcgill.ca'

# imports
import json
import argparse
import pandas as pd
import networkx as nx
from collections import Counter


# functions
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--script_input', type=str, required=True)
    parser.add_argument('-o', '--interaction_network', type=str, required=True)
    args = parser.parse_args()

    return args.script_input, args.interaction_network


def get_a_to_b(df):
    tmp = df.copy().shift(1) + '|' + df.copy()
    tmp = tmp.drop(0)
    # filter: any containing 'others', 'ponies', 'and' & speaking to oneself
    tmp = tmp[~tmp['pony'].str.lower().str.contains('others|ponies|and|all')]
    tmp[['pony', 'pony2']] = tmp['pony'].str.split('|', 1, expand=True)
    tmp = tmp[tmp['pony'] != tmp['pony2']]

    return tmp


def get_undir_graph(g_d):
    g_u = g_d.to_undirected()
    for node in g_d:
        for nhbr in nx.neighbors(g_d, node): # neighbour
            if node in nx.neighbors(g_d, nhbr):
                g_u.edges[node, nhbr]['weight'] = g_d.edges[node, nhbr]['weight'] + g_d.edges[nhbr, node]['weight']

    return g_u


def get_most_frequent_characters(df_edges, num_characters):
    # get dictionary with total interactions per character
    counts = {}
    for row in df_edges.itertuples(index=False):
        if row[0] in counts:
            counts[row[0]] += row[2]
        else:
            counts[row[0]] = row[2]
        if row[1] in counts:
            counts[row[1]] += row[2]
        else:
            counts[row[1]] = row[2]
    # get the top <num_characters> of interaction characters and list of all
    top_chars = [character for (character, count) in Counter(counts).most_common(num_characters)]
    all_chars = [character for (character, count) in Counter(counts).most_common()]

    return top_chars, all_chars


def df_to_json(df_edges, dir_output, list_c, list_a):
    # construct desired json dictionary structure
    dic = dict.fromkeys(list_a, {})
    for row in df_edges.itertuples(index=False):
        if dic[row[0]] == {}:
            dic[row[0]] = {row[1]: row[2]}
        else:
            dic[row[0]][row[1]] = row[2]
        if dic[row[1]] == {}:
            dic[row[1]] = {row[0]: row[2]}
        else:
            dic[row[1]][row[0]] = row[2]
    # cleanup: remove values of 0, remove those not in top <n>; and write to output
    dic = {p1: {p2: val for p2, val in dic_w0s.items() if val} for p1, dic_w0s in dic.items() if p1 in list_c}
    with open(dir_output, 'w') as file:
        json.dump(dic, file, indent=4)


# main block
def main():
    # init data
    dir_script, dir_output = get_args()
    df = pd.read_csv(dir_script, usecols=['pony'],encoding='utf-8')

    # df {cols= pony1, pony2} --> directed graph --> undirected graph (edge = sum of both direction edges)
    df = get_a_to_b(df)
    df['weight'] = df.groupby(['pony', 'pony2'])['pony'].transform('size')
    g_directed = nx.from_pandas_edgelist(df, 'pony', 'pony2', edge_attr='weight')
    g_undirected = get_undir_graph(g_directed)

    # graph --> df --> json & filter if not top <n> --> export
    df_edges = nx.convert_matrix.to_pandas_edgelist(g_undirected)
    list_characters, list_all = get_most_frequent_characters(df_edges, num_characters=101)
    df_to_json(df_edges, dir_output, list_characters, list_all)


if __name__ == "__main__":
    main()
