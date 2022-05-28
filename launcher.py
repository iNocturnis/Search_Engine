from indexer import Indexer
import time
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)
errors = list()
indexer = Indexer(list(),dict(),list())	
search = None

@app.route('/',methods=['POST','GET'])
def index():
	errors = list()
	if not indexer:
		errors.append("Error in creating indexer module")
	elif not indexer.load_index_index():
		errors.append("Indexer does not exists, please run it first")
	if not search:
		errors.append("Error in creating search module")

	if request.method == 'POST':
		if request.form.get('start-index') == "start":
			print("Making the indexer")
			indexer.create_index()
			return render_template('index.html',ips="Thanks for waiting you are ready to search.")
		if request.form.get('search_query') != "":
			search_query = request.form['search_query']
			result = [['lorem','ipsi'],['lores','dolores']]
			return render_template('index.html',results=result,errors=errors)
		return render_template('index.html',errors=errors)
	else:
		return render_template('index.html',errors=errors)

if __name__ == "__main__":
	app.run(debug=True)
	