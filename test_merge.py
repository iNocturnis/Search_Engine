import json
from posting import Posting
import math
import sys
import random
from nltk.corpus import words
random_list = [1,2,3,4,5,6,7,8,9,10]


test_data = words.words()
random.shuffle(test_data)


def random_posting(id):
	return Posting(id,random.choice(random_list),random.choice(random_list),[random.choice(random_list),random.choice(random_list),random.choice(random_list),random.choice(random_list),
	random.choice(random_list),random.choice(random_list),random.choice(random_list),random.choice(random_list)])

class Node():
	index_value = 'Something'
	postings = list()

class Index():
	length = 0
	index = list()

def random_partial_index(name):
	part_index = Index()
	part_index.index = list()
	part_index.length = 0
	with open(name +'.partial', 'w') as f:
		for i in range(1000):

			node1 = Node()
			node1.index_value = random.choice(test_data).lower()
			node1.postings = list()
			for i in range(10):
				node1.postings.append(random_posting(i))

			jsonStr = json.dumps(node1, default=lambda o: o.__dict__,sort_keys=False)
			
			part_index.index.append((node1.index_value,f.tell()))
			f.write(jsonStr + '\n')
			part_index.length = part_index.length + 1

	part_index.index.sort(key=lambda y:y[0])
	jsonStr =json.dumps(part_index, default=lambda o: o.__dict__,sort_keys=False)
	with open(name + '.index','w') as f:
		f.write(jsonStr)

def merge(partial_indices):
	partial_files = list()
	partial_index_files = list()
	parital_index_indices = list()
	merged_index = open("merged_index.full",'w')
	num_indices = len(partial_indices)

	#Full Index.Index and Length
	full_index = Index()
	full_index.index = list()
	full_index.length = 0

	for partial_index in partial_indices:
		file = open(partial_index+'.partial','r')
		partial_files.append(file)
		index = open(partial_index+'.index','r')
		partial_index_files.append(index)

	for partial_index_file in partial_index_files:
		partial_index_file.seek(0,0)
		parital_index_indices.append(json.loads(partial_index_file.readline()))

	#Start all indexes at 0
	for partial_file in partial_files:
		partial_file.seek(0,0)

	pointers = [0]*num_indices

	while(True):

		#Get all values from all indices to find min
		value = None
		values = list()
		for i in range(num_indices):
			if pointers[i] < parital_index_indices[i]['length']:
				values.append(parital_index_indices[i]['index'][pointers[i]][0])
			
		if(len(values) == 0):
			break
		value = min(values)

		#Get data from the min value of all indices if exists then save to mergedIndex
		if value == None:
			print("I have crashed some how by not getting min value")
			break

		node = Node()
		node.index_value = value
		for i in range(num_indices):
			if pointers[i] < parital_index_indices[i]['length'] and parital_index_indices[i]['index'][pointers[i]][0] == value:
				to_seek = parital_index_indices[i]['index'][pointers[i]][1]
				partial_files[i].seek(to_seek,0)
				json_value = partial_files[i].readline()
				temp_node = json.loads(json_value)
				node.postings = node.postings + temp_node['postings']
				pointers[i] = pointers[i] + 1
		
		node.postings.sort(key=lambda y:y['doc_id'])
		full_index.index.append((value,merged_index.tell()))
		full_index.length = full_index.length + 1
		jsonStr = json.dumps(node,default=lambda o: o.__dict__,sort_keys=False)
		merged_index.write(jsonStr + '\n')

	full_index.index.sort(key=lambda y:y[0])
	jsonStr =json.dumps(full_index, default=lambda o: o.__dict__,sort_keys=False)
	with open("merged_index.index" ,'w') as f:
		f.write(jsonStr)
