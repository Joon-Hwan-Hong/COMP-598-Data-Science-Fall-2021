#!/bin/bash

# 1. number of lines in the file
test_file="$1"
len_file=$(cat $test_file | wc -l)
if [ $len_file -lt 10000 ]; then
	echo $len_file is less than 10k lines.
	exit 1
fi
echo $len_file

# 2. first line of the file (header row)
head -n 1 $test_file

# 3. number of lines in last 10k rows containing <<potus>> case-insensitive
tail -n 10000 $test_file | grep -ci "potus"

# 4. from rows 100-200 (inclusive), how many of them contain the word <<fake>>
sed -ne '100,200p' $test_file | grep -c "\bfake\b"
