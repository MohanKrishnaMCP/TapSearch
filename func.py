import nltk
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()

def last(n): 
    return n[1]


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
			print(word_inv_index[word])
			#sorted(word_inv_index[word], key=last, reverse=True)
			word_inv_index[word].sort(key=last, reverse=True)
			for i in range(len(word_inv_index[word])):
				print(len(word_inv_index[word]))
				index_val.append(word_inv_index[word][i][0])
	print(word_inv_index)
	return index_val
	# res = []
	# for i in range(len(index_val)):
	# 	res.append(doc_dict[index_val[i]])

	# return res