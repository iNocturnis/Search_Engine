from indexer import Indexer
from search import Search
import time
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

errors = None
indexer = None	
search = None
safe_guard = 1

def get_data():
	global indexer
	indexer = Indexer(list(),dict(),list())

	global search
	search = Search(indexer)

	global safe_guard
	safe_guard = 1

	global errors
	errors = list()
	if not indexer.load_index_index():
		errors.append("Index of index is missing, probably should run the indexer")
	if not indexer.load_weight_index():
		errors.append("Index of index is missing, probably should run the indexer")



@app.route('/',methods=['POST','GET'])
def index():
	global errors
	global search
	global indexer
	global safe_guard
	local_errors = errors

	if request.method == 'POST':
		if request.form.get('start-index') == "start":
			print("Making the indexer")
			if safe_guard == 5:
				safe_guard = 1
				indexer.create_index()
				indexer.load_index_index()
				return render_template('index.html',ips="Thanks for waiting you are ready to search.")
			safe_guard = safe_guard + 1
			return render_template('index.html',ips=str(safe_guard) + " DANGER ! PROCEED IF YOU ARE KNOWING WHAT YOU DOING, OTHERWISE STOP, INDEX MIGHT GET YEETED")
		if request.form.get('search_query') != "":
			search_query = request.form['search_query']
			result = search.search(search_query)
			safe_guard = 1
			errors = list()
			return render_template('index.html',results=result,errors=local_errors)
		safe_guard = 1
		errors = list()
		return render_template('index.html',errors=local_errors)
	else:
		safe_guard = 1
		errors = list()
		return render_template('index.html',errors=local_errors)

if __name__ == "__main__":
	get_data()
	
	app.run(debug=False)
		