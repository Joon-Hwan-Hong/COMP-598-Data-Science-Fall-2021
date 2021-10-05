"""
COMP 598 Assignment 3 Doc String.
Count shows the number of speech acts that each character has in the entire file.
Verbosity gives fraction of dialogue, measured in # of speech acts produced by this pony.

This file generates a JSON file from the clean_dialog.csv given for MLP.
Typecasting counts to int because json does not recognize Numpy data types (int64)

Pipeline:
1. initialize variables & read cleaned csv
2. for each pony name, calculate count and verbosity values
3. export to json file
"""

# imports
import json
import sys
import pandas as pd

# initialize
list_p = ['twilight sparkle', 'applejack', 'rarity', 'pinkie pie', 'rainbow dash', 'fluttershy']
df = pd.read_csv(sys.argv[2])
count = {}
verbosity = {}

# for each name, get total count & the fraction compared to entire # of interactions.
for name in list_p:
    count[name] = int(df['pony'].str.fullmatch(name, case=False).sum())
    verbosity[name] = round(count[name]/len(df.index), 2)

# write output JSON file
data = {"count": count, "verbosity": verbosity}
with open(sys.argv[1], 'w') as f:
    json.dump(data, f, indent=4)