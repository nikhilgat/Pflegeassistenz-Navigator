from datetime import datetime
from sqlalchemy import JSON
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import uuid


from . import db

class Details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.String(10000))
    form_data = db.Column(JSON, default={})  
    response = db.Column(db.String(100000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    saved_choices = db.Column(JSON, default={})  
    is_complete = db.Column(db.Boolean, default=False)



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    unique_id = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()))
    full_name = db.Column(db.String(150))
    infos = db.relationship('Details')

    
    def get_id(self):
        return self.unique_id