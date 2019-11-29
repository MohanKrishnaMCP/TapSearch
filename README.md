# TapSearch
TapSearch is a word search-engine. It splits the document by paragraphs and returns top 10 match of paragraph when a word is search.

------------------------------------------------------------

Installation:
------------
+ Install python 3 and pip
+ Clone repo and cd to the folder
+ Install requirements using: `pip install -r requirements.txt` in the cmd
+ Run `Python deploy.py` in the cmd (will not run in python IDLE, custom modules are used)
+ Enter the displayed url in the browser. url will be similar to `http://127.0.0.1:5000/`

Instruction:
------------
+ Enter the document in the text area and Index.
+ Search the indexed document.
+ Top 10 results will show up.
+ Clear the document and add new document are present in menu.

Features:
---------
+ Each word in the document is stemmed. Stemming is done to increace the relevancy of the search.
+ Each stemmed word is invert indexed to make search fast and its frequency is also counted to return the top searched.
+ Search is dynamic and multiple documents can be added.

Tech Used:
----------
+ HTML, CSS, Bootstrap for frontend development.
+ Flask python for backend development.
