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


db.init_app(app)


class Contacts(db.Model):
    srno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(20), nullable=True, unique=True)

class Post(db.Model):
    srno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(1000), nullable=False)
    content = db.Column(db.String(5000), nullable=False)
    date = db.Column(db.String(20), nullable=True)
    
    
class Signup_details(db.Model):
    srno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fristName = db.Column(db.String(30), nullable=False)
    lastName = db.Column(db.String(30), nullable=False)
    gender = db.Column(db.String(12), nullable=False)
    phoneNo = db.Column(db.Integer, nullable=False)
    birthDate = db.Column(db.String(12), nullable=False)
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

        entry = Contacts(name=name, phone_num=phone_num, date=datetime.now(), msg=message, email=email)
        db.session.add(entry)
        db.session.commit()

    
    return render_template('contact.html', params = params)

@app.route('/set-post', methods = ['GET', 'POST'])
def setPost():
    if(request.method == 'POST'):        
        title = request.form.get('title')
        content = request.form.get('content')

        entryPost = Post(title=title, date=datetime.now(), content=content)
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
        subject = request.form['chooseSubject']
        #cursor = mysql.connection.cursor(instance/codingthunder.db)
        query = 'SELECT * FROM Signup_details WHERE email = email;'
        cursor.execute(query)
        account = cursor.fetchall()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not password or not email:
            msg = 'Please fill out the form !'
        else:
            entryPost = Signup_details(email=email, password=password, fristName=firstName, lastName=lastName, gender=gender, phoneNo=phoneNo, birthDate=birthDate, subject=subject, date=datetime.now())
            db.session.add(entryPost)
            db.session.commit()
            msg = 'You have successfully registered !'
            return redirect('/login', params = params, msg = msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return redirect('/login', params = params, msg = msg)


@app.route('/login')
def login():
    return render_template('login.html', params = params)


with app.app_context():
    db.create_all()
#---------run the main file--------- 

if __name__ == '__main__':
    app.run(debug = True)