from app.extensions import db
from datetime import datetime, timezone

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key =True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(10), nullable=False, default='active') 

    applications = db.relationship('ApplicationModel', back_populates='user', cascade='all, delete-orphan')