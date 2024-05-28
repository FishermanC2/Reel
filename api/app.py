from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    # Initialize extensions
    from .extensions import db, login_manager, cors
    db.init_app(app)
    login_manager.init_app(app)
    cors.init_app(app, supports_credentials=True)

    # Set up nginx reverse proxy
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )

    # Register blueprints
    from .home import bp as home_bp
    app.register_blueprint(home_bp)

    from .hook import bp as hook_bp
    app.register_blueprint(hook_bp, name='hook_bp', url_prefix='/hook')

    from .command import bp as command_bp
    app.register_blueprint(command_bp, name='command_bp', url_prefix='/command')

    # Setup admin panel
    from flask_admin import Admin as FlaskAdmin
    from .admin.views import HookAdminView, CommandAdminView, AttacksView
    from .admin.views import FishermanIndexView
    from .hook.models import Hook
    from .command.models import Command
    admin = FlaskAdmin(app, index_view=FishermanIndexView(), name="Fisherman's Boat", template_mode='bootstrap3')
    admin.add_view(HookAdminView(Hook, db.session))
    admin.add_view(CommandAdminView(Command, db.session))
    admin.add_view(AttacksView(name='Attacks', endpoint='attacks'))

    from .admin.models import Admin
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(Admin).get(user_id)
    
    with app.app_context():
        db.create_all()
        return app
    











