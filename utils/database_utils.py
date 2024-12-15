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

# Function to check if the value of that key existed in the database
# for example to check if email : example@domain.com existed use
# query_existed('email','example@domain.com',data)
def query_existed(key,value,data):
	for item in data:
		if data[item][key] == value:
			return True
	return False


def replace_data(database_name, old_phrase, new_phrase):
	try:
		file_name = f'./database/{database_name}.json'
		# Open the file in read mode
		with open(file_name, 'r', encoding='utf-8') as file:
			content = file.read()
		
		# Replace the old phrase with the new one
		updated_content = content.replace(old_phrase, new_phrase)
		
		# Open the file in write mode to save the updated content
		with open(file_name, 'w', encoding='utf-8') as file:
			file.write(updated_content)
	except Exception as bug:
		print(bug)


def query_with_pair(key,value,data):
	item_list = []
	for item in data:
		if data[item][key] == value:
			item_list.append(data[item])
	return item_list