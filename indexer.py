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



#Data process
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np

import re

#Logging postings
from posting import Posting


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
		self.save_2 = shelve.open("save_2.shelve")
		self.save_3 = shelve.open("save_3.shelve")
		self.save_4 = shelve.open("save_4.shelve")
		self.save_5 = shelve.open("save_5.shelve")


	def save_index(self,word,posting):
		cur_save = self.get_save_file(word)
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
		except:
			shelve_list.append(posting)
			cur_save[word] = shelve_list
			cur_save.sync()

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

	# retuns a dict of words/n-grams with their assosiated tf-idf score *can also return just a single score or a pandas dataframe
	# https://stackoverflow.com/questions/34449127/sklearn-tfidf-transformer-how-to-get-tf-idf-values-of-given-words-in-documen
	def get_tf_idf(self,words,word):
		#tf_idf
		#words = whole text
		#word the word we finding the score for
		#return the score
		try:
			tfidf = TfidfVectorizer(ngram_range=(1,3)) # ngram_range is range of n-values for different n-grams to be extracted (1,3) gets unigrams, bigrams, trigrams
			tfidf_matrix = tfidf.fit_transform(words)  # fit trains the model, transform creates matrix
			df = pd.DataFrame(tfidf_matrix.toarray(), columns = tfidf.get_feature_names_out()) # store value of matrix to associated word/n-gram
			#return(df.iloc[0][''.join(word)]) #used for finding single word in dataset
			data = df.to_dict() # transform dataframe to dict *could be expensive the larger the data gets, tested on ~1000 word doc and took 0.002 secs to run
			return data			# returns the dict of words/n-grams with tf-idf
			#print(df)			# debugging 
		except: 		
			print("Error in tf_idf!")
			return


	def get_data(self):
		for directory in os.listdir(self.path):
			for file in os.listdir(self.path + "/" + directory + "/"):
				#Actual files here
				#JSON["url"] = url of crawled page, ignore fragments
				#JSON["content"] = actual HTML
				#JSON["encoding"] = ENCODING
				ticker = perf_counter()
				tic = perf_counter()
				file_load = open(self.path + "/" + directory + "/"+file)
				data = json.load(file_load)
				soup = BeautifulSoup(data["content"],from_encoding=data["encoding"])
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
					stemmed_words.append(self.stemmer.stem(word))
					#stemming,
					#tf_idf
					#get_tf_idf(stemmed_words,word)
					#post = Posting()
				toc = perf_counter()
				if toc - tic > 1 :
					print("Took " + str(toc - tic) + "seconds to stemmed text !")

				for word in stemmed_words:
					#posting = Posting(data["url"],self.get_tf_idf(list(' '.join(stemmed_words)),word))
					tic = perf_counter()
					posting = Posting(data["url"],self.tf_idf_raw(stemmed_words,word))
					toc = perf_counter()
					if toc - tic > 1 :
						print("Took " + str(toc - tic) + "seconds to tf_idf text !")

					tic = perf_counter()
					self.save_index(word,posting)
					toc = perf_counter()
					if toc - tic > 1 :
						print("Took " + str(toc - tic) + "seconds to save text !")

				tocker = perf_counter()
				print("Finished " + data['url'] + " in \t " + str(tocker-ticker))

	def tf_idf_raw(self,words,word):
		tf_times = words.count(word)

		tf = tf_times/len(words)

		return tf

		



				




def main():
	indexer = Indexer(True,0)
	indexer.get_data()

if __name__ == "__main__":
	main()