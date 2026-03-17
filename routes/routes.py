from .logs_routes import logs_bp


def register_all_blueprints(app):
    app.register_blueprint(logs_bp)
