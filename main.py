from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import sqlite3


with open("config.json", "r") as config:
    params = json.load(config)["params"]

local_server= True

db = SQLAlchemy()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db=SQLAlchemy(app)

if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params["local_server"]
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["prod_server"]


class Contacts(db.Model):
    contact_srno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact_name = db.Column(db.String(80), nullable=False)
    contact_phone_num = db.Column(db.String(12), nullable=False)
    contact_message= db.Column(db.String(120), nullable=False)
    contact_date = db.Column(db.String(12), nullable=False)
    contact_email = db.Column(db.String(20), nullable=True, unique=True)

class Post(db.Model):
    post_srno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_title = db.Column(db.String(1000), nullable=False)
    post_content = db.Column(db.String(5000), nullable=False)
    post_date = db.Column(db.String(20), nullable=True)
    
    
class SignupDetails(db.Model):
    srno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    frist_name = db.Column(db.String(30), nullable=False)
    last_lame = db.Column(db.String(30), nullable=False)
    gender = db.Column(db.String(12), nullable=False)
    phone_no = db.Column(db.Integer, nullable=False)
    birth_date = db.Column(db.String(12), nullable=False)
    date = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(20), nullable=True, unique=True)
    subject = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    
#create first app
@app.route('/')
def home():
    return render_template('index.html', params = params)


@app.route('/about')
def aboout():
    return render_template('about.html', params = params)


@app.route('/posts')
def post():
    return render_template('posts.html', params = params)


@app.route('/contact', methods = ['GET', 'POST'])
def Contact():
    if(request.method == 'POST'):
        
        name = request.form.get('name')
        phone_num = request.form.get('phone_num')
        message = request.form.get('message')
        email = request.form.get('email')

        entry = Contacts(contact_name=name, contact_phone_num=phone_num, contact_date=datetime.now(), contact_message=message, contact_email=email)
        db.session.add(entry)
        db.session.commit()

    
    return render_template('contact.html', params = params)

@app.route('/set-post', methods = ['GET', 'POST'])
def setPost():
    if(request.method == 'POST'):        
        title = request.form.get('title')
        content = request.form.get('content')

        entry_post = Post(post_title=title, post_date=datetime.now(), post_content=content)
        db.session.add(entryPost)
        db.session.commit()

    
    return render_template('set-post.html', params = params)


@app.route('/signup', methods = ['GET', 'POST'])
def signUp():
    msg = ''
    if (request.method == 'POST' and 'email' in request.form and 'password' in request.form):
        password = request.form['password']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        gender = request.form['inlineRadio']
        phoneNo = request.form['phoneNumber']
        birthDate = request.form['birthdayDate']
        # Query to check the email already available in database
        existing_email = SignupDetails.query.filter_by(email=email).first()
        print(existing_email)
        if existing_email == None:
            entryPost = Signup_details(email=email, password=password, fristName=firstName, lastName=lastName, gender=gender, phoneNo=phoneNo, birthDate=birthDate, subject=subject, date=datetime.now())
            db.session.add(entryPost)
            db.session.commit()
            msg = 'You have successfully registered !'
            return redirect('/login', params = params, registration_succ_msg = msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('signup.html', params = params, msg = msg)


@app.route('/login')
def login():
    if request == 'post':
        email = request.form['email']
        password = request.form['password']
            
    return render_template('login.html', params = params)


with app.app_context():
    db.create_all()
#---------run the main file--------- 

if __name__ == '__main__':
    app.run(debug = True)