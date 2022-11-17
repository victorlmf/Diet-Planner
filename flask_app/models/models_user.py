import re
from flask import flash
from pprint import pprint
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import models_menu
db = 'diet_menu'

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.menu = None

    # Create User
    @classmethod
    def create_user(cls,data):
        query = """
                INSERT INTO users (first_name, last_name, email, password, created_at, updated_at)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(pw_hash)s, NOW(), NOW())
                """
        return connectToMySQL(db).query_db(query,data)

    # Get one user by email, for login purpose
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    # Get one user by ID
    @classmethod
    def get_user_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL(db).query_db(query,data)
        return cls(results[0])

    # Get all like_senders of one menu
    @classmethod
    def get_like_senders_of_menu(cls,data):
        query = """
                SELECT * FROM users
                LEFT JOIN likes ON users.id = likes.like_sender_id
                LEFT JOIN menus ON menus.id = likes.menu_id
                WHERE menus.id = %(id)s
                """
        results = connectToMySQL(db).query_db(query,data)
        all_like_senders = []
        for db_row in results:
            one_like_sender = cls(db_row)
            menu_data = {
                'id': db_row['menus.id'],
                'title': db_row['title'],
                'ingredient': db_row['ingredient'],
                'calorie': db_row['calorie'],
                'instruction': db_row['instruction'],
                'date_made': db_row['date_made'],
                'creator_id': db_row['creator_id'],
                'created_at': db_row['menus.created_at'],
                'updated_at': db_row['menus.updated_at']
            }
            menu = models_menu.Menu(menu_data)
            one_like_sender.menu = menu
            all_like_senders.append(one_like_sender)
        return all_like_senders

    # User Validation
    @staticmethod
    def user_validation(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[0-9]).{8,}')
        is_valid = True
        if len(data['first_name']) == 0 or len(data['last_name']) == 0 or len(data['email']) == 0 or len(data['password']) == 0:
            flash('All fields are required!', 'register')
            is_valid = False
        if len(data['first_name']) < 2 and len(data['first_name']) != 0:
            flash('First name must be at least 2 characters!', 'register')
            is_valid = False
        if len(data['last_name']) < 2 and len(data['last_name']) != 0:
            flash('Last name must be at least 2 characters!', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']) and len(data['email']) != 0:
            flash('Invalid email address!', 'register')
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(db).query_db(query,data)
        if len(results) != 0:
            flash('This email is already being used!', 'register')
            is_valid = False
        if not PASSWORD_REGEX.match(data['password']) and len(data['password']) != 0:
            flash('Password must be at least 8 characters, with 1 number and 1 uppercase letter!', 'register')
            is_valid = False
        if data['password'] != data['confirm_pw']:
            flash('Password does not match!', 'register')
            is_valid = False
        return is_valid
