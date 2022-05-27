import math
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

class Posting():
	def __init__(self, url, rtf, position):
		self.url = url
		self.rtf = rtf
		self.tf = 1
		self.tfidf = 0
		self.positions = [position]


d = {
    'a' : [Posting(0, 1, 1), Posting(2, 1, 1), Posting(3, 1, 1), Posting(8, 1, 1)], 
    'b' :[Posting(0, 1, 1), Posting(8, 1, 1)],
    'c' : [Posting(0, 1, 1), Posting(1, 1, 1), Posting(2, 1, 1), Posting(8, 1, 1)]
    }

def get_index(word):
    for k, v in d.items():
        if k == word:
            return v

# takes a list of posting lists returns a list of indexes that correspond to search temp list
def two_shortest(l_posting):
    short = []
    location = []
    for postings in l_posting:
        short.append(len(postings))
    
    for i in range(2):
        x = short.index(min(short))
        location.append(x)
        short[x] = float('inf')
    
    return location

# len(list1) <= len(list2) So the code in this function works with that in mind
def merge(list1, list2):
    merged = []
    i = 0
    j = 0
    # TODO: optimize by having a pointer to the current index+4
    while i < len(list1) or j < len(list2):
        if j == len(list2):
            break
        if i == len(list1):
            break
        # Since list1 is shorter it will hit its max index sooner, 
        #   so in the cases were it does we still need to go through list2 to see if the last element of list1 appears anywhere in the rest of list2
        if i == len(list1)-1:
            if list1[i].url == list2[j].url:
                merged.append(list1[i])
                j += 1
                i += 1
            elif list1[i].url < list2[j].url:
                break
            else:
                j += 1
        else:
            if list1[i].url == list2[j].url:
                merged.append(list1[i])
                i += 1
                j += 1
            elif list1[i].url < list2[j].url:
                break
            else:
                i += 1
                j += 1
    return merged, 

# query is a list of stemmed tokens, returns a list of postings (which we'll directly ignore except for the doc id)
def search(query):
    temp = []
    for token in query:
        temp.append(get_index(token))
    
    l = two_shortest(temp)
    m = merge(temp[l[0]], temp[l[1]])

    while len(temp) > 1:
        # delete from temp the already merged lists
        del temp[l[0]]
        del temp[l[1]]
        temp.append(m)

        l = two_shortest(temp)
        m = merge(temp[l[0]], temp[l[1]])

    for p in m:
        print(p.url)
    
    # For now going to do a loop through each query's index and match it with the merged list (can be faster if i implement something during merge/search in order to keep track of the postings)
    
    



search(["a", "b", "c"])
            
