import json
import os
import shelve
from bs4 import BeautifulSoup
from time import perf_counter
import requests

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import numpy as np
path_to_script = os.path.dirname(os.path.abspath(__file__))
my_filename = os.path.join(path_to_script, "testfile.json")
url = "https://www.crummy.com/software/BeautifulSoup/bs4/doc/"

req = requests.get(url)
file = open('D:/Visual Studio Workspace/CS121/assignment3/Search_Engine/testfile.json')
content = json.load(file)
soup = BeautifulSoup(content["content"], 'lxml')
bold = []
#print(soup.prettify())
print(soup.findAll('h3'))
for i in soup.findAll('title'):
    print(word_tokenize(i.text))
print(bold)




