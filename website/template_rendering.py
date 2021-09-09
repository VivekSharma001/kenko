from website import DB_NAME, auth
from website.models import User,Weight
from flask import Blueprint, render_template, jsonify, flash,request,redirect,send_file,Response
from sqlalchemy.sql.functions import current_date, current_user, user
from sqlalchemy.sql.expression import join
from flask_login import login_required, current_user 
import smtplib
from io import BytesIO

views = Blueprint("template_rendering", __name__)
gmail_user = 'Altmail812@gmail.com'
gmail_password = 'dasfgsd32fdas'
def send_email(user_email, name,msg):
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(gmail_user, gmail_password)
        subject = 'User Query'
        body = f'{{msg}} sent by {{name}}({{user_email}}'
        msg = f'Subject: {subject}\n\n{body}'
        smtp.sendmail(gmail_user, 'technicalfriend.help@gmail.com', msg)
@views.route("/")
@views.route("/home",methods=['GET','POST'])
def home():
    if request.method=="GET":
        return render_template("home.html",user=current_user)
    elif request.method=="POST":
        email=request.form.get("email")
        name=request.form.get("name")
        msg=request.form.get("msg")
        send_email(user_email=email,name=name,msg=msg)


@views.route("/profile/<username>")
def dashboard(username):
    cuser=User.query.filter_by(username=username).first()
    if(bool(cuser)):
        uname=cuser.username
        weight=cuser.weight
        height=cuser.height
        m=(height/100)*(height/100)
        bmi=weight/m
        return render_template("profile.html",user=current_user,uname=uname,email=cuser.email,weight=weight,height=height,bmi=str(bmi),verified=bool(cuser.verified))
    else:
        flash("User Not Found",category="error")
        return redirect("/")

@views.route("/<username>/profileimage")
def serveprofileimage(username):
    cuser=User.query.filter_by(username=username).first()
    if(bool(cuser)):
        fname= cuser.username+str(cuser.id)+"."+cuser.ext
        img= send_file(BytesIO(cuser.profileimage),download_name=fname,as_attachment=False)
        return img

@views.route("/weight")
def weightpage():
  return render_template("weight.html",user=current_user)

@views.route("/food")
def foodpage():
  return render_template("food.html",user=current_user)


@views.route("/<name>/weights")
def weightdata(name):
    data={}
    wdata=Weight.query.filter_by(username=name).first()
    if(bool(wdata)):
        w=Weight.query.filter_by(username=name).all()
        for i in w:
            data[i.month]=i.value
        return jsonify(data)
    else:
        return jsonify({"Error":"Weight Doesn't Exist"})
