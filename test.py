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
