import click
from flask import Flask
from flask.cli import with_appcontext
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config
from utils import User, db, Server, Properties, Contracts

# Create the global objects
migrate = Migrate()
login = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['SESSION_COOKIE_SAME SITE'] = "Lax"
    app.config['SESSION_COOKIE_SECURE'] = False

    # Create and configure the app
    db.init_app(app)

    # init all the packages
    login.init_app(app)
    login.login_view = 'auth.login'
    login.login_message = 'Please log in to access this page.'

    migrate.init_app(app, db)

    # The user loader for flask_login
    @login.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    from blueprints.admin import bp as admin_bp
    from blueprints.auction import bp as auction_bp
    from blueprints.auth import bp as auth_bp
    from blueprints.contracts import bp as contracts_bp
    from blueprints.main import bp as main_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auction_bp, url_prefix='/auction')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(contracts_bp, url_prefix='/contracts')
    app.register_blueprint(main_bp, url_prefix='/')

    @app.cli.command('initdb')
    @with_appcontext
    def initdb():
        """Initialize the database."""
        db.create_all()
        click.echo('Initialized the database!')

    @app.cli.command("add_test_data")
    @with_appcontext
    def add_test_data():
        """Add test data to the database."""
        try:
            # Add Users
            user1 = User(username="happytrike", display_name="Happy Trike", discord_id=681072154019889173,
                         balance=10000)
            user2 = User(username="testuser2", display_name="Test User 2", discord_id=123456789012345678, balance=20000)
            db.session.add_all([user1, user2])
            db.session.commit()

            # Add Server
            server = Server(name="Test Server", ip="127.0.0.1", map="Default Map")
            db.session.add(server)
            db.session.commit()

            # Add Properties
            property1 = Properties(server_id=server.id, property_number=101, user_id=user1.id, image="image1.png",
                                   size=100, price=5000)
            property2 = Properties(server_id=server.id, property_number=102, user_id=None, image="image2.png",
                                   size=200, price=10000)
            db.session.add_all([property1, property2])
            db.session.commit()

            # Add Contracts
            contract = Contracts(user_id=user1.id, server_id=server.id, title="Test Contract",
                                 description="This is a test contract.", status="open", price=15000)
            db.session.add(contract)
            db.session.commit()

            click.echo("Test data added successfully!")

        except Exception as e:
            db.session.rollback()
            click.echo(f"Error adding test data: {e}")

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
