from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'kjgajgfksaffsa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)

from app.controllers import default
from app.models.users_db import User


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect("/")
        elif not current_user.is_admin:
            return redirect("/")
        return super(MyAdminIndexView, self).index()


admin = Admin(app, name='Admin', template_mode='bootstrap3', index_view=MyAdminIndexView())
admin.add_view(ModelView(User, db.session))
