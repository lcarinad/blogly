from flask import Flask, request, render_template, redirect, flash, session
from datetime import datetime
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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
    image_url = request.form.get("image_url", None)
    
    if not first_name or not last_name:
        flash("Enter both name fields.")
        return redirect('users/new')
    
    if not image_url:
        default_image_url = User.image_url.default.arg
        image_url = default_image_url
    
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details about a single user"""
    user=User.query.get_or_404(user_id)
    post=Post.query.filter(Post.user_id == user.id).all()

    return render_template("details.html", user=user, posts=post)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Show edit form"""
    user=User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)

@app.route('/users/<int:user_id>/edit', methods= ["POST"])
def edit_submission(user_id):
    """User submits edit form"""
    user = User.query.get_or_404(user_id)
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form.get("image_url", None)
    
    if not first_name and last_name:
        flash("Enter both name fields." )
        return redirect(f'users/{user_id}/edit')
    
    if not image_url:
        default_image_url = User.image_url.default.arg
        image_url = default_image_url
    
    user.first_name=first_name 
    user.last_name=last_name
    user.image_url=image_url
   
    db.session.commit()
    return render_template("details.html", user=user)

@app.route('/users/<int:user_id>/delete', methods = ["POST"])
def delete_user(user_id):
    """Delete user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
        
    db.session.commit()
    return redirect ("/users")

@app.route("/users/<int:user_id>/posts/new")
def add_post(user_id):
    """shows add post form"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("postform.html", user= user, tags =tags)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def submit_post(user_id):
    """handles post submission"""
    user = User.query.get_or_404(user_id)
    post_title = request.form["post_title"]
    post_content=request.form["post_content"]
    created_at = Post.created_at.default.arg
    selected_tags = request.form.getlist("tag")
    
    if not post_title or not post_content:
        flash("Enter both fields.")
        return redirect(f'users/{user_id}/posts/new')
    
    new_post = Post(title=post_title, content=post_content, user_id=user_id)
    
    db.session.add(new_post)
    db.session.commit()
    
    for tag in selected_tags:
        tag_selection = Tag.query.get(tag)
        
        if tag_selection:
            new_post.tags.append(tag_selection)
            
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """shows single post"""

    post = Post.query.get_or_404(post_id)
    tags = post.tags
    return render_template("show_post.html",  post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit")
def show_edit_post_form(post_id):
    """shows form to edit post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template("edit_post.html", post = post, tags=tags)
    
@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """handles edit post form"""
    post = Post.query.get_or_404(post_id)
   
    post_title = request.form["post_title"]
    post_content=request.form["post_content"]
    selected_tags = request.form.getlist("tag")
    
    post.title=post_title
    post.content=post_content
    
    post.tags=[]
    for tag in selected_tags:
        tag_selection = Tag.query.get(tag)
        
        if tag_selection:
            post.tags.append(tag_selection)
    
    db.session.commit()
    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """handles post delete"""
    post = Post.query.get_or_404(post_id)
    
    db.session.delete(post)
    db.session.commit()
    return redirect("/users")

@app.route("/tags")
def show_tags_list():
    """Show list of all tags"""
    tags = Tag.query.all()
    return render_template("tags.html", tags=tags)

@app.route("/tags/<int:id>")
def show_tag(id):
    """ Shows single tag """
    tag = Tag.query.get_or_404(id)
    posts = tag.posts
    return render_template("show_tag.html", tag = tag, posts=posts)

@app.route("/tags/new")
def add_tag():
    """shows add tag form"""
    return render_template("tagform.html")

@app.route("/tags/new", methods=["POST"])
def submit_tag():
    """handle new tag form submission"""
    name = request.form["name"]
    if not name:
        flash("Enter a tag name")
        return redirect("/tags/new")
    
    new_tag = Tag(name=name)
    
    db.session.add(new_tag)
    db.session.commit()
    
    return redirect('/tags')

@app.route("/tags/<int:id>/edit")
def show_edit_tag_form(id):
    """Show edit form"""
    tag = Tag.query.get_or_404(id)
    
    return render_template('edit_tag.html', tag=tag)

@app.route("/tags/<int:id>/edit", methods=["POST"])
def edit_tag(id):
    """Edit tag name"""
    tag = Tag.query.get_or_404(id)
    name = request.form["name"]
    
    tag.name = name
    db.session.commit()
    
    return redirect('/tags')
    
@app.route("/tags/<int:id>/delete", methods=["POST"])
def delete_tag(id):
    """Delete a tag"""
    tag = Tag.query.get_or_404(id)
    
    db.session.delete(tag)
    db.session.commit()
  
    return redirect("/tags")