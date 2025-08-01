#Paso 3: Cracion de base de datos con Flask y SQLALchemy 
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    tasks = db.relationship('Task', backref='owner', lazy=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username
        }

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id, 
            "title": self.title, 
            "completed": self.completed,
            "user_id": self.user_id
        }