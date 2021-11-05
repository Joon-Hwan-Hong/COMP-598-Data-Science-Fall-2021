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
from bs4 import BeautifulSoup
import argparse
import json
import requests
import os.path
import re


# functions
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type=str)
    parser.add_argument('-o', '--output', type=str)

    return parser.parse_args().config, parser.parse_args().output


def load_config(str_cfg):
    with open(str_cfg, 'r') as f:
        dic_cfg = json.load(f)
        dir_cache = dic_cfg['cache_dir']
        target_people = dic_cfg['target_people']

    return dir_cache, target_people


def get_relation_list(dir_cache, person, json_output):
    # download non-dynamic html page of the person
    if not os.path.isfile(os.path.join(dir_cache, person)):
        open(os.path.join(dir_cache, person), 'wb').write(requests.get(f'https://www.whosdatedwho.com/dating/{person}').content)

    # get to overall section for the person
    soup = BeautifulSoup(open(os.path.join(dir_cache, person), 'r', encoding="utf8"), 'html.parser')
    div_person = soup.find('div', class_='ff-panel clearfix')

    # edge case for when an incorrect or non-existing person is put in
    try:
        h4_about = div_person.find('h4', class_='ff-auto-about')
    except AttributeError:
        json_output[person] = []
        return

    # remove content after the "about" section
    for item in h4_about.find_next_siblings():
        item.decompose()
    h4_about.decompose()

    # get a list of links & remove self-reference if needed
    list_regex = [*{a['href'] for a in div_person.find_all('a', href=True) if re.search('/dating/', str(a))}]
    if f'/dating/{person}' in list_regex:
        list_regex.remove(f'/dating/{person}')
    list_cleaned = [b.removeprefix('/dating/') for b in list_regex]
    json_output[person] = list_cleaned


def pretty_export(str_out, json_output):
    with open(str_out, 'w') as f_out:
        t = json.dumps(json_output, indent=4)
        t = re.sub('\[\n {7}', '[', t)
        t = re.sub('(?<!\]),\n {7}', ',', t)
        t = re.sub('\n {4}\]', ']', t)
        f_out.write(t)


def main():
    # get input arguments
    str_cfg, str_out = get_args()

    # load config json file
    dir_cache, target_people = load_config(str_cfg)

    # create the dictionary {key: person, value: list of people 'dated'}
    json_output = {}
    for person in target_people:
        get_relation_list(dir_cache, person, json_output)

    # save to JSON file with pretty print
    pretty_export(str_out, json_output)


if __name__ == "__main__":
    main()
