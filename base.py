from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config_methods import config_section_map

db_user = config_section_map('database')['user']
db_password = config_section_map('database')['password']
db_name = config_section_map('database')['database']
db_host = config_section_map('database')['host']
db_port = config_section_map('database')['port']


url = 'postgresql://{}:{}@{}:{}/{}'
url = url.format(db_user, db_password, db_host, db_port, db_name)

# The return value of create_engine() is our connection object
engine = create_engine(url, client_encoding='utf8')
Session = sessionmaker(bind=engine)

Base = declarative_base()

