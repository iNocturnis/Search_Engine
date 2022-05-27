#Posting class for indexer, will probably be more complex as we keep adding crap to it

class Posting():
	def __init__(self,doc_id,tf_raw,tf_idf,positionals):
		self.doc_id = doc_id
		self.tf_raw = tf_raw
		self.tf_idf = tf_idf
		self.positionals = positionals

	def comparator(self):
		#Some custom comparator for sorting postings later
		pass