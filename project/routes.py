from project import app, db, bcrypt
from flask import render_template, url_for, redirect, flash, request
from project.models import User, Course, User_Course
from project.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required




@app.route('/home')
@app.route('/')
def home():
    return render_template('home.html', title='Home')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


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
         return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)


@app.route('/login',  methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password')

    return render_template('login.html',title='Login',form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/member_area')
@login_required
def member_area():
    courses = Course.query.all()
    user_courses = User_Course.query.filter(User_Course.the_user.has
                                            (username=current_user.username)).all()
    return render_template('member_area.html',title='Member', courses=courses,
                            user_courses=user_courses)

@app.route('/save_courses', methods=['POST'])
def save_courses():
    user_courses = User_Course.query.filter(User_Course.the_user.has
                                            (username=current_user.username)).all()
    courses_list = [ user_course.the_course.title for user_course in user_courses]
    selected_courses = request.form.getlist('course_checkbox')
    the_user = User.query.filter_by(username=current_user.username).first()
    for course_name in selected_courses:
            if course_name not in courses_list:
                the_course = Course.query.filter_by(title=course_name).first()
                user_course = User_Course(the_user=the_user,the_course=the_course)
                db.session.add(user_course)
    db.session.commit()
    return redirect(url_for('member_area'))


@app.route('/cancel_course')
def cancel_course():
    course_title = request.args.get('course')
    if course_title:
        the_course = Course.query.filter_by(title=course_title).first()
        the_user = User.query.filter_by(username=current_user.username).first()
        user_course = User_Course.query.filter_by(the_user=the_user, the_course=the_course).first()
        if user_course:
            db.session.delete(user_course)
        db.session.commit()
    return redirect(url_for('member_area'))


@app.route('/admin')
@login_required
def admin():
    users = User.query.all()
    courses = Course.query.all()
    users_courses = User_Course.query.all()
    id = current_user.id
    if id == 5:
        return render_template('admin.html', title='Admin', users=users, courses=courses,
                                users_courses=users_courses)
    else:
        flash('Admin privilege needed to access admin page')
        return redirect(url_for('member_area'))
    

@app.route('/landing_page')
def landing_page():
    return render_template('landing_page.html')