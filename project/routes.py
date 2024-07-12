from project import app, db, bcrypt
from flask import render_template, url_for, redirect, flash, request
from project.models import User, Course, User_Course
from project.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/home')
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register',  methods=['GET', 'POST'])
def register():

    return render_template('register.html',title='Register')