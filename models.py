from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()

def connect_db(app):
    db.app=app
    db.init_app(app)
    
class User(db.Model):
    __tablename__ = 'users'
    id=db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name=db.Column(db.String, nullable=False)
    last_name=db.Column(db.String, nullable=False)
    image_url=db.Column(db.String, nullable=False, default='https://static.thenounproject.com/png/4613680-200.png')
    
    def __repr__(self):
        """show info about user"""
        u = self
        return f"<User {u.id} {u.first_name} {u.last_name}>"
    
class Post(db.Model):
    __tablename__='posts'
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    title=db.Column(db.String(30), nullable=False)
    content=db.Column(db.String(150), nullable=False)
    created_at=db.Column(db.DateTime, default=lambda: datetime.utcnow())
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))
    
    user = db.relationship('User', backref='posts')
    
    def __repr__ (self):
        return f"<Post: {self.title}, Created at: {self.created_at}, Created by: {self.user_id}>"