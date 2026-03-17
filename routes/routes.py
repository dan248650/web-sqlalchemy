from .logs_routes import logs_bp
from .auth.register_page import register_bp


def register_all_blueprints(app):
    app.register_blueprint(logs_bp)
    app.register_blueprint(register_bp)
