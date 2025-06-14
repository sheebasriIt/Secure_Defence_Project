from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'admin' or 'uploader'

def add_user(username, password, role):
    hashed_password = generate_password_hash(password)
    user = User(username=username, password=hashed_password, role=role)
    db.session.add(user)
    db.session.commit()

def get_user(username):
    return User.query.filter_by(username=username).first()

def check_user_password(user, password):
    return check_password_hash(user.password, password)