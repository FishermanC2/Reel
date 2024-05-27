from flask_admin.form import Select2Widget
from flask_admin.contrib.sqla import ModelView
from wtforms import SelectField
from wtforms.validators import InputRequired
from ..command.models import Command
from ..armory.parsers import Module
from flask import request, redirect, url_for
from flask_admin import AdminIndexView, helpers, expose
import flask_login as login
from wtforms import form, fields, validators
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm

TEMP_ADMIN_PASSWORD = generate_password_hash("temp")

class LoginForm(form.Form):
    login = fields.StringField(validators=[validators.InputRequired()])
    password = fields.PasswordField(validators=[validators.InputRequired()])

    def validate_login(self):
        if not check_password_hash(TEMP_ADMIN_PASSWORD, self.password.data):
            raise validators.ValidationError('Invalid password')

class FishermanIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(FishermanIndexView, self).index()
    
    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            self.admin_is_logged_in = True
            return redirect(url_for('.index'))
        
        self._template_args['form'] = form
        return super(FishermanIndexView, self).index()
    
    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


class CommandForm(FlaskForm):
    id = SelectField('Command ID', coerce=int, validators=[InputRequired()])
    module = SelectField('Module', choices=[(module.value, module.name) for module in Module], validators=[InputRequired()])

class CommandAdminView(ModelView):
    column_list = ('id', 'command')
    form_columns = ('id', 'command')
    

    
class HookAdminView(ModelView):
    column_list = ('id', 'ip_address', 'user_agent', 'screen_resolution', 'browser_plugins', 'language', 'timezone', 'last_update')
    