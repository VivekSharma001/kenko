from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    weight=db.Column(db.Integer)
    height=db.Column(db.Integer)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    verified = db.Column(db.Integer, unique=False)
    token = db.Column(db.String(40), unique=True)
    profileimage=db.Column(db.LargeBinary)
    ext=db.Column(db.Text)

class Weight(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    value=db.Column(db.Integer)
    unit=db.Column(db.String(5),default="kg")
    month=db.Column(db.String(12))
    username=db.Column(db.String(150))

class Food(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.Text)
    calories=db.Column(db.Integer)
    username=db.Column(db.String(150))
    date_created=db.Column(db.DateTime(timezone=True),default=func.now())
    month=db.Column(db.String(12))