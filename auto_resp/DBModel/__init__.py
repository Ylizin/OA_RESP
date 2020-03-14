from . import InputMessage
# from .OutMessage import OutMessage
from sqlalchemy.ext.declarative import declarative_base 
Base = declarative_base()

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = r'mysql+pymysql://flask:flask_pwd@localhost:3306/flask'
engine = create_engine(DB_URL,encoding = 'utf-8')


Session = sessionmaker(bind=engine)

from contextlib import contextmanager
@contextmanager
def make_session():
    sess = Session()
    try:
        yield sess
        sess.commit()
    except:
        sess.rollback()
        raise
    finally:
        sess.close()
