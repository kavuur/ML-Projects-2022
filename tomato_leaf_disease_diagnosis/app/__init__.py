import os
from flask import Flask
from flask_security.utils import hash_password
from wtforms import StringField, DateField, RadioField
from wtforms.validators import DataRequired as Required
from models.role import Role
from models.user import User
from models.location import Location
from models.history import History
from models.post import Post
from models.comment import Comment
from main.routes import main
from farmer.routes import farmer
from admin.routes import admin
from admin.routes import admin
from flask_security import Security, SQLAlchemyUserDatastore, RegisterForm, user_registered
from extensions import db, login_manager, bcrypt

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True, static_url_path='',
                static_folder='../static', template_folder='../templates')

    if test_config is None:
        app.config.from_pyfile("../config.py")
        print('------configuration----------')
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    login_manager.login_view = 'login'
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(farmer, url_prefix='/farmer')
    app.register_blueprint(admin, url_prefix='/admin')

    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    @user_registered.connect_via(app)
    def user_registered_sighandler(app, user, confirm_token):
        user_role = user_datastore.find_role("farmer")
        user_datastore.add_role_to_user(user, user_role)
        db.session.commit()

    def build_sample_db():
        """
            Populate a small db with some example entries.
        """
        with app.app_context():
            db.drop_all()
            db.create_all()
            farmer_role = Role(name='farmer')
            admin_role = Role(name='admin')

            db.session.add(farmer_role)
            db.session.add(admin_role)

            admin = user_datastore.create_user(
                username='admin',
                email='admin@smartfarming.com',
                phone='0777547547',
                password=bcrypt.generate_password_hash('pass@admin'),
                roles=[admin_role]
            )
            """
            print(' --- ADMIN ROLE ---')
            doctor1 = user_datastore.create_user(
                username='samuel',
                email='samuel@med.com',
                phone='0713222556',
                password=hash_password('pass@doctors'),
                roles=[doctor_role]
            )
            print(' --- DOCTOR ROLE ---')
            farmer1 = user_datastore.create_user(
                username='henry',
                email='henry@med.com',
                phone='0714222555',
                password=hash_password('pass@farmer'),
                roles=[farmer_role]
            )
            print(' --- farmer 1 ROLE ---')
            farmer2 = user_datastore.create_user(
                username='leon',
                email='leon@med.com',
                phone='0719262557',
                password=hash_password('pass@farmer'),
                roles=[farmer_role]
            )
            print(' --- farmer 2 ROLE ---')
            print(' --- Before commit ---')"""
            db.session.commit()
            print(' --- After commit ---')
        return
    #build_sample_db()
    return app

