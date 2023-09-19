# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# DB_URL = 'sqlite:///fastapidb.sqlite3'
DB_URL = 'mysql+mysqlconnector://deepak_shukla:deep70@radixusers2.com/deepak_shukla3'


engine = create_engine(DB_URL)
sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()