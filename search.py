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

class Search():

    def __init__(self):
        self.save_1 = shelve.open("save_1.shelve")
        self.save_2 = shelve.open("save_2.shelve")
        self.save_3 = shelve.open("save_3.shelve")
        self.save_4 = shelve.open("save_4.shelve")
        self.save_5 = shelve.open("save_5.shelve")

    def get_save_file(self, word):
        word_lower = word.lower()

        if re.match(r"^[a-d0-1].*", word_lower):
            return self.save_1
        elif re.match(r"^[e-k2-3].*", word_lower):
            return self.save_2
        elif re.match(r"^[l-q4-7].*", word_lower):
            return self.save_3
        elif re.match(r"^[r-z8-9].*", word_lower):
            return self.save_4
        else:
            return self.save_5
    
    def get_userinput():
        return

    def get_tf_idf(self, words):
        try:
            tfidf = TfidfVectorizer(ngram_range=(1,3))

    def search(query):
        x = [query]
        
        file = self.get_save_file()






