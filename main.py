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
from utils.date_utils import *
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
	reminded_list = load_data("reminded")
	apt_list = load_data("appointments")

	for apt_id in apt_list:
		if apt_id not in reminded_list:
			le_apt = apt_list[apt_id]
			
			if days_from_today(le_apt["apt_date"]) < 1:
				if le_apt['apt_type'] == "On-demand":

					html_content = f"""<h3>YOUR UPCOMING APPOINTMENT IS NEAR<h3><br><p> Type: {le_apt["apt_type"]}</p><br><p> Category: {le_apt["apt_category"]}</p><br><p> Date: {le_apt["apt_date"]}</p><br><p> Session: {le_apt["apt_session"]}</p><br><p> Number: {le_apt["apt_number"]}</p>"""

				else:
					html_content = f"""<h3>YOUR UPCOMING APPOINTMENT IS NEAR<h3><br><p> Type: {le_apt["apt_type"]}</p><br><p> Date: {le_apt["apt_date"]}</p><br><p> Session: {le_apt["apt_session"]}</p><br><p> Number: {le_apt["apt_number"]}</p>"""
				qr_data = f"""Appointment Id : {apt_id}"""
				# send_email(le_apt.customer_email, "Appointment Accepted", html_content, generate_qr_code_base64(qr_data))
				print('sending email')
				print(html_content)
				print()
				pass
				reminded_list.append(apt_id)

	save_data("reminded",reminded_list)

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
	# IF USER ALREADY LOGGED IN 
	if session.get('user_data'):
		return redirect("/home")
	
	# POST
	if request.method == 'POST':
		phone_number = request.form['phone_number']
		password = request.form['password']
		# LOAD USERS DATA
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
	# REMOVE SESSION DATA
	session.pop("user_data",None)
	return redirect("/")
	
@app.route('/register', methods=['GET','POST'])
def register():
	# IF USER ALREADY LOGGED IN 
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
		# LOAD USERS DATA
		le_data = load_data("users")

		
		if item_existed(new_user.phone_number,le_data):
			# PHONE NUMBER USED BY ANOTHER ACCOUNT
			return render_template('register.html',app_name = app_config['app_name'],message="Phone number is registered to another account",message_type="warning")
		elif query_existed('email',new_user.email,le_data):
			# EMAIL IS USED BY ANOTHER ACCOUNT
			return render_template('register.html',app_name = app_config['app_name'],message="Email is registered to another account",message_type="warning")
		elif query_existed('ssn',new_user.ssn,le_data):
			# SSN IS USED BY ANOTHER ACCOUNT
			return render_template('register.html',app_name = app_config['app_name'],message="SSN is registered to another account",message_type="warning")
		else:
			# SUCCESS
			# ADD USER TO DATABASE
			le_data[new_user.phone_number] = new_user.__dict__
			save_data("users",le_data)
			# SEND EMAIL
			html_content = f"""<h3>Account created successfully<h3>
			<br><p>You have registered an account on our HMS</p>
			<br><p>Please login to add or edit your personal information</p>"""
			send_email(new_user.email, "HMS account creation", html_content)
			print('Registration Mail Sent')
			# RETURN TO LOGIN SCREEN 
			return redirect("/login")
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
			
		# LOAD USERS DATA
		le_data = load_data("users")

		# CASE : PHONE NUMBER NOT CHANGE
		if item_existed(form_data['phone_number'],le_data) and (form_data['phone_number'] == user_data['phone_number']):

			# CASE : CHANGE EMAIL
			if (user_data['email'] != form_data['email']):
				replace_data('appointments.json',user_data['email'],form_data['email'])

			old_data = le_data[user_data['phone_number']]
			for i in form_data:
				old_data[i]=form_data[i]
			le_data[user_data['phone_number']]=old_data
			session['user_data']=old_data
			save_data("users",le_data)
			return  redirect('/profile')

		# CASE : PHONE NUMBER CHANGE AND NOT IN DATABASE
		elif not item_existed(form_data['phone_number'],le_data) and (form_data['phone_number'] != user_data['phone_number']):
			old_data = le_data[user_data['phone_number']]

			# OBSERVER ?
			# UPDATE RELATED APPOINTMENTS
			replace_data('appointments',user_data['phone_number'],form_data['phone_number'])
			# CASE : IF THEY CHANGE EMAIL AS WELL
			if (user_data['email'] != form_data['email']):
				replace_data('appointments',user_data['email'],form_data['email'])
			# SAVE CHANGE TO DATABASE
			for i in form_data:
				old_data[i]=form_data[i]
			le_data.pop(user_data['phone_number'])
			le_data[form_data['phone_number']]=old_data
			session['user_data']=old_data
			save_data("users",le_data)
			return  redirect('/profile')
		# CASE: PHONE NUMBER CHANGE AND IN DATABASE
		elif item_existed(form_data['phone_number'],le_data) and (form_data['phone_number'] != user_data['phone_number']):
			return render_template('user_profile.html',app_name = app_config['app_name'], user_data = session['user_data'],message="The Phone Number is currently in use",message_type="danger")
	
		
	# REFRESH SESSION DATA
	le_data = load_data("users")
	session['user_data']=le_data[session['user_data']['phone_number']]
	
	# RENDER USER'S PROFILE SCREEN
	return render_template('user_profile.html',app_name = app_config['app_name'], user_data = session['user_data'])

