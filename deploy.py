from flask import flask

app = Flask(__name__)

@app.route('')
def index():
	return '<h1>Deployed</h1>'