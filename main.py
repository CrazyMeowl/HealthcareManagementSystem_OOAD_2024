from flask import Flask, request, jsonify, render_template, session, redirect
from flask_session import Session
from flask_apscheduler import APScheduler

import json
import webbrowser
import time
import os

from utils.password_utils import *
from utils.database_utils import *
from models.user_model import *
app = Flask(__name__)

 
app = Flask(__name__)
app.config["SCHEDULER_API_ENABLED"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = os.environ.get('SUPER_SECRET')

scheduler = APScheduler()
scheduler.init_app(app)
Session(app)
 
# Define the routine function
@scheduler.task('interval', id='send_remind_email', minutes=1)
def send_remind_email():
	# print(f'{time.time()}')
	print("Sending Reminder Emails")

def load_config():
	with open("config.json",'r',encoding='utf-8') as f:
		config = json.load(f)
		return config

app_config = load_config()

@app.route('/', methods=['GET'])
def main():
	if session.get('user_data'):
		return redirect("/home")
	return render_template('index.html',app_name = app_config['app_name'])

@app.route('/login', methods=['GET','POST'])
def login():
	# if user logged in
	if session.get('user_data'):
		return redirect("/home")
	
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
				# return f"Logged In as {session['user_data']}"
				return redirect('/home')
				
	# if session.get("user_data"):
	# 	return redirect("/")
	# GET
	return render_template('login.html',app_name = app_config['app_name'])

@app.route('/logout', methods=['GET','POST'])
def logout():
	session.pop("user_data",None)
	return redirect("/")
	
@app.route('/register', methods=['GET','POST'])
def register():
	# if user logged in
	if session.get('user_data'):
		return redirect("/home")
	# POST
	if request.method == 'POST':
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

		
		if item_existed(new_user.phone_number,le_data):
			# phone number used
			return "This phone number is already in use. Please try another one."
		else:
			# add new user
			le_data[new_user.phone_number] = new_user.__dict__
			save_data("users",le_data)
			return redirect("/login")
			# return "Nicely done"
	# GET 
	return render_template('register.html',app_name = app_config['app_name'])

@app.route('/home', methods=['GET'])
def home():
	if not session.get('user_data'):
		return redirect("/login")
	return render_template('user_home.html',app_name = app_config['app_name'], user_data = session['user_data'])

@app.route('/profile', methods=['GET','POST'])
def profile():
	if not session.get('user_data'):
		return redirect("/login")
	
	# POST
	if request.method == 'POST':
		user_data = session.get('user_data')
		form_data = {
			'full_name':request.form['full_name'],
			'phone_number':request.form['phone_number'],
			'email':request.form['email'],
			'gender' : request.form['gender'],
			'date_of_birth' : request.form['date_of_birth'],
			'ssn' : request.form['ssn'],
			'height':request.form['height'],
			'weight':request.form['weight'],
			'blood_type':request.form['blood_type'],
			'role':'user'}
			
		# Load database
		le_data = load_data("users")

		# Not changing phone number
		if item_existed(form_data['phone_number'],le_data) and (form_data['phone_number'] == user_data['phone_number']):
			old_data = le_data[user_data['phone_number']]
			for i in form_data:
				old_data[i]=form_data[i]
			le_data[user_data['phone_number']]=old_data
			session['user_data']=old_data
			save_data("users",le_data)
			return  redirect('/profile')

		# If the new phone number isnt in use
		elif not item_existed(form_data['phone_number'],le_data) and (form_data['phone_number'] != user_data['phone_number']):
			old_data = le_data[user_data['phone_number']]
			for i in form_data:
				old_data[i]=form_data[i]
			le_data.pop(user_data['phone_number'])
			le_data[form_data['phone_number']]=old_data
			session['user_data']=old_data
			save_data("users",le_data)
			return  redirect('/profile')
		# If the new phone number is in use
		elif item_existed(form_data['phone_number'],le_data) and (form_data['phone_number'] != user_data['phone_number']):
			return "The phone number is in use"
		# if item_existed(form_data['phone_number'],le_data):
		# 	# phone number used
		# 	return "This phone number is already in use. Please try another one."
		# else:
		# 	# add new user
		# 	le_data[new_user.phone_number] = new_user.__dict__
		# 	save_data("users",le_data)
		# 	return redirect("/login")
			# return "Nicely done"
	return render_template('user_profile.html',app_name = app_config['app_name'], user_data = session['user_data'])


if __name__ == '__main__':
	scheduler.start()
	webbrowser.open('http://127.0.0.1:5000/', new=2)
	app.run(debug=True)
