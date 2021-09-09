from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "demo.db"

def create_app():
    app = Flask(__name__)
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "fdafeset5jdfgfgb"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .template_rendering import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User

    create_database(app)

    lg = LoginManager()
    lg.login_view = "auth.login"
    lg.init_app(app)

    @lg.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created Database!")

