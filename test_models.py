from unittest import TestCase


from app import app
from models import db, connect_db, User, Post

app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///users_test'
app.config['SQLALCHEMY_ECHO']=False

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Tests for model for users"""
    
    def setUp(self):
        """Before each test, clean up existing users"""
        db.session.rollback()
        
    def tearDown(self):
        """Clean up any fouled transaction"""
        db.session.rollback()
        
    def test__repr(self):
        """test repr"""
        user = User(first_name="TestFirstName", last_name="TestLastName")
        expected_repr = '<User None TestFirstName TestLastName>'
        self.assertEqual(repr(user), expected_repr)
        

        
class PostModelTestCase(TestCase):
    """Tests for model for posts"""

    def setUp(self):
        """Before each test, clean up existing posts and users"""
        db.session.rollback()

    def tearDown(self):
        """Clean up any fouled transaction"""
        db.session.rollback()

    def test__repr(self):
        """Test repr for the Post model"""
        user = User(first_name="TestFirstName", last_name="TestLastName")
        db.session.add(user)
        db.session.commit()

        post = Post(title="TestPostTitle", content="TestPostContent", user_id=user.id)
        db.session.add(post)
        db.session.commit()
        
   
        expected_repr = f'<Post: TestPostTitle, Created at: {post.created_at}, Created by: {user.id}>'
        self.assertEqual(repr(post), expected_repr)
        
    def test_relationship(self):
        """Test posts is associated with user"""
        user = User(first_name="TestFirstName", last_name="TestLastName")
        db.session.add(user)
        db.session.commit()

        
        post = Post(title="TestPostTitle", content="TestPostContent", user_id=user.id)
        db.session.add(post)
        db.session.commit()
        
        self.assertEqual(post.user, user)
        
        self.assertIn(post, user.posts)