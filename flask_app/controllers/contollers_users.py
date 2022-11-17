from flask_app import app
from flask import request, render_template, redirect, flash, session
import requests
# from flask_app.models.models_menu import Menu
from flask_app.models.models_user import User
from flask_app.models.models_menu import Menu
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    user_data = {
        'id': session['user_id']
    }
    user = User.get_user_by_id(user_data)
    all_info = Menu.get_all_menus_and_likes()
    return render_template('/dashboard.html', user=user, all_info=all_info)

# Registration
@app.route('/')
def registration_page():
    return render_template('/registration.html')

@app.route('/register', methods=['POST'])
def register():
    user_data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': request.form['password'],
        'confirm_pw': request.form['confirm_pw']
    }
    valid = User.user_validation(user_data)
    if valid:
        pw_hash = bcrypt.generate_password_hash(user_data['password'])
        user_data['pw_hash'] = pw_hash
        user_id = User.create_user(user_data)
        session['user_id'] = user_id
        return redirect('/dashboard')
    return redirect('/')

# Login
@app.route('/login_page')
def login_page():
    return render_template('/login.html')

@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if len(request.form['email']) == 0 or len(request.form['password']) == 0:
        flash('All fields are required!', 'login')
        return redirect('/login_page')
    if not user and len(request.form['email']) != 0:
        flash('Invalid email or password!', 'login')
        return redirect('/login_page')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid password!', 'login')
        return redirect('/login_page')
    session['user_id'] = user.id
    return redirect('/dashboard')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')