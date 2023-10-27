from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()

def connect_db(app):
    db.app=app
    db.init_app(app)
    
class User(db.model):
    __tablename__ = 'users'
    id=db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name=db.Column(db.String, nullable=False)
    last_name=db.Column(db.String, nullable=False)
    image_url=db.Column(db.String, nullable=False, default='https://static.thenounproject.com/png/4613680-200.png')