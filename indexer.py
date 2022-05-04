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


#Data process
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

import re


class Indexer():
	def __init__(self,restart,trimming):
		#Config stuffs
		self.path = "data/DEV/"
		self.restart = restart
		self.trimming = trimming
		self.stemmer = PorterStemmer()
		self.vectorizer = TfidfVectorizer(lowercase=True,ngram_range = (1,3))

		#Shelves for index
		#https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html
		#https://www.irishtimes.com/news/science/how-many-numbers-begin-with-a-1-more-than-30-per-cent-1.4162466
		#According to this will be how we split things
		#Save #1 = ABCD + (1) ~ 18.3% of words
		#Save #2 = EFGHIJK + (2-3)~ 27.1% of words
		#Save #3 = LMNOPQ + (4-7) ~ 25.4% of words
		#Save #4 = RSTUVWXYZ + (8-9)~ 29.2% of words
		#Save #5 = Numbers ???
		if os.path.exists("save_1.shelve") and restart:
			os.remove("save_1.shelve")
		if os.path.exists("save_2.shelve") and restart:
			os.remove("save_2.shelve")
		if os.path.exists("save_3.shelve") and restart:
			os.remove("save_3.shelve")
		if os.path.exists("save_4.shelve") and restart:
			os.remove("save_4.shelve")


		self.save_1 = shelve.open("save_1.shelve")
		self.save_2 = shelve.open("save_2.shelve")
		self.save_3 = shelve.open("save_3.shelve")
		self.save_4 = shelve.open("save_4.shelve")


	def save_index(self,word,posting):
		wordhash = hash(word)	##Honestly do not know why hashing is even needed, might cause more problems 
		cur_save = get_save(word)
		shelve_list = list()

		if wordhash not in cur_save:
			shelve_list.append(posting)
			cur_save[wordhash] = shelve_list
			cur_save.sync()
		else:
			shelve_list = cur_save[wordhash]
			shelve_list.append(posting)
			shelve_list.sort(key=lambda x: x.tf_idf, reverse = True)
			cur_save.sync()

	def get_save_file(self,word):
		#return the correct save depending on the starting letter of word
		word_lower = word.lower()

		if re.match(r"^[a-d1-1].*",word_lower):
			return self.save_1
		elif re.match(r"^[e-k2-3].*",word_lower):
			return self.save_2
		elif re.match(r"^[l-q4-7].*",word_lower):
			return self.save_3
		elif re.match(r"^[r-z8-9].*",word_lower):
			return self.save_4
		else:
			print("You have somehow went beyond the magic")
			return None

	def get_tf_idf(self,words,word):
		#tf_idf
		#words = whole text
		#word the word we finding the score for
		#return the score
		pass


	def get_data(self):
		for directory in os.listdir(self.path):
			for file in os.listdir(self.path + "/" + directory + "/"):
				#Actual files here
				#JSON["url"] = url of crawled page, ignore fragments
				#JSON["content"] = actual HTML
				#JSON["encoding"] = ENCODING
				file_load = open(self.path + "/" + directory + "/"+file)
				data = json.load(file_load)
				soup = BeautifulSoup(data["content"],from_encoding=data["encoding"])
				words = word_tokenize(soup.get_text())
				tokenized_words = list()
				stemmed_words = list()
				for word in words:
					if word != "" and word.isalnum():
						#So all the tokenized words are here,
						tokenized_words.append(word)
				#YOUR CODE HERE
				print(tokenized_words)

				for word in tokenized_words:
					stemmed_words.append(self.stemmer.stem(word))

					print(X)
					#stemming,
					#tf_idf
					#get_tf_idf(stemmed_words,word)
					#post = Posting()

				print(stemmed_words)
				#
				exit(1)


				




def main():
	indexer = Indexer(True,0)
	indexer.get_data()

if __name__ == "__main__":
	main()