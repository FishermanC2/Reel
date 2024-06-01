from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    # Initialize extensions
    from .extensions import db, cors, auth, socketio
    db.init_app(app)
    cors.init_app(app, supports_credentials=True)
    auth.init_app(app)
    socketio.init_app(app)

    # Set up nginx reverse proxy
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )

    def color_from_index(index):
        colors = ['#FF847C', '#FCCB8C', '#FFD166', '#A0E7E5', '#7ED6DF', '#B2B1CF']  # Darker pastel colors
        return colors[index % len(colors)]

    # Register the custom filter with Jinja2
    app.jinja_env.filters['color_from_index'] = color_from_index

    # Register blueprints
    from .home import bp as home_bp
    app.register_blueprint(home_bp)

    from .hook import bp as hook_bp
    app.register_blueprint(hook_bp, name='hook_bp', url_prefix='/hook')

    from .command import bp as command_bp
    app.register_blueprint(command_bp, name='command_bp', url_prefix='/command')

    from .admin import bp as admin_console_bp
    app.register_blueprint(admin_console_bp, name='admin_console_bp', url_prefix='/admin')

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
    
    with app.app_context():
        db.create_all()
        return app, socketio
    











