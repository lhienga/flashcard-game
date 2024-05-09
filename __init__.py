from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, current_user
from sqlalchemy import update
from sqlalchemy import schema, create_engine


db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    # app.config['UPLOAD_FOLDER'] = "static/uploads"
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)
    
    #from app import app
    from auth import auth
    
    #app.register_blueprint(app, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from models import User
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('database/' + DB_NAME):
        db.create_all(app=app)
