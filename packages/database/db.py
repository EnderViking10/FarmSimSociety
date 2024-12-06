from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

Base = declarative_base()


class Database:
    def __init__(self, database_url: str = None):
        """
        Initialize the database connection.
        :param database_url: Optional URL for the database connection.
                             Defaults to an in-memory SQLite database.
        """
        if not database_url:
            database_url = "sqlite:///:memory:"  # Default to an in-memory SQLite database
        self.engine = create_engine(
            database_url,
            pool_pre_ping=True,
        )
        self.SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))

    def get_session(self):
        return self.SessionLocal()

    @contextmanager
    def session_scope(self):
        """
        Provide a transactional scope for a session.
        Automatically commits or rolls back transactions.
        """
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
