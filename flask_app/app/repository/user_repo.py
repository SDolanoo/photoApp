from flask_login import current_user
from sqlalchemy.orm import Session

from ..utils import convert_to_date

from ..models import Receipt, User


class UserRepo:
    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, id):
        return self.session.query(User).get(id)
    
    def find_by_email(self, email):
        return self.session.query(User).filter_by(email=email)

    def create(self, user: User):
        self.session.add(user)
        self.session.commit()
        
class UserRepoTest:
    def __init__(self, session: Session):
        self.session = session
    
    def create_users(self):
        user = User(email="email@address.cum", username="coollookingusername", password="supersecret123")
        one = User(email="one@address.cum", username="onecoollookingusername", password="supersecret123")
        two = User(email="two@address.cum", username="twocoollookingusername", password="supersecret123")
        three = User(email="three@address.cum", username="threecoollookingusername", password="supersecret123")
        four = User(email="four@address.cum", username="fourcoollookingusername", password="supersecret123")

        self.session.add_all([user, one, two, three, four])


        self.session.commit()


    def add_transactions(self, id):
        self.user_repo.add_transaction(id)



