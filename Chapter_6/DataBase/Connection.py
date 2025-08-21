from .Employees import Employees
from .PayGrades import PayGrades
Listing 6-5 DataBase/__init__.py
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

engine = create_engine("postgresql://postgres:admin@127.0.0.1:5432/CompanyData")
DBSession = sessionmaker(bind=engine)


@contextmanager
def session_manager() -> Session:
    session = DBSession()
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
