from flask import Flask, request, render_template, redirect, flash, session
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User 

app = Flask(__name__)
# app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///users"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY']= "chiweeniesarecool"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False

# debug = DebugToolbarExtension(app)
app.app_context().push()

connect_db(app)

@app.route('/')
def list_users():
    """Shows list of users in db"""
    users = User.query.all()
    return render_template("list.html", users=users)

@app.route('/<int:user_id>')
def show_user(user_id):
    """SHow details about a single user"""
    user=User.query.get_or_404(user_id)
    return render_template("details.html", user=user)