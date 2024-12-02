from flask import Flask, request, jsonify, render_template, session, redirect
from flask_session import Session
import json
import webbrowser
from utils.password_utils import *
from utils.database_utils import *
from models.user_model import *
import os
app = Flask(__name__)

 
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = os.environ.get('SUPER_SECRET')
Session(app)
 


def load_config():
	with open("config.json",'r',encoding='utf-8') as f:
		config = json.load(f)
		return config

app_config = load_config()

@app.route('/', methods=['GET'])
def main():
	if session.get("name"):
		return redirect("/home")
	return render_template('index.html',name = app_config['name'])

@app.route('/login', methods=['GET','POST'])
def login():
	# POST
	if request.method == 'POST':
		phone_number = request.form['phone_number']
		password = request.form['password']
		# Load database
		le_data = load_data("users")
		if not item_existed(phone_number,le_data):
			# Phone number not found
			return "Cannot find User"
		else:
			if not verify_password(le_data[phone_number]["password"],password):
				# WRONG PASSWORD
				return "Something ain't right"
			else:
				session['user_data']=le_data[phone_number]
				return f"Logged In as {session["user_data"]}"
				
	# if session.get("user_data"):
	# 	return redirect("/")
	# GET
	return render_template('login.html',name = app_config['name'])

@app.route('/logout', methods=['GET','POST'])
def logout():
	if session.pop("user_data",None):
		return redirect("/")
	
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
			password = str(hash_password(request.form['password'])),
			role = 'user'
			)
		# Load database
		le_data = load_data("users")

		
		if item_existed(phone_number,le_data):
			# phone number used
			return "This phone number is already in use. Please try another one."
		else:
			# add new user
			le_data[phone_number] = new_user.__dict__
			save_data("users",le_data)

			return "Nicely done"
	# GET 
	return render_template('register.html',name = app_config['name'])

#


if __name__ == '__main__':
	webbrowser.open('http://127.0.0.1:5000/', new=2)
	app.run(debug=True)
