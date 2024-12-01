from flask import Flask, request, jsonify, render_template
import json
import webbrowser
from utils.password_utils import *
from utils.database_utils import *
from models.user import *
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
		# Load database
		le_data = load_data("users")
		if item_existed(phone_number,le_data):
			if verify_password(le_data[phone_number]["password"],password):
				return "Logged In"
			else:
				return "Something ain't right"
		else:
			return "The phone number is not registered"
		
	# GET
	return render_template('login.html',name = app_config['name'])


@app.route('/register', methods=['GET','POST'])
def register():
	# POST
	if request.method == 'POST':
		phone_number=request.form['phone_number']
		new_user = User(
			full_name=request.form['full_name'],
			phone_number=request.form['phone_number'],
			email=request.form['email'],
			gender = request.form['gender'],
			date_of_birth = request.form['date_of_birth'],
			ssn = request.form['ssn'],
			password = str(hash_password(request.form['password']))
			)
		# Load database
		le_data = load_data("users")

		
		if item_existed(phone_number,le_data):
			# phone number used
			return "Not so fast"
		else:
			# add new user
			le_data[phone_number] = new_user.__dict__
			save_data("users",le_data)

			return "Nicely done"
	# GET 
	return render_template('register.html',name = app_config['name'])



if __name__ == '__main__':
	webbrowser.open('http://127.0.0.1:5000/', new=2)
	app.run(debug=True)
