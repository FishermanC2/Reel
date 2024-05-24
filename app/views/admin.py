from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash


class HookModelView(ModelView):
    column_list = ('id', 'last_update')


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        auth = request.authorization
        if auth and auth.username == 'admin':
            return check_password_hash(generate_password_hash("temp"), auth.password)
        return False