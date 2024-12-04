from database import get_engine, get_session, User
from flask import Flask
from flask_login import LoginManager

from app.config import Config, DevelopmentConfig


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    engine = get_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    app.config['SESSION_LOCAL'] = get_session(engine)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        with app.config['SESSION_LOCAL']() as session:
            return session.query(User).get(int(user_id))

    # Register blueprints (if any)
    from app.blueprints.auth import auth_bp
    app.register_blueprint(auth_bp)

    # Register routes
    from app.routes import main
    app.register_blueprint(main)

    return app
