#Data input
import json
import os
import shelve
from bs4 import BeautifulSoup
from time import perf_counter
import time
import threading
import pickle


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
        self.stemmer = PorterStemmer()
        p = os.path.dirname(os.path.abspath(__file__))
        my_filename = os.path.join(p, "urlID.pkl")
        self.f = open(my_filename, "rb+")
        self.id = pickle.load(self.f)

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
    
    # looks for the smallest list and largest list
    def find_extremes(self, q):
        longest = float('-inf')
        shortest = float('inf')
        remaining = []
        # Careful if there is a word that the indexer doesn't have
        for word in q:
            d = self.get_save_file(word)
            if len(d[word]) > longest:
                longest = len(d[word])
                l = word  
            elif len(d[word]) < shortest:
                shortest = len(d[word])
                s = word
        for word in q:
            if word != l or word != s:
                remaining.append(word)
        return s, l, remaining
    
    def merge(self, short, long, r):
        m = []
        i = 0
        j = 0
        s = self.get_save_file(short)
        l = self.get_save_file(long)
        while i < len(s[short]) or j < len(l[long]):
            if i == len(d[short])-1:
                if s[short][i].url == l[long][j].url:
                    m.append(s[short][i].url)
                    j += 1
                elif s[short][i].url < l[long][j].url:
                    break
                else:
                    j += 1
            else:
                if s[short][i].url == l[long][j].url:
                    m.append(d[short][i].url)
                    i += 1
                    j += 1
                elif s[short][i].url < l[long][j].url:
                    break
                else:
                    i += 1
                    j += 1
        
        final = []
        if len(m) > 0:
            while len(r) > 0:
                d = self.get_save_file(r[0])
                for i in d[r[0]]:
                    if i.url > m[len(m) -1]:
                        break
                    elif i.url in m:
                        final.append(i.url)
                if len(final) != len(m):
                    m = final
                    final = []
                    r.pop(0)
                else:
                    final = []
                    r.pop(0)
                        
            return m
        else:
            return -1

    def search(self):
        query = input("Enter query: ")
        query = [self.stemmer.stem(i) for i in query.split()]
        x = self.find_extremes(query)
        match = self.merge(x[0], x[1], x[2])
        if match == -1:
            print("No valid matches")
        else:
            for i in match:
                print(self.id[i])








