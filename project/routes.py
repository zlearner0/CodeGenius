from flask import render_template
from project import app

@app.route('/home')
@app.route('/')
def home():
    return render_template('home.html')

