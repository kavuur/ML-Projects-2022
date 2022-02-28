from flask_login import UserMixin
from extensions import db, login_manager, bcrypt
from sqlalchemy import TIMESTAMP
from datetime import datetime

# Define models
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


@login_manager.user_loader
def get_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), unique=True, nullable=True)
    active = db.Column(db.Boolean())
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False, )
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    history = db.relationship('History', backref='user')
    posts = db.relationship('Post', backref='user')
    comments = db.relationship('Comment', backref='user')
    location = db.relationship('Location', backref='user', lazy=True)

    def __init__(self, username, email, password, roles, active=1, phone=None):
        self.username = username
        self.email = email
        self.password = password
        self.roles = roles
        self.active = active
        self.phone = phone


    def is_active(self):
        return True

    def __str__(self):
        return self.username

    @property
    def password_(self):
        raise AttributeError('password is not a readable attribute!')

    @password_.setter
    def password_(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def verify_password(self, pwd):
        return bcrypt.check_password_hash(self.password, pwd)

