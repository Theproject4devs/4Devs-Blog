from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    is_admin = db.Column(db.String(6), nullable=False)




class Users:
    def __init__(self, name: str, trouth: bool = False):
        self.name = name
        self.trouth = trouth

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.name

    @property
    def is_admin(self):
        if self.trouth:
            return True
        else:
            return False
