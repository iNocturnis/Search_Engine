from threading import Thread
import json
import os

from bs4 import BeautifulSoup
import re


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

class Worker(Thread):
	def __init__(self,worker_id,indexer):
		self.indexer = indexer
		self.stemmer = PorterStemmer()
		self.worker_id = worker_id
		self.num_partial = 0
		self.index = dict()
		super().__init__(daemon=True)

	def dump(self):
		part_index = Index()
		part_index.length = 0
		part_index.index = list()

		cur_partial_index_str = str(self.worker_id) + "_" + str(self.num_partial) + '.partial'
		cur_partial_index_index_str = str(self.worker_id) + "_" + str(self.num_partial) + '.index'


		cur_partial_index = open(cur_partial_index_str,'w')
		cur_partial_index_index = open(cur_partial_index_index_str,'w')

		for key in self.index:
			node = Node()
			node.index_value = key
			node.postings = self.index[key]

			jsonStr = json.dumps(node, default=lambda o: o.__dict__,sort_keys=False)

			part_index.index.append((node.index_value,cur_partial_index.tell()))
			cur_partial_index.write(jsonStr + '\n')
			part_index.length = part_index.length + 1

		part_index.index.sort(key=lambda y:y[0])
		jsonStr =json.dumps(part_index, default=lambda o: o.__dict__,sort_keys=False)
		cur_partial_index_index.write(jsonStr)

		self.num_partial = self.num_partial + 1
		self.indexer.add_partial_index(str(self.worker_id) + "_" + str(self.num_partial))


	def run(self):
		while True:
			target = self.indexer.get_next_file()
			if not target:
				self.dump()
				print("Worker " + str(self.worker_id) + " died")
				break
			file_load = open(target)
			data = json.load(file_load)
			soup = BeautifulSoup(data["content"],features="lxml")
			doc_id = target[target.rfind('/')+1:-5]
			url = data['url']
			print("Worker " + str(self.worker_id) + " working on " + url)
			important = {'b' : [], 'h1' : [], 'h2' : [], 'h3' : [], 'title' : []}
			for key_words in important.keys():
				for i in soup.findAll(key_words):
					for word in word_tokenize(i.text):
						important[key_words].append(self.stemmer.stem(word))

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

			#counter(count,positionals)

			counter = dict()
			#We calculating tf_raw, and positionals here
			for i in range(len(tokens)):
				word = tokens[i]
				if word in counter:
					counter[word][0] = counter[word][0] + 1
					counter[word][1].append(i)
				else:
					counter[word] = [1,list()]
					counter[word][1].append(i)

			doc_length = len(tokens)
			for index in counter:
				if index in self.index:
					postings = self.index[index]
					postings.append(Posting(doc_id,url,counter[index][0]/doc_length,0,counter[index][1]))
				else:
					self.index[index] = list()
					self.index[index].append(Posting(doc_id,url,counter[index][0]/doc_length,0,counter[index][1]))
					self.index[index].sort(key=lambda y:y.doc_id)

			#10 Megabytes index (in Ram approx)
			if sys.getsizeof(self.index) > 500000:
				self.dump()





			
