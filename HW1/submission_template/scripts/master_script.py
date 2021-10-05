"""
COMP 598 Assignment 1 Doc String.
This is the master script for the assignment. This file consists of library imports of other scripts I made,
constant initialized variables, then the code to collect data, annotate, then analyze

The python files need to be ran under /HW1/submission_template/scripts/. IRAhandle_tweets_1.csv needs to be
located /HW1/submission_template/data/. The code assumes working directory is one level above /HW1/ to work.

Technically regex should be (\b|_) to account for the fact that python regex considers '_' as a \\w character,
but the first instance of a _Trump or Trump_ occurs at 23120, so oh well. We only look at first 10k

Pipeline:
1. Imports various subscripts/functions for use
2. According to initialized variables, collect desired data via data_collection()
3. Create Boolean feature 'trump_mention' if a tweet mentions "Trump" in data_annotation(); save to dataset.tsv
4. Compute the fraction of the tweets that mention Trump; save to results.tsv
"""

# *** imports ***
from HW1.submission_template.scripts.data_collection import data_collection
from HW1.submission_template.scripts.data_annotation import data_annotation
from HW1.submission_template.scripts.analysis import analysis

# const. ini. variables
file_name = '../data/IRAhandle_tweets_1.csv'
file_annotated = '../dataset.tsv'
file_results = '../results.tsv'
list_columns = ['tweet_id', 'publish_date', 'content', 'language']
regex_trump = r'\bTrump\b'
n_rows = 10000

# 1) data collection
df_filtered = data_collection(file_name, n_rows, list_columns)
# 2) data annotation
df_annotated = data_annotation(df_filtered, file_annotated, regex_trump)
# 3) analysis
analysis(df_annotated, file_results)
