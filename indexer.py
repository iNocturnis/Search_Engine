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
from threading import Lock
import math


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
from worker_weight import Worker_Weight

class Node():
	index_value = ''
	postings = list()

class Index():
	length = 0
	index = list()

class Indexer():
	def __init__(self,list_partials,weight,data_paths,worker_factory=Worker,worker_weight_factory=Worker_Weight):
		#Config stuffs
		self.path = "data/DEV"
		self.num_doc = 0
		self.list_partials = list_partials
		self.weight = weight
		self.data_paths = data_paths
		self.stemmer = PorterStemmer()
		self.data_paths_lock = Lock()
		self.list_partials_lock = Lock()
		self.workers = list()
		
		self.worker_factory = worker_factory

		self.weight_workers = list()
		self.worker_weight_factory = worker_weight_factory

	def start_async(self):
		self.workers = [
			self.worker_factory(worker_id,self)
			for worker_id in range(8)]
		for worker in self.workers:
			worker.start()

	def start(self):
		self.start_async()
		self.join()

	def join(self):
		for worker in self.workers:
			worker.join()


	def get_postings(self,index):
		merged_index_index = open("merged_index.index" ,'r')
		merged_index = open("merged_index.full",'r')
		merged_index_index.seek(0,0)
		json_value = merged_index_index.readline()
		data = json.loads(json_value)
		index_index = dict(data['index'])
		to_seek = index_index[index]
		merged_index.seek(to_seek,0)
		json_value = merged_index.readline()
		data = json.loads(json_value)
		return data['postings']

	def set_weight(self):
		weight_file = open('docs.weight','w')
		jsonStr =json.dumps(self.weight, default=lambda o: o.__dict__,sort_keys=False)
		weight_file.write(jsonStr)
		weight_file.close()

	def get_weight(self,doc_id):
		weight = open('docs.weight','r')
		weight.seek(0,0)
		json_value = weight.readline()
		data = json.loads(json_value)
		return data[doc_id]

	def get_data_path(self):
		for directory in os.listdir(self.path):
			for file in os.listdir(self.path + "/" + directory + "/"):
				self.data_paths.append("data/DEV/" + directory + "/"+file)
		self.num_doc = len(self.data_paths)

	def get_next_file(self):
		self.data_paths_lock.acquire()
		try:
			holder = self.data_paths.pop()
			self.data_paths_lock.release()
			return holder
		except IndexError:
			self.data_paths_lock.release()
			return None
	
	def add_partial_index(self,partial_index):
		self.list_partials_lock.acquire()
		self.list_partials.append(partial_index)
		self.list_partials_lock.release()

	#Found 55770 documents
	#
	#getting important tokens

	def merge(self):
		partial_files = list()
		partial_index_files = list()
		parital_index_indices = list()
		
		num_indices = len(self.list_partials)

		#Full Index.Index and Length
		full_index = Index()
		full_index.index = list()
		full_index.length = 0

		for partial_index in self.list_partials:
			file = open("temp/" + partial_index+'.partial','r')
			partial_files.append(file)
			index = open("temp/" + partial_index+'.index','r')
			partial_index_files.append(index)

		for partial_index_file in partial_index_files:
			partial_index_file.seek(0,0)
			parital_index_indices.append(json.loads(partial_index_file.readline()))

		#Start all indexes at 0
		for partial_file in partial_files:
			partial_file.seek(0,0)

		pointers = [0]*num_indices
		merged_index = open("merged_index.full",'w')
		merged_index_index = open("merged_index.index" ,'w')

		while(True):

			#Get all values from all indices to find min
			value = None
			values = list()
			for i in range(num_indices):
				if pointers[i] < parital_index_indices[i]['length']:
					values.append(parital_index_indices[i]['index'][pointers[i]][0])
				
			if(len(values) == 0):
				break
			value = min(values)

			#Get data from the min value of all indices if exists then save to mergedIndex
			if value == None:
				print("I have crashed some how by not getting min value")
				break

			node = Node()
			node.index_value = value
			for i in range(num_indices):
				if pointers[i] < parital_index_indices[i]['length'] and parital_index_indices[i]['index'][pointers[i]][0] == value:
					to_seek = parital_index_indices[i]['index'][pointers[i]][1]
					partial_files[i].seek(to_seek,0)
					json_value = partial_files[i].readline()
					temp_node = json.loads(json_value)
					node.postings = node.postings + temp_node['postings']
					pointers[i] = pointers[i] + 1
			#Change postings here with tf*idf idf = log (n/df(t)) 
			node.postings.sort(key=lambda y:y['doc_id'])
			for posting in node.postings:
				posting['tf_idf'] = posting['tf_raw']*math.log(self.num_doc/len(node.postings))
			full_index.index.append((value,merged_index.tell()))
			full_index.length = full_index.length + 1
			jsonStr = json.dumps(node,default=lambda o: o.__dict__,sort_keys=False)
			merged_index.write(jsonStr + '\n')

		full_index.index.sort(key=lambda y:y[0])
		jsonStr =json.dumps(full_index, default=lambda o: o.__dict__,sort_keys=False)
		merged_index_index.write(jsonStr)

		for partial_index in self.list_partials:
			os.remove("temp/" + partial_index+'.partial')
			os.remove("temp/" + partial_index+'.index')

		merged_index_index.close()
		merged_index.close()


def main():
	indexer = Indexer(list(),dict(),list())
	indexer.get_data_path()
	print("We have " + str(len(indexer.data_paths)) + " documents to go through !" )
	indexer.start()
	indexer.merge()
	print("Finished merging into 1 big happy family")
	indexer.set_weight()

	tic = time.perf_counter()
	indexer.get_postings('artifici')
	toc = time.perf_counter()
	print(f"Took {toc - tic:0.4f} seconds to get postings for artifici")
	tic = time.perf_counter()
	indexer.get_weight('00ba3af6a00b7cfb4928e5d234342c5dc46b4e31714d4a8f315a2dd4d8e49860')
	print(f"Took {toc - tic:0.4f} seconds to get weight for some random page ")
	toc = time.perf_counter()

	


if __name__ == "__main__":
	main()