@app.route('/book_appointment', methods=['GET','POST'])
def book_appointment():
	# USER NOT LOGGED IN 
	if not session.get('user_data'):
		return redirect("/login")
	
	# POST
	if request.method == 'POST':
		# LOAD APPOINTMENTS DATA
		le_data = load_data("appointments")
		# CASE : ANYTHING ELSE
		if request.form['apt_type'] != "On-demand":
			apt_category = ""
		# CASE : TYPE IS ON DEMAND CHECK CATEGORY
		else:
			apt_category = request.form['apt_category']
   
   
		apt_number = 1
		for item_id in le_data:
			item  = le_data[item_id]
			if ( item['apt_type'] == request.form['apt_type'] ) and (item['apt_category'] == apt_category) and (item['apt_date'] == request.form['apt_date']) and (item['apt_session'] == request.form['apt_session']):
				apt_number +=1
  

  		# SAVE TO DATABASE
		apt_id = len(le_data)+1
		# CREATE NEW INSTANT OF APPOINTMENT 
		le_apt = Appointment(apt_type = request.form['apt_type'],
						apt_category = apt_category,
						apt_date = request.form['apt_date'],
						apt_session = request.form['apt_session'],
						apt_number = apt_number,
						customer_phone = session['user_data']['phone_number'],
						customer_email = session['user_data']['email'],
						status="Pending",
						apt_description=request.form['apt_description'],
						rating=None,
						apt_id=apt_id
		)

		le_data[apt_id]=le_apt.__dict__
		save_data("appointments",le_data)
		# SEND EMAIL
		html_content = """<h3>This email is to inform you that you booked an appointment throught our system <h3>
		<br><p>Please give this code to our staff upon arrival</p>"""
		qr_data = f"""Appointment Id : {apt_id}"""

		send_email(le_apt.customer_email, "Appointment Accepted", html_content, generate_qr_code_base64(qr_data))
		print('Appointment Mail Sent')
		# RENDER HOME SCREEN 
		return redirect('/home')
	
	min_date = datetime.today().strftime('%Y-%m-%d')
	max_date = (datetime.today() + timedelta(weeks=2)).strftime('%Y-%m-%d')
	return render_template('book_appointment.html', app_name = app_config['app_name'], user_data = session['user_data'], min_date = min_date, max_date = max_date)

# API FOR APPOINTMENT BOOKING
# INPUT APPOINTMENT TYPE & DATE
# RETURN AVAILABILITY OF MORNING / AFTERNOON SESSION
 
@app.route('/api/get_availability/', methods=['GET'])
def get_availability():
	apt_type = request.args.get('apt_type')
	apt_date = request.args.get('apt_date')
	apt_category = request.args.get('apt_category')

	if apt_type != 'On-demand':
		apt_category = ""

	le_data = load_data("appointments")

	morning_count = 0
	afternoon_count = 0

	print(f'Type: {apt_type}')
	print(f'Category: {apt_category}')
	print(f'Date: {apt_date}')
	
	for i in le_data:
		if (le_data[i]['apt_date'] == apt_date) and (le_data[i]['apt_type'] == apt_type) and (le_data[i]['apt_category'] == apt_category):
			if le_data[i]['apt_session'] == 'Morning':
				morning_count+=1
			else: 
				afternoon_count+=1

	availability = {
		'morning': morning_count < 10,
		'afternoon': afternoon_count < 10,
	}
	print( availability)
	return jsonify(availability)

