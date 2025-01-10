# Healthcare Management System - OOAD - 2024
The Healthcare Management System was created as an assignment-project for the course of Object Oriented Analysis and Design.

With the purpose practice implementing design pattern and system designing

Through the HMS, patient can register an account, schedule an apt, view all their apts, view an apt detail, cancel an apt, view their medical record, and edit their personal profile.

# Step by step guide on how to run the project
PREREQUISITE: Have an email for mailing service
 
 FOR GMAIL: Do as follow:
-  Enable 2 factors authentication (2FA)
-  Create an app password with via this link : https://myaccount.google.com/apppasswords

## Setup
Step 0: Edit the "setup_secret.bat" with your email credentials.
For example 
```bat
setx SENDER_EMAIL_USERNAME example@email.com /m
setx SENDER_EMAIL_PASSWORD example_app_password /m
```

Step 1: run "setup_secret.bat" as admin

Step 2: Setup the venv

```bat
python -m venv ./venv
```

Step 3: Set Policy to activate venv

```bat
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUse
```

Step 4: Activate Venv

```bat
venv/Scripts/activate
```

Step 5: Install dependency

```bat
pip install -r requirements.txt
```

Step 6: Run Flask Server

```bat
python main.py
```
## Update requirement file
Do this after adding dependency: Regenerate requirements.txt file

```bat
pip3 freeze > requirements.txt
```
