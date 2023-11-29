import json
import bcrypt
from datetime import datetime, timedelta


class User:
    def __init__(self, id, name, family_name, email, username, password):
        self.id = id
        self.name = name
        self.family_name = family_name
        self.email = email
        self.username = username
        self.password = self._hash_password(password)
        self.email = email
    
    def _hash_password(self, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password

    def verify_password(self, input_password):
        # Verify a password against its hash
        return bcrypt.checkpw(input_password.encode('utf-8'), self.password)
    
    def login(self, username, password):
        return self.username == username and self.verify_password(password) 
    

class Admin(User):
    def __init__(self, id,  name, family_name, email, username, password):
        super().__init__(id, name, family_name, email, username, password)

class Student(User):
    def __init__(self, id, name, family_name, email, username, password, books):
        super().__init__(id, name, family_name, email, username, password)
        self.books = books
    
    def borrow_book(self, book):
        if len(self.books) < 3:
            now = datetime.now()
            deadline = timedelta(days=7)
            book = {"book":book,
                    "b_date":now,
                     "deadline": now+deadline}
            self.books.append(book)

            return True
        else :
            return False
    def return_book(self, book):
        if book in self.books:
            self.books.remove(book)
            return True
        else : 
            return False


class Book:
    def __init__(self, id, title, author, editor, ISBN, num, year):
        self.id = id
        self.title = title
        self.author = author
        self.editor = editor
        self.ISBN = ISBN
        self.num = num
        self.year = year

class DataManager:
    @staticmethod
    def load_data(file):
        with open(file, 'r') as outfile:
            json_data = json.load(outfile)
        
        students = []
        for student_data in json_data["students"]:
            student_data["books"] = [Book(**book) for book in student_data["books"]]
            student = Student(**student_data)
            students.append(student)

        data = {
            "students": students,
            "admins": [Admin(**admin) for admin in json_data["admins"]],
            "books": [Book(**book) for book in json_data["books"]]
        }

        return data
    
    @staticmethod
    def update_data(file, data):
        new_json_data = {
            "books" : [vars(book) for book in data["books"]],
            "admins" : [vars(admin) for admin in data["admins"]],
            "students" : [vars(student) for student in data["students"]]
            }

        with open(file, 'w') as outfile:
            json.dump(new_json_data, outfile, indent=4)