# USER'S APPOINTMENTS
@app.route('/appointments', methods=['GET','POST'])
def user_appointments():
	# USER NOT LOGGED IN 
	if not session.get('user_data'):
		return redirect("/login")
	
	# GET
	user_data = session['user_data']
	le_data = load_data("appointments")
	apt_list = query_with_pair("customer_phone",user_data["phone_number"],le_data)
	return render_template('user_appointments.html', app_name = app_config['app_name'], user_data=user_data, appointments = apt_list)

# USER'S APPOINTMENT
@app.route('/appointment/<apt_id>', methods=['GET','POST','DELETE'])
def user_appointment(apt_id):
	# USER NOT LOGGED IN 
	if not session.get('user_data'):
		return redirect("/login")

	# POST
	if request.method == 'POST':
		user_data = session['user_data']
		le_data = load_data("appointments")
		le_apt = le_data[apt_id]
		# IF THE USER IS THE OWNER OF THE APT
		if user_data["phone_number"] == le_apt["customer_phone"]:
			# UPDATE TYPE
			le_apt['apt_type'] = request.form['apt_type']
			# UPDATE CATEGORY
			if le_apt['apt_type'] == 'On-demand':
				le_apt['apt_category'] = request.form['apt_category']
			else:
				le_apt['apt_category'] = ""
			# UPDATE DATE
			le_apt['apt_date'] = request.form['apt_date']
			# UPDATE SESSION
			le_apt['apt_session'] = request.form['apt_session']
			# UPDATE DESCRIPTION
			le_apt['apt_description'] = request.form['apt_description']
			# UPDATE NUMBER
			apt_number = 1
			for item_id in le_data:
				item  = le_data[item_id]
				if ( item['apt_type'] == request.form['apt_type'] ) and (item['apt_category'] == le_apt['apt_category']) and (item['apt_date'] == request.form['apt_date']) and (item['apt_session'] == request.form['apt_session']):
					apt_number +=1
			le_apt['apt_number'] = apt_number

			# UPDATE DATA
			le_data[apt_id] = le_apt
			save_data("appointments",le_data)
		return redirect("/home")

	
	# GET
	
	# REFRESH SESSION DATA
	le_data = load_data("users")
	session['user_data']=le_data[session['user_data']['phone_number']]
	
	user_data = session['user_data']
	le_data = load_data("appointments")
	le_apt = le_data[apt_id]
	if user_data["phone_number"] == le_apt["customer_phone"]:
		min_date = datetime.today().strftime('%Y-%m-%d')
		max_date = (datetime.today() + timedelta(weeks=2)).strftime('%Y-%m-%d')
		return render_template('user_appointment.html', app_name = app_config['app_name'], user_data=user_data, le_apt = le_apt, min_date = min_date, max_date = max_date)
	else:
		return redirect("/home")

# CANCEL USER'S APPOINTMENT
@app.route('/delete_appointment/<apt_id>', methods=['GET'])
def cancel_appointment(apt_id):
	# USER NOT LOGGED IN 
	if not session.get('user_data'):
		return redirect("/login")

	# GET
	user_data = session['user_data']
	le_data = load_data("appointments")
	le_apt = le_data[apt_id]
	if user_data["phone_number"] == le_apt["customer_phone"]:
		le_apt["status"] = "Canceled"
		le_data[apt_id] = le_apt
		save_data("appointments",le_data)

		return redirect("/appointments")
	return redirect("/home")
		
# CANCEL USER'S APPOINTMENT
@app.route('/rate_appointment/<apt_id>/<rating>', methods=['GET'])
def rate_appointment(apt_id,rating):
	# USER NOT LOGGED IN 
	if not session.get('user_data'):
		return redirect("/login")

	user_data = session['user_data']
	le_data = load_data("appointments")
	le_apt = le_data[apt_id]
	if user_data["phone_number"] == le_apt["customer_phone"]:
		le_apt["rating"] = rating
		le_data[apt_id] = le_apt
		save_data("appointments",le_data)

		return "Nice"
	return redirect("/home")

# USER'S RECORDS
@app.route('/records', methods=['GET','POST'])
def user_records():
	# USER NOT LOGGED IN 
	if not session.get('user_data'):
		return redirect("/login")
	
	# POST
	if request.method == 'POST':
		# LOAD APPOINTMENTS DATA
		pass
	# REFRESH SESSION DATA
	le_data = load_data("users")
	session['user_data']=le_data[session['user_data']['phone_number']]

	return render_template('user_records.html', app_name = app_config['app_name'], user_data = session['user_data'])

if __name__ == '__main__':
	scheduler.start()
	# webbrowser.open('http://127.0.0.1:5000/', new=2)
	app.run(debug=True)
