from extensions import  db
from sqlalchemy import TIMESTAMP
from datetime import datetime


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    disease = db.Column(db.String(255), nullable=False)
    user_id = db.Column( db.Integer(), db.ForeignKey('user.id'))
    image_url = db.Column('image', db.String(255))
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False, )

    def __init__(self, disease, user_id, image):
        self.disease = disease
        self.user_id = user_id
        self.image_url = image
