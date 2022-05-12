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

		important = {'b' : [], 'h1' : [], 'h2' : [], 'h3' : [], 'title' : []}
		for key_words in important.keys():
			for i in soup.findAll(key_words):
				for word in word_tokenize(i.text):
					important[key_words].append(self.indexer.stemmer.stem(word))

		tic = perf_counter()
		for word in words:
			if word != "" and re.fullmatch('[A-Za-z0-9]+',word):
				tokenized_words.append(word)
		toc = perf_counter()
		if toc - tic > 1 :
			print("Took " + str(toc - tic) + "seconds to isalnum text !")

		tic = perf_counter()
		for word in tokenized_words:
			stemmed_words.append(self.indexer.stemmer.stem(word))

		toc = perf_counter()
		if toc - tic > 1 :
			print("Took " + str(toc - tic) + "seconds to stemmed text !")

			"""
		tfidf = TfidfVectorizer(ngram_range=(1,3)) # ngram_range is range of n-values for different n-grams to be extracted (1,3) gets unigrams, bigrams, trigrams
		tfidf_matrix = tfidf.fit_transform(stemmed_words)  # fit trains the model, transform creates matrix
		#df = pd.DataFrame(tfidf_matrix.toarray(), columns = tfidf.get_feature_names_out()) # store value of matrix to associated word/n-gram
		tfidf.sget_feature_names_out()
		#tf_idf_dict = df.to_dict() # transform dataframe to dict *could be expensive the larger the data gets, tested on ~1000 word doc and took 0.002 secs to run
		
		print(tfidf_matrix)
		"""

		tfIdfVectorizer=TfidfVectorizer(use_idf=True)
		tfIdf = tfIdfVectorizer.fit_transform(stemmed_words)
		df = pd.DataFrame(tfIdf[0].T.todense(), index=tfIdfVectorizer.get_feature_names_out(), columns=["TF-IDF"])
		df = df.sort_values('TF-IDF', ascending=False)

		print(df.head(25))

		for word in tf_idf_dict.keys():
			tic = perf_counter()
			print(tf_idf_dict)
			weight = 1.0
			for k,v in important.items():
				if k == 'b' and word in v:
					weight = 1.2
				elif k == 'h1' and word in v:
					weight = 1.75
				elif k == 'h2' and word in v:
					weight = 1.5
				elif k == 'h3' and word in v:
					weight = 1.2
				elif k == 'title' and word in v:
					weight = 2
			
			posting = Posting(data["url"],tf_idf_dict[word]*weight)
			
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
