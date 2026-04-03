from .logs_routes import logs_bp

from .auth.register_page import register_bp
from .auth.login_page import login_bp

from .html.jobs_routes import job_bp
from .html.departments_routes import department_bp
from .html.categories_routes import category_bp
from .html.users_routes import user_bp
from .html.user_map import user_map_bp

from .api import api_bp

from .api.v2 import init_api_v2


def register_all_blueprints(app):
    app.register_blueprint(logs_bp)

    app.register_blueprint(register_bp)
    app.register_blueprint(login_bp)

    app.register_blueprint(job_bp)
    app.register_blueprint(department_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(user_map_bp)

    app.register_blueprint(api_bp)

    init_api_v2(app)
