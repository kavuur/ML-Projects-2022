from extensions import  db
from sqlalchemy import TIMESTAMP
from datetime import datetime


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow, nullable=False, )

    def __init__(self, street, city, country, user_id):
        self.street = street
        self.city = city
        self.country = country
        self.user_id = user_id
