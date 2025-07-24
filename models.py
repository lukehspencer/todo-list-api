# User and todo models

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt() # password hashing and checking
jwt = JWTManager() # JSON Web Token Manager
db = SQLAlchemy() # sqlalchemy database

class UserModel(db.Model):
    __tablename__ = "users"
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password) # generate password hash (covers it in random text)

    def check_password(self, password): # checks if the password matches the password has
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"User({self.uid}, {self.username}, {self.password})"

class TodoModel(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f"Task({self.id}, {self.title}, {self.description})"