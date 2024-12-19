from flask import Flask
from flask.cli import with_appcontext
from flask_login import LoginManager
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler
import click

from config import Config
from models import db, User, Server, Properties, Contracts, Savings

# Global objects
login = LoginManager()
migrate = Migrate()
scheduler = BackgroundScheduler()

# Flask app factory
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    login.login_view = "auth.login"
    login.login_message = "Please log in to access this page."

    # User loader
    @login.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # Register blueprints
    from blueprints.admin import bp as admin_bp
    from blueprints.auction import bp as auction_bp
    from blueprints.auth import bp as auth_bp
    from blueprints.bank import bp as bank_bp
    from blueprints.contracts import bp as contracts_bp
    from blueprints.main import bp as main_bp

    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(auction_bp, url_prefix="/auction")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(bank_bp, url_prefix="/bank")
    app.register_blueprint(contracts_bp, url_prefix="/contracts")
    app.register_blueprint(main_bp, url_prefix="/")

    # CLI commands
    @app.cli.command("initdb")
    @with_appcontext
    def initdb():
        """Initialize the database."""
        db.create_all()
        click.echo("Initialized the database!")

    @app.cli.command("add_test_data")
    @with_appcontext
    def add_test_data():
        """Add test data to the database."""
        try:
            # Add Users
            bank_user = User(username="bank", display_name="Bank", discord_id=1219655857315385436, balance=0)
            user1 = User(username="happytrike", display_name="Happy Trike", discord_id=681072154019889173, balance=10000)
            user2 = User(username="testuser2", display_name="Test User 2", discord_id=123456789012345678, balance=20000)
            db.session.add_all([bank_user, user1, user2])
            db.session.commit()

            # Add Server
            server = Server(name="Test Server", ip="127.0.0.1", map="Default Map")
            db.session.add(server)
            db.session.commit()

            # Add Properties
            property1 = Properties(server_id=server.id, property_number=101, user_id=user1.id, image="image1.png",
                                   size=100, price=5000)
            db.session.add(property1)
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

    # Scheduler task
    def calculate_interest():
        """Calculate and add monthly interest to savings accounts."""
        with app.app_context():
            interest_rate = 0.05 / 12  # 5% annual interest, divided by 12 months
            savings_accounts = Savings.query.all()

            for account in savings_accounts:
                if account.amount > 0:  # Only calculate interest for accounts with a balance
                    interest = account.amount * interest_rate
                    account.amount += interest

            db.session.commit()

    scheduler.add_job(func=calculate_interest, trigger="cron", hour=0, minute=0)

    # Shutdown scheduler on teardown
    @app.teardown_appcontext
    def shutdown_scheduler(exception=None):
        scheduler.shutdown()

    return app


# Run the app
if __name__ == "__main__":
    app = create_app(Config)
    scheduler.start()
    app.run(debug=True)
