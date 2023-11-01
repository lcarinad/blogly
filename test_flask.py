from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///users_test'
app.config['SQLALCHEMY_ECHO']=False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
                                
db.drop_all()
db.create_all()

class UsersTestCase(TestCase):

    def setUp(self):
        """Add sample user""" 
        User.query.delete()
        user = User(first_name='Doug', last_name='The Pug', image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Doug_the_Pug_NYC.jpg/440px-Doug_the_Pug_NYC.jpg")
        db.session.add(user)
        db.session.commit()        
          
        # post = Post(title='First Story Eva', content='Oh hai! This is my first story!', user_id='1')
        # db.session.add(post)
        # db.session.commit()
        
        self.user_id=user.id
        self.user=user
        # self.post_id=post.post_id
        # self.post=post
        
    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()
        
    def test_list_users(self):
        """Test that user li appear on /users route"""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Doug The Pug', html)

    def test_home(self):
        """Test to check root page gets redirected to /users"""
        with app.test_client() as client:
            resp = client.get("/")
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location,'/users')
            
    def test_submit_new_user(self):
        """test new user gets added"""
        with app.test_client() as client:
            d={"first_name":"Pumpkin", "last_name":"Bones"}
            resp=client.post('/users/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Pumpkin Bones", html)
            
        with app.test_client() as client:
            d={"first_name":"Pumpkin"}
            resp=client.post('/users/new', data=d, follow_redirects=True)
            self.assertEqual(resp.status_code, 404)
           
    
    def test_show_user(self):
        """Testing user details function"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Doug The Pug", html)
            
        with app.test_client() as client:
            resp = client.get(f"/users/100")
            self.assertEqual(resp.status_code, 404)
    
    def test_edit_submission(self):
        """test user edit"""
        with app.test_client() as client:
            d={"first_name":"Dougie", "last_name":"The Puggie"}
            resp = client.post(f"/users/{self.user_id}/edit", data=d)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Dougie The Puggie", html)
        
            
    def test_delete_user(self):
        """test user delete"""
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Doug The Pug", html)
            
           
   

