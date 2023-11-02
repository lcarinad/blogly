from datetime import datetime
from models import User, Post, db, Tag, PostTag
from app import app

db.drop_all()
db.create_all()

User.query.delete()

lauren = User(first_name = 'Lauren', last_name = 'DeLago-Mullins', image_url = 'https://images.zola.com/f8f41191-d519-41ae-9d41-24cc2d4479a5')

maria = User(first_name = 'Maria', last_name = 'Del Valle', image_url = 'https://www.musicconstructed.com/wp-content/uploads/2022/01/Maria-DelV-crop-295x300.png')

rosie = User(first_name = 'Rosie', last_name = 'The Dog')

db.session.add(lauren)
db.session.add(maria)
db.session.add(rosie)

db.session.commit()
p1 = Post(title='First Story', content='This is my first story!', user_id='1')
p2 = Post(title='I am a mom', content='My daughter is Imara', user_id='2')
p3=Post(title='I am a cat mom too!', content='My cats are black and very lovely', user_id='2')

db.session.add_all([p1, p2,p3])

db.session.commit()

t1 = Tag(name = 'Pets')
t2 = Tag(name='Daily Stuff')
t3=Tag(name='Careers')

db.session.add_all([t1, t2, t3])
db.session.commit()

pt1 = PostTag(post_id=p1.id, tag_id=t2.id) 
pt2 = PostTag(post_id=p2.id, tag_id=t2.id)
pt3= PostTag(post_id=p2.id, tag_id=t1.id)
pt4= PostTag(post_id=p3.id, tag_id=t1.id)

db.session.add_all([pt1, pt2, pt3, pt4])
db.session.commit()