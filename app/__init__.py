from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from settings import settings

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def unauthorized(e):
    render_template("assets/error_pages/403.html"), 403


def page_not_found(e):
    return render_template("assets/error_pages/404.html"), 404


def international_server_error(e):
    return render_template("assets/error_pages/500.html", e=e), 500


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    app.register_error_handler(403, unauthorized)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, international_server_error)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Bu Sayfaya Erişmek İçin Giriş Yapmanız Gerekmektedir.'
    login_manager.login_message_category = 'info'

    from app.routes.main import main as bp_main
    app.register_blueprint(bp_main)  # url_prefix = "/"

    from app.routes.auth import auth as bp_auth
    app.register_blueprint(bp_auth)  # url_prefix = "/auth"

    from app.routes.user import user as bp_user
    app.register_blueprint(bp_user)  # url_prefix = "/user"

    from app.routes.task import task as bp_task
    app.register_blueprint(bp_task)  # url_prefix = "/task"

    from app.routes.report import report as bp_report
    app.register_blueprint(bp_report)  # url_prefix = "/report"

    from app.routes.count import count as bp_count
    app.register_blueprint(bp_count)  # url_prefix = "/count"

    return app
