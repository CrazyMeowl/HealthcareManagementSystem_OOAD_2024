import json

# Function to load data from the JSON file
def load_data(database_name):
    try:
        file_name = f'./database/{database_name}.json'
        with open(file_name, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, return an empty dictionary
        return {}

# Function to save data to the JSON file
def save_data(database_name, data):
    file_name = f'./database/{database_name}.json'
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Function to check if the key existed in the dict data
def item_existed(item,data):
    if item in data:
        return True
    else:
        return False