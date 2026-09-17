from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = "sqlite:///rangmanch.db"  # SQLite database file

engine = create_engine(DATABASE_URL, echo=True)  # Connect Python to SQLite DB

def create_tables():
    """Create all tables defined bt SQLModel Class"""
    SQLModel.metadata.create_all(engine)  # Create tables in DB


def get_session():
    """Dependency that provides a database session per request"""
    with Session(engine) as session:  # Create and manage session
        yield session  # Give session to the request
        

# This file is responsible for connecting your FastAPI application to the database and creating database sessions.