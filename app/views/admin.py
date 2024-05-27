from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose, helpers
from flask import request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import form, fields, validators
import flask_login as login
from flask_login import login_required


TEMP_ADMIN_PASSWORD = generate_password_hash("temp")

class HookModelView(ModelView):
    column_list = ('id', 'last_update')


class CommandView(ModelView):
    column_list = ('id', 'command')
    form_columns = ('command',)

class LoginForm(form.Form):
    login = fields.StringField(validators=[validators.InputRequired()])
    password = fields.PasswordField(validators=[validators.InputRequired()])

    def validate_login(self):
        if not check_password_hash(TEMP_ADMIN_PASSWORD, self.password.data):
            raise validators.ValidationError('Invalid password')

# TODO : fix admin panel and make login simpler
class MyAdminIndexView(AdminIndexView):
    admin_is_logged_in = False

    @login_required
    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()
    
    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        if self.admin_is_logged_in:
            return 'One session is allowed', 403
        
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            self.admin_is_logged_in = True
            return redirect(url_for('.index'))
        
        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()
    
    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        self.admin_is_logged_in = False
        return redirect(url_for('.index'))