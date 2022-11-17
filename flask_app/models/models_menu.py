from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import models_user
from flask import flash
db = 'diet_menu'

class Menu:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.ingredient = data['ingredient']
        self.calorie = data['calorie']
        self.instruction = data['instruction']
        self.date_made = data['date_made']
        self.creator_id = data['creator_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.all_likes = []

    # Add new menu
    @classmethod
    def new_menu(cls,data):
        query = """
                INSERT INTO menus (title, ingredient, calorie, instruction, date_made, creator_id, created_at, updated_at)
                VALUES (%(title)s, %(ingredient)s, %(calorie)s, %(instruction)s, %(date_made)s, %(creator_id)s, NOW(), NOW())
                """
        return connectToMySQL(db).query_db(query,data)

    # Edit menu
    @classmethod
    def edit_menu(cls,data,menu_id):
        query = f"UPDATE menus SET title = %(title)s, ingredient = %(ingredient)s, calorie = %(calorie)s, instruction = %(instruction)s, date_made = %(date_made)s WHERE id = {menu_id}"
        return connectToMySQL(db).query_db(query,data)

    # Like menu
    @classmethod
    def add_like(cls,data):
        query = """
                INSERT INTO likes (menu_id, like_sender_id)
                VALUES (%(menu_id)s, %(like_sender_id)s)
                """
        return connectToMySQL(db).query_db(query,data)
    
    # Dislike menu
    @classmethod
    def dislike(cls,data):
        query = """
                DELETE FROM likes 
                WHERE menu_id = %(menu_id)s
                AND like_sender_id = %(like_sender_id)s
                """
        return connectToMySQL(db).query_db(query,data)

    # Delete menu: need to delete the menu from likes table first
    @classmethod
    def delete_liked_menu(cls,data):
        query = "DELETE FROM likes WHERE menu_id = %(id)s"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def delete_menu(cls,data):
        query = "DELETE FROM menus WHERE id = %(id)s"
        return connectToMySQL(db).query_db(query,data)

    # Get all menus of one creator
    @classmethod
    def get_menus_of_creator(cls,data):
        query = """
                SELECT * FROM menus
                JOIN users ON users.id = menus.creator_id
                WHERE users.id = %(id)s
                """
        results = connectToMySQL(db).query_db(query,data)
        all_menus = []
        for db_row in results:
            one_menu = cls(db_row)
            creator_data = {
                'id': db_row['users.id'],
                'first_name': db_row['first_name'],
                'last_name': db_row['last_name'],
                'email': db_row['email'],
                'password': db_row['password'],
                'created_at': db_row['users.created_at'],
                'updated_at': db_row['users.updated_at']
            }
            creator = models_user.User(creator_data)
            one_menu.creator = creator
            all_menus.append(one_menu)
        return all_menus

    # Get one menu with its creator for edit
    @classmethod
    def get_one_menu_with_creator(cls,data):
        query = """
                SELECT * FROM menus
                JOIN users ON users.id = menus.creator_id
                WHERE menus.id = %(id)s
                """
        results = connectToMySQL(db).query_db(query,data)
        menu = cls(results[0])
        creator_info = {
            'id': results[0]['users.id'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'email': results[0]['email'],
            'password': results[0]['password'],
            'created_at': results[0]['users.created_at'],
            'updated_at': results[0]['users.updated_at']
        }
        creator = models_user.User(creator_info)
        menu.creator = creator
        return menu

    # Get all menus, creators info, likes number
    @classmethod
    def get_all_menus_and_likes(cls):
        query = """
                SELECT * FROM menus
                JOIN users ON users.id = menus.creator_id
                LEFT JOIN likes ON menus.id = likes.menu_id
                LEFT JOIN users AS users2 ON users2.id = likes.like_sender_id
                """
        results = connectToMySQL(db).query_db(query)
        likes = []
        for result in results:
            new_like = True
            like_sender_data = {
                'id': result['users2.id'],
                'first_name': result['users2.first_name'],
                'last_name': result['users2.last_name'],
                'email': result['users2.email'],
                'password': result['users2.password'],
                'created_at': result['users2.created_at'],
                'updated_at': result['users2.updated_at']
            }
            # Check to see if the logged in user like or not
            if len(likes) > 0 and likes[(len(likes)-1)].id == result['id']:
                likes[(len(likes)-1)].all_likes.append(models_user.User(like_sender_data))
                new_like = False
            if new_like:
                like = cls(result)
                creator_data = {
                    'id': result['users.id'],
                    'first_name': result['first_name'],
                    'last_name': result['last_name'],
                    'email': result['email'],
                    'password': result['password'],
                    'created_at': result['users.created_at'],
                    'updated_at': result['users.updated_at']
                }
                creator = models_user.User(creator_data)
                like.creator = creator
                if result['users2.id'] is not None:
                    like.all_likes.append(models_user.User(like_sender_data))
                likes.append(like)
        return likes

    # Menu validator
    @staticmethod
    def menu_validator(data):
        is_valid = True
        if len(data['title']) < 1 or len(data['ingredient']) < 1 or len(data['calorie']) < 1 or len(data['instruction']) < 1:
            flash('All fields are required!', 'menu')
            is_valid = False
        if int(data['calorie']) < 1:
            flash('Calories must be greater than 0!', 'menu')
            is_valid = False
        if len(data['date_made']) < 1:
            flash('Please select a date you made this menu!', 'menu')
            is_valid = False
        return is_valid