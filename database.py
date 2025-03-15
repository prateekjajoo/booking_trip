from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
import configparser

# Create a configparser object
config = configparser.ConfigParser()

# Read the config file
config.read('config.ini')


username = config['database']['username']
password = config['database']['password']
host = config['database']['host']
port = config['database']['port']
db_name = config['database']['database_name']

engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{db_name}', echo=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.
    # you will have to import them first before calling init_db()
    Base.metadata.create_all(bind=engine)