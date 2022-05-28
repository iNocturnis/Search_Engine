#Data input
import json
import os
import shelve
from bs4 import BeautifulSoup
from time import perf_counter
import time
import threading
import pickle
import sys
import math
import numpy as np

sys.path.append('D:/Visual Studio Workspace')

#Data process
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np

import re
from indexer import Indexer

#Logging postings
from posting import Posting
from worker import Worker
import indexer

class Search():
    # wrote the code for testing in the file searchtesting.py so many of the variables and function calls are wrong.
    def __init__(self, indexer):
        self.indexer = indexer
        self.indexer.load_index_index()
        self.indexer.load_weight_index()
        self.stemmer = PorterStemmer()

    # takes a list of posting lists returns a list of indexes of the querys with the two shortest postings list that corresponds to search temp list
    def two_shortest(self, l_posting):
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
    def merge(self, list1, list2):
        max = 0
        valid1 = []
        valid2 = []
        i = 0
        j = 0
        # TODO: optimize by having a pointer to the current index+4
        i4 = 3
        j4 = 3
        while i < len(list1) or j < len(list2):
            if j == len(list2):
                break
            if i == len(list1):
                break
            #if max == 40:
                #break
            try:
                if i == len(list1)-1:
                    if list1[i]['doc_id'] == list2[j]['doc_id']:
                        valid1.append(list1[i])
                        valid2.append(list2[j])
                        j += 1
                        j4 +=1
                        i += 1
                        i4 += 1
                        max += 1
                    elif  list1[i]['doc_id'] >= list2[j4]['doc_id']:
                        j = j4
                        j4 = j + 3
                    elif list1[i4]['doc_id'] < list2[j]['doc_id'] and i4 < len(list1):
                        i = i4
                        i4 = i + 3
                    elif list1[i]['doc_id'] < list2[j]['doc_id']:
                        i += 1
                        i4 += 1
                    elif list1[i]['doc_id'] > list2[j]['doc_id']:
                        j += 1
                        j4 += 1
                    else:
                        j += 1
                        j4 += 1

                else:
                    if list1[i]['doc_id'] == list2[j]['doc_id']:
                        valid1.append(list1[i])
                        valid2.append(list2[j])
                        j += 1
                        j4 +=1
                        i += 1
                        i4 += 1
                        max += 1
                    elif list1[i]['doc_id'] >= list2[j4]['doc_id'] and j4 < len(list2):
                        j = j4
                        j4 = j + 3
                        
                    elif list1[i4]['doc_id'] < list2[j]['doc_id'] and i4 < len(list1):
                        i = i4
                        i4 = i + 3
                    elif list1[i]['doc_id'] < list2[j]['doc_id']:
                        i += 1
                        i4 += 1
                    elif list1[i]['doc_id'] > list2[j]['doc_id']:
                        j += 1
                        j4 += 1
                    else:
                        j += 1
                        j4 +=1
                        i += 1
                        i4 += 1
            except:
                if i == len(list1)-1:
                    if list1[i]['doc_id'] == list2[j]['doc_id']:
                        valid1.append(list1[i])
                        valid2.append(list2[j])
                        j += 1
                        j4 +=1
                        i += 1
                        i4 += 1
                    elif list1[i]['doc_id'] < list2[j]['doc_id']:
                        i += 1
                        i4 += 1
                    elif list1[i]['doc_id'] > list2[j]['doc_id']:
                        j += 1
                        j4 += 1
                    else:
                        j += 1
                        j4 += 1
                else:
                    if list1[i]['doc_id'] == list2[j]['doc_id']:
                        valid1.append(list1[i])
                        valid2.append(list2[j])
                        j += 1
                        j4 +=1
                        i += 1
                        i4 += 1
                    elif list1[i]['doc_id'] < list2[j]['doc_id']:
                        i += 1
                        i4 += 1
                    elif list1[i]['doc_id'] > list2[j]['doc_id']:
                        j += 1
                        j4 += 1
                    else:
                        j += 1
                        j4 +=1
                        i += 1
                        i4 += 1
            # Since list1 is shorter it will hit its max index sooner, 
            #   so in the cases were it does we still need to go through list2 to see if the last element of list1 appears anywhere in the rest of list2
            
        return valid1, valid2
    
    # query is a list of stemmed tokens, returns a list of postings (which we'll directly ignore except for the doc id)
    def search(self, query):
        tokens = word_tokenize(query)
        stemmed_tokens = list()
        for token in tokens:
            token = self.stemmer.stem(token)
            stemmed_tokens.append(token)
        
        query_valid_postings = dict()
        temp = []
        for token in stemmed_tokens:
            temp.append(self.indexer.get_postings(token))
            query_valid_postings[token] = []

        tic = perf_counter()
        l = self.two_shortest(temp)
        m = self.merge(temp[l[0]], temp[l[1]])
        if len(m[0]) == 0:
            return -1
        # Keep track of the valid postings for each query as we do merge
        first = stemmed_tokens[l[0]]
        query_valid_postings[first] = m[0]
        query_valid_postings[stemmed_tokens[l[1]]] = m[1]
        toc = perf_counter()
        print("first merge", toc-tic)
        tic = perf_counter()
        while len(temp) > 1:
            # delete from temp the already merged lists
            temp.pop(l[0])
            # Try and except since temp length changes
            try:
                temp.pop(l[1])
            except:
                temp.pop(l[1]-1)

            temp.append(m[0])

            # Delete and append to query to make it consistent with temp
            stemmed_tokens.pop(l[0])
            try:
                stemmed_tokens.pop(l[1])
            except:
                stemmed_tokens.pop(l[1]-1)

            stemmed_tokens.append(None)
            
            l = self.two_shortest(temp)
            # Checks if contents in l are the same
            if len(set(l)) == 1:
                break
            else:
                m = self.merge(temp[l[0]], temp[l[1]])
                print(len(m[0]), len(m[1]))
                query_valid_postings[first] = m[0]
                query_valid_postings[stemmed_tokens[l[1]]] = m[1]
        toc = perf_counter()
        print("while loop", toc-tic)
        tic = perf_counter()
        # Create list of doc ids of correct merged postings for cross checking

        merge = []
        for posting in query_valid_postings[first]:
            merge.append(posting['doc_id'])
        

        # Cross checking each query's valid postings list with correct merged set which we donated as being first
        for token, postings in query_valid_postings.items():
            if token == first:
                continue
            else:
                print(token)
                for p in postings:
                    if p['doc_id'] not in merge:
                        postings.remove(p)
        
        toc = perf_counter()
        print(toc-tic)
        
        
        for token, postings in query_valid_postings.items():
            print(token, len(postings))
        
        
        tic = perf_counter()
        results = []
        
        for i in range(len(query_valid_postings[first])):
            q_denom = 0
            norm_q = []
            norm_d = []

            for q in query_valid_postings.keys():
                q_denom += (query_valid_postings[q][i]['tf_idf']/(1 + math.log(query_valid_postings[q][i]['tf_raw'])))**2
            q_denom = math.sqrt(q_denom)
    
            for q in query_valid_postings.keys():
                x = query_valid_postings[q][i]['tf_idf']/(1 + math.log(query_valid_postings[q][i]['tf_raw']))/q_denom
                norm_q.append(x)
                y = (1 + math.log(query_valid_postings[q][i]['tf_raw']))/self.indexer.get_weight(query_valid_postings[q][i]['doc_id'])
                norm_d.append(y)
            results.append({'url' :query_valid_postings[first][i]['url'], 'cosine' : np.dot(norm_q, norm_d)})
        
        results = sorted(results, key = lambda x: x['cosine'], reverse = True)
        finalresults = []
        for i in range(20):
            finalresults.append(results[i]['url'])
        print(finalresults)
        return finalresults
    






