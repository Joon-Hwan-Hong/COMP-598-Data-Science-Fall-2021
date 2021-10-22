import unittest
from pathlib import Path
from datetime import datetime
import json
import ast
import os, sys
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)


class CleanTest(unittest.TestCase):
    def setUp(self):
        # paths used
        self.test_path = os.path.join(parentdir, 'test')
        self.fixtures_path = os.path.join(self.test_path, 'fixtures')
        self.fixture_names = os.listdir(self.fixtures_path)
        # load data from fixtures folder.
        self.fixture1 = os.path.join(self.fixtures_path, self.fixture_names[0])
        self.fixture2 = os.path.join(self.fixtures_path, self.fixture_names[1])
        self.fixture3 = os.path.join(self.fixtures_path, self.fixture_names[2])
        self.fixture4 = os.path.join(self.fixtures_path, self.fixture_names[3])
        self.fixture5 = os.path.join(self.fixtures_path, self.fixture_names[4])
        self.fixture6 = os.path.join(self.fixtures_path, self.fixture_names[5])

    def test_title(self):
        with open(self.fixture1, 'r', encoding='utf-8') as f:
            print('Checking if title or title_text exists...')          # assumption that JSON data is a dictionary
            data = json.load(f)
            self.assertTrue(('title' in data) or ('title_text' in data))
            print('OK')

    def test_date(self):
        with open(self.fixture2, 'r', encoding='utf-8') as f:
            print('Checking if date is in ISO 8601 format...')
            data = json.load(f)                         # assert it can be converted with exact ISO 8601 format
            self.assertIsInstance(datetime.strptime(data['createdAt'], '%Y-%m-%dT%H:%M:%S%z'), datetime)
            print('OK')

    def test_valid(self):
        with open(self.fixture3, 'r', encoding='utf-8') as f:
            print('Checking if JSON file is a valid dictionary...')
            self.assertIsInstance(ast.literal_eval(f.readline()), dict)     # check if raw line is literally a dict
            print('OK')

    def test_author(self):
        with open(self.fixture4, 'r', encoding='utf-8') as f:
            print('Checking if author is null, N/A or empty...')
            data = json.load(f)
            self.assertTrue('author' in data)                                       # author needs to exist as a key
            self.assertTrue(data['author'] not in ('', 'N/A', 'null', None))        # can't be empty, N/A or null
            print('OK')

    def test_count(self):
        with open(self.fixture5, 'r', encoding='utf-8') as f:
            print('Checking if total_count is a str containing a castable number (int or float)...')
            data = json.load(f)
            self.assertIsInstance(data['total_count'], str)                 # could put (int, float, str) instead
            self.assertIsInstance(int(float(data['total_count'])), int)     # check if would be casted into an int
            print('OK')

    def test_tags(self):
        with open(self.fixture6, 'r', encoding='utf-8') as f:
            print('Checking if tag field gets split when given 3 words...')     # assumption that 'tags' exist in JSON
            data = json.load(f)
            for word in data['tags']:                       # for each word in list, see if str.split() length is 1
                self.assertEqual(len(word.split()), 1)
            print('OK')


if __name__ == '__main__':
    unittest.main()
