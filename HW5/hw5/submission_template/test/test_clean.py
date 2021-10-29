import unittest
from pathlib import Path
from datetime import datetime
import json
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
            data = json.load(f)
            self.assertFalse(('title' in data) or ('title_text' in data))

    def test_date(self):
        with open(self.fixture2, 'r', encoding='utf-8') as f:
            data = json.load(f)
            with self.assertRaises(Exception):
                self.assertIsInstance(datetime.strptime(data['createdAt'], '%Y-%m-%dT%H:%M:%S%z'), datetime)

    def test_valid(self):
        with open(self.fixture3, 'r', encoding='utf-8') as f:
            self.assertNotIsInstance(f.readline(), dict)     # check if raw line is literally a dict

    def test_author(self):
        with open(self.fixture4, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.assertTrue((data['author'] in ('', 'N/A', 'null', None)) or ('author' not in data))

    def test_count(self):
        with open(self.fixture5, 'r', encoding='utf-8') as f:
            data = json.load(f)
            with self.assertRaises(Exception):
                self.assertIsInstance(int(data['total_count']), int)
                self.assertNotIsInstance(data['total_count'], bool)         # boolean edge case

    def test_tags(self):
        with open(self.fixture6, 'r', encoding='utf-8') as f:
            data = json.load(f)
            with self.assertRaises(Exception):
                self.assertEqual(len(data['tags'][0].split()), 1)


if __name__ == '__main__':
    unittest.main()
