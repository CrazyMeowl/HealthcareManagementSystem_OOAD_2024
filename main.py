from flask import Flask, request, jsonify, render_template
import json
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

@app.route('/login', methods=['GET','POST'])
def login():
	# POST
	if request.method == 'POST':
		phone_number = request.form['phone_number']
		password = request.form['password']
		return f"Phone Number: {phone_number}, Password: {password}"
	# GET
	return render_template('login.html',name = app_config['name'])


@app.route('/register', methods=['GET','POST'])
def register():
	# POST
	if request.method == 'POST':
		full_name = request.form['full_name']
		gender = request.form['gender']
		date_of_birth = request.form['date_of_birth']
		phone_number = request.form['phone_number']
		password = request.form['password']
		return f"Full Name: {full_name}, Phone Number: {phone_number}, Password: {password}, Gender: {gender}, Date Of Birth: {date_of_birth}"
	# GET 
	return render_template('register.html',name = app_config['name'])



if __name__ == '__main__':
	webbrowser.open('http://127.0.0.1:5000/', new=2)
	app.run(debug=True)
