from database import Database, Base
from database import UserRepository
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from config import Config

# Create the global objects
migrate = Migrate()
login = LoginManager()

db = Database(Config.SQLALCHEMY_DATABASE_URI)
session = db.get_session()


def create_app(config_class=Config):
    # Create and configure the app
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['SESSION_COOKIE_SAMESITE'] = "Lax"
    app.config['SESSION_COOKIE_SECURE'] = False

    # init all the packages
    login.init_app(app)
    login.login_view = 'auth.login'
    login.login_message = 'Please log in to access this page.'

    # The user loader for flask_login
    @login.user_loader
    def load_user(user_id):
        return UserRepository.get_user_by_id(session, user_id)

    from main import bp as main_bp
    app.register_blueprint(main_bp)

    from admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    @app.cli.command('initdb')
    def initdb():
        Base.metadata.create_all(bind=db.engine)

    return app


if __name__ == '__main__':
    application = create_app()
