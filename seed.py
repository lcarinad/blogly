from models import User, db
from app import app

db.drop_all()
db.create_all()

User.query.delete()

lauren = User(first_name = 'Lauren', last_name = 'DeLago-Mullins', image_url = 'https://i.imgur.com/YQdXhf6.jpg')

maria = User(first_name = 'Maria', last_name = 'Del Valle', image_url = 'https://i.imgur.com/axHE1cV.png')

rosie = User(first_name = 'Rosie', last_name = 'The Dog')

db.session.add(lauren)
db.session.add(maria)
db.session.add(rosie)

db.session.commit()