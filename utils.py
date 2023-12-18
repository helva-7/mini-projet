import json
from datetime import datetime, timedelta
import re

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
	with open('data.json', 'r') as outfile:
		data = json.load(outfile, object_hook=json_datetime_hook) 
	
	return data

def save_data(data):
	with open('data.json', 'w', encoding='utf8') as outfile:
		json.dump(data, outfile, indent=4 , default=json_serial)
	# data = load_data()	

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

def get_overdue_books(student):
	now = datetime.now()
	overdue_books = []
	for book in student['books']:
		if now > book['deadline']: overdue_books.append(book)

	return overdue_books


def borrow_book(data, book, user):
	
	if book["num"] == 0 : return "Book unavailable"
	
	if len(user['books']) < 3 :
		if book not in [b['book'] for b in user['books']]:
			now = datetime.now()
			deadline = timedelta(days=7)
			book["num"] -= 1
			book = {"book":book,
					"b_date":now,
					"deadline": now+deadline}
			user['books'].append(book)

			save_data(data)

			return True
		else : return "You already borrowed this book"
	else :
		return "You can't borrow more than 3 books"
	
def return_book(data, user, book):
	print('book', book, end='\n\n')
	for b in user['books']:
		if b == book:
			user['books'].remove(b)  # Remove the specific book, not the entire dictionary
			#updating books
			for i in data['books']:
				if i == book['book']: 
					i['num']+=1
					break
				
			save_data(data)
			return True
	return "Book not found in user's borrowed books"


def suspend_user(data, user_to_suspend):
	for student in data['students']:
		if student == user_to_suspend:
			data['students'].remove(student)

	save_data(data)

def get_user_by_id(data, id):
	for user in data['students']:
		if user['id'] == id:
			return user
	
def is_valid_email(email):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))


def generate_student_id(data):
	return max([student['id'] for student in data['students']]) + 1
