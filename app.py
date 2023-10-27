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
def home():
    return redirect("/users")

@app.route('/users')
def list_users():
    """Shows list of users in db"""
    users = User.query.all()
    return render_template("list.html", users=users)

@app.route('/users/new')
def add_user():
    """shows add new user form"""
    return render_template("userform.html")

@app.route('/users/new', methods=["POST"])
def submit_new_user():
    """taking user input from form, send to users db, and redirect to /users"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")

@app.route('/<int:user_id>')
def show_user(user_id):
    """SHow details about a single user"""
    user=User.query.get_or_404(user_id)
    return render_template("details.html", user=user)