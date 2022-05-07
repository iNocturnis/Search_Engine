from threading import Thread
import json
import os
import shelve
from bs4 import BeautifulSoup
from time import perf_counter
import time

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
		ticker = perf_counter()
		tic = perf_counter()
		file_load = open(self.file)
		data = json.load(file_load)
		soup = BeautifulSoup(data["content"],features="lxml")
		words = word_tokenize(soup.get_text())
		toc = perf_counter()
		if toc - tic > 1 :
			print("Took " + str(toc - tic) + "seconds to tokenize text !")

		tokenized_words = list()
		stemmed_words = list()

		tic = perf_counter()
		for word in words:
			if word != "" and re.fullmatch('[A-Za-z0-9]+',word):
				#So all the tokenized words are here,
				tokenized_words.append(word)
		toc = perf_counter()
		if toc - tic > 1 :
			print("Took " + str(toc - tic) + "seconds to isalnum text !")
		#YOUR CODE HERE

		tic = perf_counter()
		for word in tokenized_words:
			stemmed_words.append(self.indexer.stemmer.stem(word))
			#stemming,
			#tf_idf
			#get_tf_idf(stemmed_words,word)
			#post = Posting()
		toc = perf_counter()
		if toc - tic > 1 :
			print("Took " + str(toc - tic) + "seconds to stemmed text !")

		counts = Counter(stemmed_words)
		size = len(stemmed_words)
		for word in counts:
			#posting = Posting(data["url"],self.get_tf_idf(list(' '.join(stemmed_words)),word))
			tic = perf_counter()
			posting = Posting(data["url"],counts[word]/size)
			toc = perf_counter()
			if toc - tic > 1 :
				print("Took " + str(toc - tic) + "seconds to tf_idf text !")

			tic = perf_counter()
			self.indexer.save_index(word,posting)
			toc = perf_counter()
			if toc - tic > 1 :
				print("Took " + str(toc - tic) + "seconds to save text !")

		tocker = perf_counter()
		print("Finished " + data['url'] + "\n" + str(tocker-ticker))
