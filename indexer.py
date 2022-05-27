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
	def __init__(self,restart):
		#Config stuffs
		self.path = "data/DEV/"
		self.restart = restart
	
	def get_data(self):
		num_threads = 1
		threads = list()

		for directory in os.listdir(self.path):
			for file in os.listdir(self.path + "/" + directory + "/"):
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