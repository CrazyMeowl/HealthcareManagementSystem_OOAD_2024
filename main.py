from flask import Flask, request, jsonify, render_template
import json
import random
import webbrowser
app = Flask(__name__)

def load_config():
	with open("config.json",'r',encoding='utf-8') as f:
		config = json.load(f)
		return config

app_config = load_config()

@app.route('/', methods=['GET'])
def main():

	return render_template('index.html',name = app_config['name'])


if __name__ == '__main__':
	webbrowser.open('http://127.0.0.1:5000/', new=2)
	app.run(debug=True)
