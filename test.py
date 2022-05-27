from threading import Thread
import json
import os
import shelve
import sys
from bs4 import BeautifulSoup
from time import perf_counter
from nltk.stem import PorterStemmer
import nltk
import time
from posting import Posting

import re

self_index = dict()
stemmer = PorterStemmer()
target = 'data/DEV/aiclub_ics_uci_edu/8ef6d99d9f9264fc84514cdd2e680d35843785310331e1db4bbd06dd2b8eda9b.json'
file_load = open(target)
data = json.load(file_load)
doc_id = target[target.rfind('/')+1:-5]
url = data['url']
soup = BeautifulSoup(data["content"],features="lxml")
# Gets a cleaner version text comparative to soup.get_text()
clean_text = ' '.join(soup.stripped_strings)
# Looks for large white space, tabbed space, and other forms of spacing and removes it
# Regex expression matches for space characters excluding a single space or words
clean_text = re.sub(r'\s[^ \w]', '', clean_text)
# Tokenizes text and joins it back into an entire string. Make sure it is an entire string is essential for get_tf_idf to work as intended
clean_text = " ".join([i for i in clean_text.split() if i != "" and re.fullmatch('[A-Za-z0-9]+', i)])
# Stems tokenized text
clean_text = " ".join([stemmer.stem(i) for i in clean_text.split()])

tokens = nltk.word_tokenize(clean_text)

#counter(count,positionals)

counter = dict()
for i in range(len(tokens)):
	word = tokens[i]
	if word in counter:
		counter[word][0] = counter[word][0] + 1
		counter[word][1].append(i)
	else:
		counter[word] = [1,list()]
		counter[word][1].append(i)
print(counter)
doc_length = len(tokens)
for index in counter:
	if index in self_index:
		postings = self_index[index]
		postings.append(Posting(doc_id,url,counter[index][0]/doc_length,0,counter[index][1]))
	else:
		self_index[index] = list()
		self_index[index].append(Posting(doc_id,url,counter[index][0]/doc_length,0,counter[index][1]))

for index in self_index:
	print(index + str(self_index[index]) + '\n')

print("The size of the dictionary is {} bytes".format(sys.getsizeof(self_index)))