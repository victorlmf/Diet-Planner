# Diet-Planner

This Diet Planner application provides the ability for users to check the nutrition facts of any food in order to create their own diet menu. 

## Features

### Registration & Login
- Proper input validations are added for resitration and login process to make sure users provide accurate information when registering and logging in. 

### Dashboard
- A table is presented to show all diet menus created by all users, the logged-in user can view and like/dislike the menus.
- The Create Menu button routes user to a new page to create a new diet menu.
- My Menus button routes user to manage his own menus.
- Logout button clears all session data and redirects user back to registration page. 

### Create New Menu
- User can create the new diet menu by adding title, ingredients, caloreis, instructions and the date that the menu was made. 
- User can search any food, the search button is linked to the API to show all the nutrition facts of the searched food. 

### Edit Menu
- The edit menu page is similar to create menu page with pre-generated menu details. 

### View Menu 
- The view menu page displays all the details of the menu, it also displays who liked the menu. 

### My Menu
- My menu page shows a table of the menus that created by the logged in user, user has the ability to edit and delete any menu. 

## Technical Overview
This application uses the following frameworks and languages:
- HTML, CSS, Bootstrap
- Python
- Flask
- MySQL

## Installation
This application can be run locally by cloning it onto your computer. MySQL is needed to be installed prior running the application. MySQL Workbench is required to be installed to setup the ERD and connect the application to the databse. 

Virtual environment with the use of Pipenv is needed for backend. Dependencies are required to be installed. 
- to install dependencies for backend
```
$ cd server
$ pipenv shell
$ pipenv install
```

### Start running locally
The application will be run on localhost port, to activate virtual environment and start running, by default on `http://localhost:5000`
```
$ cd server
$ pipenv shell
$ pipenv install flask pymysql
$ python server.py
```

- to deactivate backend virtual environment when done with application
```
$ exit
```
