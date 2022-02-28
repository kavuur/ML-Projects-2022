from extensions import  db
from sqlalchemy import TIMESTAMP
from datetime import datetime


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False, )
    comments = db.relationship('Comment', backref='post')

    def __init__(self, title, body, _userId):
        self.title = title
        self.body = body
        self.user_id = _userId

