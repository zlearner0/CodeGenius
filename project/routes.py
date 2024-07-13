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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
         hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
         user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
         with app.app_context():
             db.session.add(user)
             db.session.commit()
         flash(f'You Registered Successfully!')
         return redirect(url_for('home'))
    return render_template('register.html',title='Register',form=form)