from extensions import  db
from sqlalchemy import TIMESTAMP
from datetime import datetime

class Comment(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False, )
    ticked = db.Column(db.String(20), nullable=True)

    def __init__(self, _comment, _postId, _userId):
        self.comment = _comment
        self.user_id = _userId
        self.post_id = _postId
