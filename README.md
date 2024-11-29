# Healthcare Management System - OOAD - 2024

Setup the venv

```bat
python -m venv ./venv
```

Set Policy to activate venv

```bat
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUse
```

Activate Venv

```bat
venv/Scripts/activate
```

Install dependency

```bat
pip install -r requirements.txt
```

Run Flask Server

```bat
python main.py
```

Regenerate requirements.txt file

```bat
pip3 freeze > requirements.txt
```
