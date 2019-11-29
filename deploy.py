from flask import Flask, redirect, url_for, render_template, request, session
import nltk
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()

doc_dict = {}
#word_dict = {}


def clear(doc):
	clear_doc = ''
	extras = [',', '.', '-', ';', ':']

	for word in doc:
		if word in extras:
			continue
		else:
			clear_doc += word

	return clear_doc


def compress(cnt):
	cnt = list(cnt)
	return sorted([(i, cnt.count(i)) for i in cnt])


def indexer(full_doc):
	# i = 0
	# doc_dict[i] = []
	if not bool(doc_dict):
		i = 0
	else:
		i = max(doc_dict) + 1
	doc_dict[i] = []
	full_doc = full_doc.split('\n')
	#print(full_doc)
	for j in range(len(full_doc)):
		if full_doc[j] == '\r' and full_doc[j+1] == '\r':
			i += 1
			doc_dict[i] = []
		else:
			doc_dict[i].append(full_doc[j])

	return doc_dict


def invert_indexer(doc_dict):
	word_dict = {}
	for i in range(len(doc_dict.keys())):
		#i += 1
		#i = str(i)
		#print(doc_dict)
		for j in range(len(doc_dict[i])):
			#print(doc_dict[i][j])
			words = clear(doc_dict[i][j]).split()
			#print(words)
			for word in words:
				word = word.lower()
				word = stemmer.stem(word)
				if word not in word_dict:
					word_dict[word] = []
					word_dict[word].append(i)
				else:
					word_dict[word].append(i)

	return(word_dict)


def search_res(search, word_inv_index):
	search = search.lower()
	search = stemmer.stem(search)
	index_val = []

	for word in word_inv_index:
		if word == search:
			for i in range(len(word_inv_index[word])):
				sorted(word_inv_index[word], key=lambda x: x[1], reverse=True)
				index_val.append(word_inv_index[word][i][0])

	return index_val
	# res = []
	# for i in range(len(index_val)):
	# 	res.append(doc_dict[index_val[i]])

	# return res



app = Flask(__name__)
app.secret_key = "TapChief"

@app.route("/", methods=["POST", "GET"])
def index():
	
	if request.method == "POST":
		if bool(request.form["content"]):
			contents = request.form["content"]
			doc_dict = indexer(contents)
			session["doc"] = doc_dict
			#word_dict = invert_indexer(doc_dict)
			#word_dict = invert_indexer(doc_dict)
			#return f"{doc_dict}"
			return redirect(url_for("search_page",))

	return render_template("inputpage.html")

@app.route("/search_page", methods=["POST", "GET"])
def search_page():
	if "doc" in session:
		doc_dict = session["doc"]
		doc_dict = {int(k):[str(i) for i in v] for k,v in doc_dict.items()}
		print(doc_dict)
		word_dict = invert_indexer(doc_dict)
		word_list = list(word_dict)
		word_list.sort()
		word_inv_index = {}

		for word in word_list:
			freq = list(set(compress(word_dict[word])))
			word_inv_index[word] = freq 

		if request.method == "POST":
			if bool(request.form["search"]):
				search = request.form["search"]
				index_val = search_res(search, word_inv_index)
				res = []
				for i in range(len(index_val)):
					res.append(doc_dict[index_val[i]])
				print(res)
				return render_template("seachpage.html", res=res, doc_dict=doc_dict, word_dict=word_dict)

			if bool(request.form["clear"]):
				doc_dict = doc_dict.clear()
				return redirect(url_for("index"))

			# if bool(request.form["add_doc"]):
			# 	return redirect(url_for("index"))

		return render_template("seachpage.html")

	else:
		return redirect(url_for("index"))

if __name__ == "__main__":
	app.run(debug=True)