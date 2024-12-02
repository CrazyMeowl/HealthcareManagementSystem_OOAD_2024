# Healthcare Management System - OOAD - 2024
Step 1: run "setup_secrret.bat" as admin

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

Do this after adding dependency: Regenerate requirements.txt file

```bat
pip3 freeze > requirements.txt
```
