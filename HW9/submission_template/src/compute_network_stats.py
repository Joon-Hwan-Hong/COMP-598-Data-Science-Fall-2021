#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
from operator import itemgetter as ig


# functions
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interaction_network', type=str, required=True)
    parser.add_argument('-o', '--output', type=str, required=True)
    args = parser.parse_args()

    return args.interaction_network, args.output


# main block
def main():
    # load interaction network --> json --> df
    dic_json = {}
    dir_script, dir_output = get_args()
    with open(dir_script, 'r') as file:
        df = pd.json_normalize(json.load(file), sep='|').transpose()
        df[1] = df.index
        df.columns = ['weight', 'edge']
        df[['source', 'target']] = df['edge'].str.split('|', expand=True)
        df = df.drop(columns=['edge'])

    # df --> undirected graph
    g = nx.from_pandas_edgelist(df, 'source', 'target', create_using=nx.Graph(), edge_attr='weight')

    # get top 3 by: (edge weight, number of edges, betweenness)
    list_edge_weight = sorted([*g.degree(weight='weight')], key=ig(1), reverse=True)[0:3]
    list_edges_num = sorted([*g.degree()], key=ig(1), reverse=True)[0:3]
    list_between = sorted([*nx.algorithms.centrality.betweenness_centrality(g).items()], key=ig(1), reverse=True)[0:3]
    dic_json['most_connected_by_weight'] = [name for name, weight in list_edge_weight]
    dic_json['most_connected_by_num'] = [name for name, edges in list_edges_num]
    dic_json['most_central_by_betweenness'] = [name for name, betweeness in list_between]

    # save to json
    with open(dir_output, 'w') as file2:
        json.dump(dic_json, file2, indent=4)


if __name__ == "__main__":
    main()
