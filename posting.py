#Posting class for indexer, will probably be more complex as we keep adding crap to it

class Posting():
	def __init__(self,url,tf_idf):
		self.url = url
		self.tf_idf = tf_idf
		
	def comparator(self):
		#Some custom comparator for sorting postings later
		pass