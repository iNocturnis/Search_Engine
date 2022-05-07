#We have to import the files
#Split the indexer into 4 parts
#Alphanumeric sequences into the dataset
#Stemming
#Text in bold, headings and other titles should be treated as more important

#Posting structure > tf-idf score. Name/id the token was found in . So hashmap.
#We need shelves to hold the data.

#Posting ---> Source of file, tf-idf score. #for now we will only use these two, as we get more complex posting will be change accordingly

#Data input
import json
import os
import shelve
from bs4 import BeautifulSoup
from time import perf_counter
import time
import threading


#Data process
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np

import re

#Logging postings
from posting import Posting
from worker import Worker


class Indexer():
	def __init__(self,restart,trimming):
		#Config stuffs
		self.path = "data/DEV/"
		self.restart = restart
		self.trimming = trimming
		self.stemmer = PorterStemmer()

		#Shelves for index
		#https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html
		#https://www.irishtimes.com/news/science/how-many-numbers-begin-with-a-1-more-than-30-per-cent-1.4162466
		#According to this will be how we split things
		#Save #1 = ABCD + (1) ~ 18.3% of words
		#Save #2 = EFGHIJK + (2-3)~ 27.1% of words
		#Save #3 = LMNOPQ + (4-7) ~ 25.4% of words
		#Save #4 = RSTUVWXYZ + (8-9)~ 29.2% of words
		#Save #5 = Special characters
		if os.path.exists("save_1.shelve") and restart:
			os.remove("save_1.shelve")
		if os.path.exists("save_2.shelve") and restart:
			os.remove("save_2.shelve")
		if os.path.exists("save_3.shelve") and restart:
			os.remove("save_3.shelve")
		if os.path.exists("save_4.shelve") and restart:
			os.remove("save_4.shelve")
		if os.path.exists("save_5.shelve") and restart:
			os.remove("save_5.shelve")


		self.save_1 = shelve.open("save_1.shelve")
		self.save_1_lock = threading.Lock()
		self.save_2 = shelve.open("save_2.shelve")
		self.save_2_lock = threading.Lock()
		self.save_3 = shelve.open("save_3.shelve")
		self.save_3_lock = threading.Lock()
		self.save_4 = shelve.open("save_4.shelve")
		self.save_4_lock = threading.Lock()
		self.save_5 = shelve.open("save_5.shelve")
		self.save_5_lock = threading.Lock()

		print(len(list(self.save_1.keys())))
		print(len(list(self.save_2.keys())))
		print(len(list(self.save_3.keys())))
		print(len(list(self.save_4.keys())))
		print(len(list(self.save_5.keys())))

	def save_index(self,word,posting):
		cur_save = self.get_save_file(word)
		lock = self.get_save_lock(word)
		lock.acquire()
		shelve_list = list()
		try:
			shelve_list = cur_save[word]
			shelve_list.append(posting)
			tic = perf_counter()
			shelve_list.sort(key=lambda x: x.tf_idf, reverse = True)
			toc = perf_counter()
			if toc - tic > 1 :
				print("Took " + str(toc - tic) + "seconds to sort shelve list !")
			cur_save.sync()
			lock.release()
		except:
			shelve_list.append(posting)
			cur_save[word] = shelve_list
			cur_save.sync()
			lock.release()

	def get_save_file(self,word):
		#return the correct save depending on the starting letter of word
		word_lower = word.lower()

		if re.match(r"^[a-d0-1].*",word_lower):
			return self.save_1
		elif re.match(r"^[e-k2-3].*",word_lower):
			return self.save_2
		elif re.match(r"^[l-q4-7].*",word_lower):
			return self.save_3
		elif re.match(r"^[r-z8-9].*",word_lower):
			return self.save_4
		else:
			print(word)
			print("You have somehow went beyond the magic")
			return self.save_5
	def get_save_lock(self,word):
		word_lower = word.lower()
		if re.match(r"^[a-d0-1].*",word_lower):
			return self.save_1_lock
		elif re.match(r"^[e-k2-3].*",word_lower):
			return self.save_2_lock
		elif re.match(r"^[l-q4-7].*",word_lower):
			return self.save_3_lock
		elif re.match(r"^[r-z8-9].*",word_lower):
			return self.save_4_lock
		else:
			print(word)
			print("You have somehow went beyond the magic")
			return self.save_5_lock.acquire()
	# I have a test file (mytest.py) with pandas but couldn't figure out how to grab just a single cell.
	# so I came up with this, if anyone knows how to get a single cell and can explain it to
	# me I would love to know, as I think that method might be quicker, maybe, idk it like
	# 4am
	# https://stackoverflow.com/questions/34449127/sklearn-tfidf-transformer-how-to-get-tf-idf-values-of-given-words-in-documen

	# Andy: added paramenter imporant_words in order to do multiplication of score
	def get_tf_idf(self,words,word, important_words):
		#tf_idf
		#words = whole text
		#word the word we finding the score for
		#return the score
		try:
			tfidf = TfidfVectorizer()
			tfidf_matrix = tfidf.fit_transform(words)
			df = pd.DataFrame(tfidf_matrix.toarray(), columns = tfidf.get_feature_names_out())
			score = df.iloc[0][''.join(word)]
			for k,v in important_words.items():
				if k == 'b' and word in v:
					score = score * 1.2
				elif k == 'h1' and word in v:
					score = score * 1.75
				elif k == 'h2' and word in v:
					score = score * 1.5
				elif k == 'h3' and word in v:
					score = score * 1.2
				elif k == 'title' and word in v:
					score = score * 2
			return(score)
			#print(df)
		except KeyError: 
			return -1


	def get_data(self):

		num_threads = 8
		threads = list()

		for directory in os.listdir(self.path):
			for file in os.listdir(self.path + "/" + directory + "/"):
				#Actual files here
				#JSON["url"] = url of crawled page, ignore fragments
				#JSON["content"] = actual HTML
				#JSON["encoding"] = ENCODING
				index = 0
				while True:
					file_path = self.path + "" + directory + "/"+file
					if len(threads) < num_threads:
						thread = Worker(self,file_path)
						threads.append(thread)
						thread.start()
						break
					else:
						if not threads[index].is_alive():
							threads[index] = Worker(self,file_path)
							threads[index].start()
							break
						else:
							index = index + 1
							if(index >= num_threads):
								index = 0
							time.sleep(.1)
	
	#Found 55770 documents
	#

				#getting important tokens
				
						

		



				




def main():
	indexer = Indexer(True,0)
	indexer.get_data()

if __name__ == "__main__":
	main()