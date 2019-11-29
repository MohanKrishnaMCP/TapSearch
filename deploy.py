from flask import Flask, redirect, url_for, render_template, request, session
import func


def del_doc():
	global doc_dict
	doc_dict = doc_dict.clear()
	doc_dict = {}

def indexer(full_doc):
	if not bool(doc_dict):
		i = 0
	else:
		i = max(doc_dict) + 1
	doc_dict[i] = []
	full_doc = full_doc.split('\n')
	for j in range(len(full_doc)):
		if full_doc[j] == '\r' and full_doc[j+1] == '\r':
			i += 1
			doc_dict[i] = []
		else:
			doc_dict[i].append(full_doc[j].replace('\r', ' <br> '))

	return doc_dict


doc_dict = {}

app = Flask(__name__)
app.secret_key = "TapChief"

@app.route("/", methods=["POST", "GET"])
def index():
	
	if request.method == "POST":
		if bool(request.form["content"]):
			contents = request.form["content"]
			doc_dict = indexer(contents)
			session["doc"] = doc_dict
			return redirect(url_for("search_page",))

	return render_template("inputpage.html")

@app.route("/search_page", methods=["POST", "GET"])
def search_page():
	if "doc" in session:
		doc_dict = session["doc"]
		doc_dict = {int(k):[str(i) for i in v] for k,v in doc_dict.items()}
		print(doc_dict)
		word_dict = func.invert_indexer(doc_dict)
		word_list = list(word_dict)
		word_list.sort()
		word_inv_index = {}

		for word in word_list:
			freq = list(set(func.compress(word_dict[word])))
			word_inv_index[word] = freq 

		if request.method == "POST":
			if bool(request.form["search"]):
				search = request.form["search"]
				index_val = func.search_res(search, word_inv_index)
				res = []
				# res = res.clear()
				for i in range(len(index_val)):
					res.append(doc_dict[index_val[i]])
				#res = [item.replace('\r', '\n') for item in res]
				print(res)
				if len(res) > 10:
					l = 10
				else:
					l = len(res)
				return render_template("seachpage.html", res=res, l=l)

			if bool(request.form["clear"]):
				del_doc()
				return redirect(url_for("index"))

			# if bool(request.form["add_doc"]):
			# 	return redirect(url_for("index"))

		return render_template("seachpage.html")

	else:
		return redirect(url_for("index"))

print(doc_dict)

if __name__ == "__main__":
	app.run(debug=True)