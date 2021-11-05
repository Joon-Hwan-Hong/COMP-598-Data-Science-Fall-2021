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
import requests
from requests.auth import HTTPBasicAuth
from pathlib import Path
import os
import argparse


# functions
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', type=str)
    parser.add_argument('-s', '--subreddit', type=str)

    return parser.parse_args().output, parser.parse_args().subreddit


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


def get_json_file(subreddit, headers):
    url_request = requests.get(f'https://oauth.reddit.com/r/{subreddit}/new?limit=100', headers=headers)
    new_json = url_request.json()['data']['children']

    return new_json


def save_json(file_name, list_used):
    with open(os.path.join(Path(__file__).parents[1], file_name), 'w') as f:
        for i in range(len(list_used)):
            f.write(f'{json.dumps(list_used[i])}\n')


def main():
    # get input arguments
    dir_out, subreddit = get_args()

    # get authentication
    headers = get_oauth()

    # get json files for the subreddit
    list_1 = get_json_file(subreddit, headers)

    # save as json file
    save_json(dir_out, list_1)


if __name__ == "__main__":
    main()
