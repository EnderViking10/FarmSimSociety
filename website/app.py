from getpass import getpass

from database import Base, get_engine, get_session, User
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash

from app import create_app

app = create_app()


@app.cli.command("initdb")
def init_db():
    """Initialize the database."""
    engine = get_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    try:
        Base.metadata.create_all(bind=engine)
        print("Database initialized successfully!")
    except SQLAlchemyError as e:
        print(f"Error initializing the database: {e}")


@app.cli.command("createuser")
def create_user():
    """Create a new user."""
    engine = get_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    session_local = get_session(engine)

    username = input("Enter username: ")
    password = getpass("Enter password: ")
    admin = input("Is admin (Y/n): ")
    if admin.lower() == "y":
        admin = True
    elif admin.lower() == "n":
        admin = False
    else:
        admin = False

    with session_local() as session:
        user = User(
            username=username,
            password=generate_password_hash(password),
            is_admin=admin,
            discord_id=11111
        )
        session.add(user)
        session.commit()
        role = "Admin" if admin else "Regular"
        print(f"{role} user '{username}' created successfully!")


if __name__ == "__main__":
    app.run()
