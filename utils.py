import json
from datetime import datetime, timedelta

def json_datetime_hook(dct):
    for key, value in dct.items():
        if isinstance(value, str) and is_iso_date(value):
            dct[key] = datetime.fromisoformat(value)
    return dct

def is_iso_date(s):
    try:
        datetime.fromisoformat(s)
        return True
    except ValueError:
        return False

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code""" #save date as strings
    if isinstance(obj, (datetime,)):
        return obj.isoformat()
    raise TypeError("Type not serializable")

def load_data():
	# global data
	with open('data.json', 'r') as outfile:
		data = json.load(outfile, object_hook=json_datetime_hook) 
	
	return data

def save_data(data):
	with open('data.json', 'w', encoding='utf8') as outfile:
		json.dump(data, outfile, indent=4 , default=json_serial)
	data = load_data()	

def update_student(data, user):
	for student in data['students']:
		if student['id'] == user['id']:
			student.update(user)
	
	save_data(data)

def get_credentials(data):
		credentials= {
			"usernames": {

			}
		}
		for user in data['students'] + data['admins']:

			credentials["usernames"][user['username']] = {
				"name": f"{user['name']} {user['family_name']}",
				"password" : user['password'],
				"email":user['email']
			}

		return credentials

def get_user_by_username(data, username):
	for user in data['admins']:
		if user['username'] == username:
			return (user, 'admin')
	
	for user in data['students']:
		if user['username'] == username:
			return (user, 'student')

def get_closest_deadline(user):
	if len(user['books']) > 0:
		closest_deadline = user['books'][0]["deadline"]
		for book in user['books']:
			if closest_deadline > book['deadline']:
				closest_deadline = book['deadline']

		return closest_deadline
	else : return None

def is_past_deadline(student):
	now = datetime.now()
	closest_deadline = get_closest_deadline(student)
	if closest_deadline == None : return False
	else : return now > closest_deadline

def borrow_book(data, book, user):
	if len(user['books']) < 3:
		if book not in [b['book'] for b in user['books']]:
			now = datetime.now()
			deadline = timedelta(days=7)
			book = {"book":book,
					"b_date":now,
					"deadline": now+deadline}
			user['books'].append(book)

			update_student(data, user)
		
			return True
		else : return "You already borrowed this book"
	else :
		return "You can't borrow more than 3 books"
	
def return_book(data, user, book):
	print('book', book, end='\n\n')
	for b in user['books']:
		if b == book:
			user['books'].remove(b)  # Remove the specific book, not the entire dictionary
			update_student(data, user)
			return True
	return "Book not found in user's borrowed books"
