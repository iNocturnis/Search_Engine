from indexer import Indexer
import time
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)
def main():
	indexer = Indexer(False,list(),dict(),list())		
	indexer.load_index_index()
	search = Search()


@app.route('/',methods=['POST','GET'])
def index():
	if request.method == 'POST':
		if request.form.get('start-index') == "start":
			print("make the indexer")
			return render_template('index.html',ips="Thanks for waiting you are ready to search.")
		if request.form.get('search_query') != "":
			search = request.form['search_query']
			result = [['lorem','ipsi'],['lores','dolores']]
			return render_template('index.html',results=result)
		return render_template('index.html')
	else:
		return render_template('index.html')


if __name__ == "__main__":
	app.run(debug=True)
	main()