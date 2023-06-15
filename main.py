from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import sqlite3

connection = sqlite3.connect('instance\codingthunder.db')
cursor = connection.cursor()

with open("config.json", "r") as config:
    params = json.load(config)["params"]

local_server = True

db = SQLAlchemy()
app = Flask(__name__)

if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["local_server"]
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["prod_server"]

db.init_app(app)


class contactDetails(db.Model):
    contact_srno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact_name = db.Column(db.String(80), nullable=False)
    contact_phone_num = db.Column(db.String(12), nullable=False)
    contact_message = db.Column(db.String(120), nullable=False)
    contact_date = db.Column(db.String(12), nullable=False)
    contact_email_id = db.Column(db.String(20), nullable=True, unique=True)


class postDetails(db.Model):
    post_srno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_title = db.Column(db.String(1000), nullable=False)
    post_content = db.Column(db.String(5000), nullable=False)
    post_date = db.Column(db.String(20), nullable=True)


class signupDetails(db.Model):
    reg_srno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reg_frist_name = db.Column(db.String(30), nullable=False)
    reg_last_name = db.Column(db.String(30), nullable=False)
    reg_gender = db.Column(db.String(12), nullable=False)
    reg_phone_no = db.Column(db.Integer, nullable=False)
    reg_birth_date = db.Column(db.String(12), nullable=False)
    reg_date = db.Column(db.String(12), nullable=False)
    reg_email_id = db.Column(db.String(20), nullable=True, unique=True)
    reg_subject = db.Column(db.String(30), nullable=False)
    reg_password = db.Column(db.String(50), nullable=False)


# create first app
@app.route('/')
def home():
    return render_template('index.html', params=params)


@app.route('/about')
def aboout():
    return render_template('about.html', params=params)


@app.route('/posts')
def post():
    return render_template('posts.html', params=params)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        phone_num = request.form.get('phone_num')
        message = request.form.get('message')
        email = request.form.get('email')
        entry = contactDetails(contact_name=name, contact_phone_num=phone_num, contact_date=datetime.now(),
                               contact_message=message, contact_email_id=email)
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html', params=params)


@app.route('/set-post', methods=['GET', 'POST'])
def setpost():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        entry_post = postDetails(post_title=title, post_date=datetime.now(), post_content=content)
        db.session.add(entry_ost)
        db.session.commit()

    return render_template('set-post.html', params=params)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    err_msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        password = request.form['password']
        email = request.form['email']
        firstname = request.form['firstName']
        lastname = request.form['lastName']
        gender = request.form['inlineRadio']
        phone_no = request.form['phoneNumber']
        birth_date = request.form['birthdayDate']
        subject = request.form['chooseSubject']
        # cursor = mysql.connection.cursor(instance/codingthunder.db)
        # query = 'SELECT * FROM Signup_details WHERE email = email;'
        # cursor.execute(query)
        # account = cursor.fetchall()
        # if account:
        #     err_msg = 'Account already exists !'
        # elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        #     err_msg = 'Invalid email address !'
        # elif not password or not email:
        #     err_msg = 'Please fill out the form !'
        # else:
        entry_post = signupDetails(reg_email_id=email, reg_password=password, reg_frist_name=firstname, reg_last_name=lastname,
                                       reg_gender=gender, reg_phone_no=phone_no, reg_birth_date=birth_date, reg_subject=subject,
                                       reg_date=datetime.now())
        db.session.add(entry_post)
        db.session.commit()
        err_msg = 'You have successfully registered !'
    elif request.method == 'POST':
        err_msg = 'Please fill out the form !'
    return render_template('/login', params=params, msg=msg)

@app.route('/login')
def login():
    return render_template('login.html', params=params)


with app.app_context():
    db.create_all()
# ---------run the main file---------

if __name__ == '__main__':
    app.run(debug=True)
