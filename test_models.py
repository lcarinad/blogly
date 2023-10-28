from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///users_test'
app.config['SQLALCHEMY_ECHO']=False

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Tests for model for users"""
    
    def setUp(self):
        """Before each test, clean up existing users"""
        User.query.delete()
        
    def tearDown(self):
        """Clean up any fouled transaction"""
        db.session.rollback()
        
    def test__repr(self):
        """test repr"""
        user = User(first_name="TestFirstName", last_name="TestLastName")
        expected_repr = '<User None TestFirstName TestLastName>'
        self.assertEqual(repr(user), expected_repr)