from os import getenv
from model import Base
from logger import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy.exc
from sqlalchemy_utils import database_exists, create_database
from dotenv import load_dotenv

load_dotenv()
try:
    engine = create_engine(f"postgresql+psycopg2://{getenv('POSTGRES_USER')}:"
                           f"{getenv('POSTGRES_PASSWORD')}@db:5432/property_rent")
    if not database_exists(engine.url):
        create_database(engine.url)
  
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    session.execute("SET datestyle = dmy")
    
except sqlalchemy.exc.OperationalError as error:
    print("Can't connect to database!")
    logging.error(str(error))
    exit()
