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
from porter2stemmer import Porter2Stemmer

import re

save_1 = shelve.open("save_1.shelve")
save_2 = shelve.open("save_2.shelve")
save_3 = shelve.open("save_3.shelve")
save_4 = shelve.open("save_4.shelve")
save_5 = shelve.open("save_5.shelve")

key = list(save_1.keys())
print(key)