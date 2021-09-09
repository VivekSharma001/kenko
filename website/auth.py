from flask import Blueprint, render_template, redirect, url_for, request, flash
from sqlalchemy.sql.expression import join
import smtplib
from sqlalchemy.sql.functions import current_date, current_user, user
from . import db
import random
from .models import User
from flask_login import login_user, logout_user, login_required, current_user 
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)
gmail_user = 'Altmail812@gmail.com'
gmail_password = 'dasfgsd32fdas'

@auth.route("/login", methods=['GET', 'POST'])
def login():
  try:
    a = current_user.username
    flash("You are already logged in!")
    return redirect(url_for("template_rendering.home"))
  except AttributeError:
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = User.query.filter_by(username = username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('template_rendering.home'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Userdoes not exist', category='error')

    return render_template("login.html",user=current_user)

@auth.route("/register", methods=['GET', 'POST'])
def register():
  try:
    a = current_user.username
    flash("You are already logged in!")
    return redirect(url_for("template_rendering.home"))
  except AttributeError:
    if request.method == 'POST':
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")
            pimage=request.files['pimage']
            password1 = request.form.get("password1")
            weight=request.form.get("weight")
            height=request.form.get("height")
            ext=pimage.filename.split(".")[len(pimage.filename.split("."))-1]
            email_exists = User.query.filter_by(email=email).first()
            username_exists = User.query.filter_by(username=username).first()
            if email_exists:
                flash('Email is already in use.', category='error')
            elif username_exists:
                flash('Username is already in use.', category='error')
            elif password1 != password:
                flash('Password don\'t match!', category='error')
            elif len(username) < 2:
                flash('Username is too short.', category='error')
            elif len(password) < 8:
                flash('Password is too short.', category='error')
            elif len(email) < 10:
                flash('Email is invalid.', category='error')
            else:
                token = generate_token()
                token_exists = User.query.filter_by(token=converter(token)).first()
                while(token_exists):
                    generate_token()
                else:
                    new_user = User(email=email,weight=weight, username=username,height=height, password=generate_password_hash(password, method='sha256'),verified = 0, token=converter(token),profileimage=pimage.read(),ext=ext)
                    db.session.add(new_user)
                    db.session.commit()
                    login_user(new_user, remember=True)
                    send_email(email,'http://kenko.technicalfriend.repl.co/verify/' + converter(token))
                    flash('User created!, Check your mail ID to verify your account', category='success')
                    return redirect(url_for('template_rendering.home'))

    return render_template("register.html",user=current_user)

def send_email(user_email, link):
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(gmail_user, gmail_password)
        subject = 'Email verification'
        body = f'Hi,\n Click the link to complete your registration process: {link}\n\n\n\n\nNote this mail was sent automatically, for any queries contact website owner (aka me)'
        msg = f'Subject: {subject}\n\n{body}'
        smtp.sendmail(gmail_user, user_email, msg)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', category='success')
    return redirect(url_for("template_rendering.home"))

def generate_token():
    token = [1]
    x = 0
    while(x < 39 ):
        x = x+1
        a = random.randint(0, 9)
        token.append(a)
    return token

def converter(a):
    mystring = ''.join(map(str,a))
    print(mystring)
    print(type(mystring))
    return mystring

@auth.route("/verify/<name>")
def verify(name):
    user = User.query.filter_by(token=name).first()
    if(user.token):
        if(user.verified == 0):
            user.verified = 1
            db.session.commit()
            flash('Your account is now verified.', category="success")
            return render_template("verified.html",user=current_user)
        else:
            flash("Your account is already Verified!", category="error")
            return render_template("verified.html",erroris=True)
    else:
        flash("Please Check the link you followed.", category="error")
        return render_template("verified.html")
