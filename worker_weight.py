from threading import Thread
import json
import os

from bs4 import BeautifulSoup
import re
import math
import time
#Data process
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

from posting import Posting


import sys

class Node():
	index_value = ''
	postings = list()

class Index():
	length = 0
	index = list()

class Worker_Weight(Thread):
	def __init__(self,worker_id,indexer):
		self.indexer = indexer
		self.stemmer = PorterStemmer()
		self.worker_id = worker_id
		self.num_partial = 0
		self.weight = dict()
		merged_index_index = open("merged_index.index" ,'r')
		self.merged_index = open("merged_index.full",'r')
		merged_index_index.seek(0,0)
		json_value = merged_index_index.readline()
		data = json.loads(json_value)
		self.index_index = dict(data['index'])
		
		super().__init__(daemon=True)


	def dump(self):
		with open("docs"+str(self.worker_id)+".weight",'w') as f:
			f.write(json.dumps(self.weight))

	def run(self):
		while True:
			target = self.indexer.get_next_file()
			if not target:
				self.dump()
				print("Worker " + str(self.worker_id) + " died")
				break
			
			
			print("Worker " + str(self.worker_id) + " weighting " + target)
			file_load = open(target)
			data = json.load(file_load)
			soup = BeautifulSoup(data["content"],features="lxml")
			url = data['url']
			doc_id = target[target.rfind('/')+1:-5]
			# Gets a cleaner version text comparative to soup.get_text()
			clean_text = ' '.join(soup.stripped_strings)
			# Looks for large white space, tabbed space, and other forms of spacing and removes it
			# Regex expression matches for space characters excluding a single space or words
			clean_text = re.sub(r'\s[^ \w]', '', clean_text)
			# Tokenizes text and joins it back into an entire string. Make sure it is an entire string is essential for get_tf_idf to work as intended
			clean_text = " ".join([i for i in clean_text.split() if i != "" and re.fullmatch('[A-Za-z0-9]+', i)])
			# Stems tokenized text
			clean_text = " ".join([self.stemmer.stem(i) for i in clean_text.split()])
			# Put clean_text as an element in a list because get_tf_idf workers properly with single element lists

			tokens = word_tokenize(clean_text)

			total = 0


			counter = dict()
			#We calculating tf_raw, and positionals here
			for i in range(len(tokens)):
				word = tokens[i]
				if word in counter:
					counter[word]= counter[word] + 1
				else:
					counter[word] = 1

			doc_length = len(tokens)

			for index in tokens:
				to_seek = self.index_index[index]
				self.merged_index.seek(to_seek,0)
				json_value = self.merged_index.readline()

				data = json.loads(json_value)
				df = len(data['postings'])
				tf = counter[index]/doc_length
				idf = math.log(self.indexer.num_doc/df)
				tf_idf = tf*idf
				total = total + tf_idf*tf_idf
				
			self.weight[doc_id] = math.sqrt(total)







			
