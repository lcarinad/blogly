from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User 

app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///user_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY']= "chiweeniesarecool"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home():
    return '<h1>Homepage hi</h1>'