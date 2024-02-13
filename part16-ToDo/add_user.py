from db import db
from app import app
from models import User

with app.app_context():
    new_user = User(username='newuser3')
    new_user.set_password('user1233') # 비밀번호를 해쉬화하는 부분이 추가되어야 함.
    db.session.add(new_user)
    db.session.commit()
    user = User.query.filter_by(username='newuser3').first()
    print(user)