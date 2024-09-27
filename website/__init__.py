from flask import Flask
from flask_login import login_manager, LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_wtf.csrf import CSRFProtect


db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'AHSANPROJECTFL3ALAM'

    csrf = CSRFProtect(app)
    csrf.init_app(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DB_NAME
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .users_profile import users_profile

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(users_profile, url_prefix='/')

    from .models import User,Post,Like

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
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')