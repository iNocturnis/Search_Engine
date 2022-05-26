#Posting class for indexer, will probably be more complex as we keep adding crap to it

class Posting():
	def __init__(self, url, rtf, position):
		self.url = url
		self.rtf = rtf
		self.tf = 0
		self.tfidf = 0
		self.positions = [position]