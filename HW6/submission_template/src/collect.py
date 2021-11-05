#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Collects data of both sample types described below and dumps it to a json lines format.

Sample 1: Collect the 1000 newest posts from the 10 most popular subreddits by subscribers: funny, AskReddit, gaming,
aww, pics, Music, science, worldnews, videos, todayilearned.
Sample 2: Collect the 1000 newest posts from the 10 most popular subreddits by # of posts by day: AskReddit, memes,
politics, nfl, nba, wallstreetbets, teenagers, PublicFreakout, leagueoflegends, unpopularopinion.
"""

# header metadata
__author__ = 'Joon Hwan Hong'
__version__ = '1.0'
__maintainer__ = 'Joon Hwan Hong'
__email__ = 'joon.hong@mail.mcgill.ca'

# imports
import json
import requests
from requests.auth import HTTPBasicAuth
from pathlib import Path
import os, sys



# functions
def get_oauth():
    # setup authentication and header for reddit api
    auth = requests.auth.HTTPBasicAuth('w4KHRUrwq5S5mpE9q4_3vA', 'mJnuuKQ5Q5_QFsi1ZQusfDblpiOWBA')
    data = {'grant_type': 'password', 'username': '598-collector', 'password': 'comp598mcgill'}
    headers = {'User-Agent': 'CollectorBot/0.0.1'}
    # add authorization to the header's directory
    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
    token = res.json()['access_token']
    headers['Authorization'] = f'bearer {token}'

    return headers


def get_json_files(l_sub, l_pst, headers):
    list_sub = []
    list_pst = []
    # collect json files for the top 10 subbed
    for subreddit in l_sub:
        list_sub.append(
            requests.get(f'https://oauth.reddit.com/r/{subreddit}/new?limit=100', headers=headers).json()['data']['children'])
    # collect json files for the top 10 posts per day
    for subreddit in l_pst:
        list_pst.append(
            requests.get(f'https://oauth.reddit.com/r/{subreddit}/new?limit=100', headers=headers).json()['data']['children'])

    return list_sub, list_pst


def save_json(file_name, list_used):
    with open(os.path.join(Path(__file__).parents[1], file_name), 'w') as f:
        for i in range(0, 10):
            for j in range(0, 100):
                f.write(f'{json.dumps(list_used[i][j])}\n')


def main():
    # constant vars
    l_sub = ('funny', 'AskReddit', 'gaming', 'aww', 'pics', 'Music', 'science', 'worldnews', 'videos', 'todayilearned')
    l_pst = ('AskReddit', 'memes', 'politics', 'nfl', 'nba', 'wallstreetbets', 'teenagers', 'PublicFreakout', 'leagueoflegends', 'unpopularopinion')

    # get authentication
    headers = get_oauth()

    # get json files
    list_sub, list_pst = get_json_files(l_sub, l_pst, headers)

    # save to output json file
    save_json('sample1.json', list_sub)
    save_json('sample2.json', list_pst)


if __name__ == "__main__":
    main()
