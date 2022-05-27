#Posting class for indexer, will probably be more complex as we keep adding crap to it

class Posting():
	def __init__(self,doc_id,url,tf_raw,tf_idf,positionals):
		self.doc_id = doc_id
		self.url = url
		self.tf_raw = tf_raw
		self.tf_idf = tf_idf
		self.positionals = positionals
	def __repr__(self):
		return "Doc_id:" + str(self.doc_id) + " URL:" + self.url + " tf_raw:" + str(self.tf_raw) + " tf_idf:" + str(self.tf_idf) + " positionals:" + str(self.positionals)
	def __str__(self):
		return "Doc_id:" + str(self.doc_id) + " URL:" + self.url + " tf_raw:" + str(self.tf_raw) + " tf_idf:" + str(self.tf_idf) + " positionals:" + str(self.positionals)

	def comparator(self):
		#Some custom comparator for sorting postings later
		pass