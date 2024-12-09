from flask import Flask, request, jsonify, render_template, session, redirect
from flask_session import Session
from flask_apscheduler import APScheduler

import json
import webbrowser
import time
import os
from datetime import datetime, timedelta
from random import choice

from utils.password_utils import *
from utils.database_utils import *
from utils.qr_code_utils import * 
from utils.email_utils import *
from models.user_model import *
from models.apppointment_model import *

app = Flask(__name__)

 
app = Flask(__name__)
app.config["SCHEDULER_API_ENABLED"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = os.environ.get('SUPER_SECRET')

Session(app)
scheduler = APScheduler()
scheduler.init_app(app)


 
# Define the routine function
@scheduler.task('interval', id='send_remind_email', minutes=1)
def send_remind_email():
	# email_username = os.environ.get('SENDER_EMAIL_USERNAME')
	# email_password = os.environ.get('SENDER_EMAIL_PASSWORD')
	# html_content = "<h1>Your appointment is near<h1>"
	# qr_data = f"""/

	# """
	# send_email(email_username,email_password, "email", "Appointment Reminder", html_content, generate_qr_code_base64(qr_data))
	print('sending email')
	# print()

	

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
			return render_template('login.html',app_name = app_config['app_name'],phone_number=phone_number,message="Wrong Phone Number",message_type="danger")
		else:
			if not verify_password(le_data[phone_number]["password"],password):
				# WRONG PASSWORD
				return render_template('login.html',app_name = app_config['app_name'],phone_number=phone_number,message="Wrong Password",message_type="danger")
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
			return render_template('register.html',app_name = app_config['app_name'],message="Phone number is registered to another account",message_type="warning")
		elif query_existed('email',new_user.email,le_data):
			return render_template('register.html',app_name = app_config['app_name'],message="Email is registered to another account",message_type="warning")
		elif query_existed('ssn',new_user.ssn,le_data):
			return render_template('register.html',app_name = app_config['app_name'],message="SSN is registered to another account",message_type="warning")
		else:
			# SUCCESS
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

			# Change email 
			if (user_data['email'] != form_data['email']):
				replace_data('appointments.json',user_data['email'],form_data['email'])

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

			# Change phone number in appointments database
			replace_data('appointments',user_data['phone_number'],form_data['phone_number'])
			# Change email in appointments database
			if (user_data['email'] != form_data['email']):
				replace_data('appointments',user_data['email'],form_data['email'])

			for i in form_data:
				old_data[i]=form_data[i]
			le_data.pop(user_data['phone_number'])
			le_data[form_data['phone_number']]=old_data
			session['user_data']=old_data
			save_data("users",le_data)
			return  redirect('/profile')
		# If the new phone number is in use
		elif item_existed(form_data['phone_number'],le_data) and (form_data['phone_number'] != user_data['phone_number']):
			return render_template('user_profile.html',app_name = app_config['app_name'], user_data = session['user_data'],message="The Phone Number is currently in use",message_type="danger")

	return render_template('user_profile.html',app_name = app_config['app_name'], user_data = session['user_data'])

@app.route('/book_appointment', methods=['GET','POST'])
def book_appointment():
	if not session.get('user_data'):
		return redirect("/login")
	
	# POST
	if request.method == 'POST':
		# Load database
		le_data = load_data("appointments")
  
		if request.form['apt_type'] != "demand":
			apt_category = ""
		else:
			apt_category = request.form['apt_category']
   
   
		apt_number = 1
		for item_id in le_data:
			item  = le_data[item_id]
			if ( item['apt_type'] == request.form['apt_type'] ) and (item['apt_category'] == apt_category) and (item['apt_date'] == request.form['apt_date']) and (item['apt_session'] == request.form['apt_session']):
				apt_number +=1
  
		
		le_apt = Appointment(apt_type = request.form['apt_type'],
						apt_category = apt_category,
						apt_date = request.form['apt_date'],
						apt_session = request.form['apt_session'],
						apt_number = apt_number,
						customer_phone = session['user_data']['phone_number'],
						customer_email = session['user_data']['email'],
						status="pending",
						description="",
						rating=None,			
		)
		apt_id = len(le_data)+1
		le_data[f"{apt_id}"]=le_apt.__dict__
		save_data("appointments",le_data)

		html_content = "<h1>This email is to inform you that you booked an appointment throught our system <h1>"
		qr_data = f"""
Appointment Id : {apt_id}
{le_apt.to_qr_data()}
		"""
		send_email(le_apt.customer_email, "Appointment Accepted", html_content, generate_qr_code_base64(qr_data))
		print('sending email')


	
		return redirect('/home')
	
	min_date = datetime.today().strftime('%Y-%m-%d')
	max_date = (datetime.today() + timedelta(weeks=2)).strftime('%Y-%m-%d')
	return render_template('book_appointment.html', app_name = app_config['app_name'], user_data = session['user_data'], min_date = min_date, max_date = max_date)


@app.route('/api/get_availability/', methods=['GET'])
def get_availability():
	apt_type = request.args.get('apt_type')
	apt_date = request.args.get('apt_date')
	apt_category = request.args.get('apt_category')

	if apt_type != 'demand':
		apt_category = ""

	le_data = load_data("appointments")

	morning_count = 0
	afternoon_count = 0
	for i in le_data:
		if (le_data[i]['apt_date'] == apt_date) and (le_data[i]['apt_type'] == apt_type) and (le_data[i]['apt_category'] == apt_category):
			if le_data[i]['apt_session'] == 'morning':
				morning_count+=1
			else: 
				afternoon_count+=1

	availability = {
		'morning': morning_count < 10,
		'afternoon': afternoon_count < 10,
	}

	return jsonify(availability)
	
if __name__ == '__main__':
	scheduler.start()
	webbrowser.open('http://127.0.0.1:5000/', new=2)
	app.run(debug=False)
