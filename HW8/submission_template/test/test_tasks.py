import unittest
from pathlib import Path
import os, sys
import json
from math import log10
from submission_template.src.compile_word_counts import get_files, get_list_words, get_wcs
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)


class TasksTest(unittest.TestCase):
    def setUp(self):
        dir = os.path.dirname(__file__)
        self.mock_dialog = os.path.join(dir, 'fixtures', 'mock_dialog.csv')
        self.true_word_counts = os.path.join(dir, 'fixtures', 'word_counts.true.json')
        self.true_tf_idfs = os.path.join(dir, 'fixtures', 'tf_idfs.true.json')

    def test_task1(self):
        with open(self.true_word_counts, 'r') as f, open(self.mock_dialog, 'r') as f2:
            t_wc = json.load(f)
            # ****** from my compile_word_counts.py ******
            no_punc = str.maketrans('()[],-.?!:;#&', ' ' * 13)
            list_p = ('twilight sparkle', 'applejack', 'rarity', 'pinkie pie', 'rainbow dash', 'fluttershy')
            df, list_stop = get_files(f2, '../data/stopwords.txt', list_p, no_punc)
            list_words = get_list_words(df, list_stop)
            wordcount_p = get_wcs(list_p, list_words, df)
            # ***********************

        # assert test
        self.assertEqual(wordcount_p, t_wc)
        print('test_task1 OK')

    def test_task2(self):
        with open(self.true_word_counts, 'r') as f, open(self.true_tf_idfs, 'r') as f2:
            t_wc = json.load(f)
            true_tf_idfs = json.load(f2)
            # ****** copy and paste from my compute_pony_lang.py, but with tf-idf instead of word order ******
            dic_result = {}
            for pony in t_wc.keys():
                dic_pony = {}
                for word in t_wc[pony]:
                    tf_idf = t_wc[pony][word] * log10(len(t_wc) / len([0 for p in t_wc.keys() if word in t_wc[p].keys()]))
                    dic_pony[word] = round(tf_idf, 11)
                dic_result[pony] = dic_pony
            # ***********************

        # assert test
        self.assertEqual(dic_result, true_tf_idfs)
        print('test_task2 OK')
        
    
if __name__ == '__main__':
    unittest.main()