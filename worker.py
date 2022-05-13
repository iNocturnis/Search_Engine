from threading import Thread
import json
import os
import shelve
from bs4 import BeautifulSoup
from time import perf_counter
import time
import pickle

import re


#Data process
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
from collections import Counter

from posting import Posting


import sys

class Worker(Thread):
	def __init__(self,indexer,target):
		self.file = target
		self.indexer = indexer
		super().__init__(daemon=True)

	def run(self):
		print("Target: " + str(self.file))

		file_load = open(self.file)
		data = json.load(file_load)
		soup = BeautifulSoup(data["content"],features="lxml")
		# Gets a cleaner version text comparative to soup.get_text()
		clean_text = ' '.join(soup.stripped_strings)
		# Looks for large white space, tabbed space, and other forms of spacing and removes it
		# Regex expression matches for space characters excluding a single space or words
		clean_text = re.sub(r'\s[^ \w]', '', clean_text)
		# Tokenizes text and joins it back into an entire string. Make sure it is an entire string is essential for get_tf_idf to work as intended
		clean_text = " ".join([i for i in clean_text.split() if i != "" and re.fullmatch('[A-Za-z0-9]+', i)])
		# Stems tokenized text
		clean_text = " ".join([self.indexer.stemmer.stem(i) for i in clean_text.split()])
		# Put clean_text as an element in a list because get_tf_idf workers properly with single element lists
		x = [clean_text]
		# ngrams is a dict
		# structure looks like {ngram : {0: tf-idf score}}
		ngrams = self.indexer.get_tf_idf(x)

		for ngram, tfidf in ngrams.items():
			posting = Posting(self.indexer.get_url_id(data["url"]), tfidf[0])
			self.indexer.save_index(ngram,posting)

