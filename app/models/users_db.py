from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    is_admin = db.Column(db.String(6), nullable=False)


class Users:
    def __init__(self, username: str, name: str, password: str,
                 email: str, trouth: bool = False):
        self.username = username
        self.name = name
        self.password = password
        self.email = email
        self.trouth = trouth

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @property
    def is_admin(self):
        if self.trouth:
            return True
        else:
            return False
