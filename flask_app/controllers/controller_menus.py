from flask_app import app
import os, requests
from flask import request, render_template, redirect, session
from pprint import pprint
from flask_app.models.models_menu import Menu
from flask_app.models.models_user import User

# Create new menu
@app.route('/create_page')
def create_menu_page():
    return render_template('/create.html')

@app.route('/create', methods=['POST'])
def create_menu():
    menu_data = {
        'title': request.form['title'],
        'ingredient': request.form['ingredient'],
        'calorie': request.form['calorie'],
        'instruction': request.form['instruction'],
        'date_made': request.form['date_made'],
        'creator_id': session['user_id'],
    }
    valid = Menu.menu_validator(menu_data)
    if valid:
        Menu.new_menu(menu_data)
        return redirect('/dashboard')
    return redirect('/create_page')

# Edit menu
@app.route('/edit/<int:menu_id>')
def edit_menu_page(menu_id):
    menu_data = {
        'id': menu_id
    }
    menu = Menu.get_one_menu_with_creator(menu_data)
    return render_template('/edit.html', menu=menu)

@app.route('/edit_menu/<int:menu_id>', methods=['POST'])
def edit_menu(menu_id):
    menu_data = {
        'title': request.form['title'],
        'ingredient': request.form['ingredient'],
        'calorie': request.form['calorie'],
        'instruction': request.form['instruction'],
        'date_made': request.form['date_made']
    }
    user_id = session['user_id']
    valid = Menu.menu_validator(menu_data)
    if valid:
        Menu.edit_menu(menu_data,menu_id)
        return redirect(f'/show_menu/{user_id}')
    return redirect(f'/edit/{menu_id}')

# Show user's menus
@app.route('/show_menu/<int:user_id>')
def show_my_menu(user_id):
    user_data = {
        'id': user_id
    }
    user = User.get_user_by_id(user_data)
    menus = Menu.get_menus_of_creator(user_data)
    return render_template('/show.html', user=user, menus=menus)

# View menu
@app.route('/view/<int:menu_id>')
def view_menu(menu_id):
    user_data = {
        'id': session['user_id']
    }
    user = User.get_user_by_id(user_data)
    menu_data = {
        'id': menu_id
    }
    menu = Menu.get_one_menu_with_creator(menu_data)
    like_senders = User.get_like_senders_of_menu(menu_data)
    return render_template('/view.html', user=user, menu=menu, like_senders=like_senders)

# Like and dislike menu
@app.route('/like/<int:menu_id>')
def like_menu(menu_id):
    menu_data = {
        'menu_id': menu_id,
        'like_sender_id': session['user_id']
    }
    Menu.add_like(menu_data)
    return redirect('/dashboard')

@app.route('/dislike/<int:menu_id>')
def dislike_menu(menu_id):
    menu_data = {
        'menu_id': menu_id,
        'like_sender_id': session['user_id']
    }
    Menu.dislike(menu_data)
    return redirect('/dashboard')

# Delete menu
@app.route('/delete/<int:menu_id>')
def delete_menu(menu_id):
    menu_data = {
        'id': menu_id
    }
    user_id = session['user_id']
    Menu.delete_liked_menu(menu_data)
    Menu.delete_menu(menu_data)
    return redirect(f'/show_menu/{user_id}')

# Connect API to search for nutrition facts
@app.route('/nutrition', methods=['POST'])
def get_nutrition():
    food = request.form['food']
    session['food'] = food
    key = os.environ.get('KEY')
    api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(food)
    response = requests.get(api_url, headers={'X-Api-Key': key})
    if response.status_code == requests.codes.ok:
        pprint(response.json())
    else:
        pprint("Error:", response.status_code, response.text)
    session['name'] = response.json()[0]['name']
    session['calories'] = response.json()[0]['calories']
    session['serving_size_g'] = response.json()[0]['serving_size_g']
    session['fat_total_g'] = response.json()[0]['fat_total_g']
    session['fat_saturated_g'] = response.json()[0]['fat_saturated_g']
    session['protein_g'] = response.json()[0]['protein_g']
    session['sodium_mg'] = response.json()[0]['sodium_mg']
    session['potassium_mg'] = response.json()[0]['potassium_mg']
    session['cholesterol_mg'] = response.json()[0]['cholesterol_mg']
    session['carbohydrates_total_g'] = response.json()[0]['carbohydrates_total_g']
    session['fiber_g'] = response.json()[0]['fiber_g']
    session['sugar_g'] = response.json()[0]['sugar_g']
    return redirect('/create_page')