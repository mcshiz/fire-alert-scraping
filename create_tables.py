from database_connect import connect
from sqlalchemy import Table, Column, Integer, String, Numeric, DateTime, Text
from geoalchemy2 import Geometry
from config_methods import config_section_map

db_user = config_section_map('database')['user']
db_password = config_section_map('database')['password']
db_name = config_section_map('database')['database']
db_host = config_section_map('database')['host']
db_port = config_section_map('database')['port']


def create_table():
    con, meta = connect(db_user, db_password, db_name, db_host, db_port)
    fire = Table('fires', meta,
                 Column('id', Integer, primary_key=True),
                 Column('scrape_date', DateTime),
                 Column('source', String),
                 Column('lat', Numeric),
                 Column('lon', Numeric),
                 Column('name', String),
                 Column('acres', Numeric),
                 Column('published_date', DateTime),
                 Column('start_date', String),
                 Column('last_updated', DateTime),
                 Column('summary', Text),
                 Column('remarks', Text),
                 Column('location_description', Text),
                 Column('containment', String),
                 Column('estimated_contained_date', DateTime),
                 Column('ros', String),
                 Column('roc', String),
                 Column('alternate_name', String),
                 Column('country', String),
                 Column('state', String),
                 Column('city', String),
                 Column('region', String),
                 Column('county', String),
                 Column('fire_number', String),
                 Column('initial_attack_acres', Numeric),
                 Column('fuel_type', String),
                 Column('conditions', String),
                 Column('land_owner', String),
                 Column('life_threatened', String),
                 Column('structures_threatened', String),
                 Column('structures_destroyed', String),
                 Column('road_closures', String),
                 Column('evacuations', String),
                 Column('special_hazards', String),
                 Column('injuries_reported', String),
                 Column('details_summary', Text),
                 Column('incident_commander', String),
                 Column('type', String),
                 Column('planned_actions', Text),
                 Column('source_url', String),
                 Column('irwin_id', String),
                 Column('inciweb_id', Integer),
                 Column('calfire_id', Integer),
                 Column('description', Text),
                 Column('geom', Geometry('POINT', 4326), index=True)
                 )
    meta.create_all(con)

create_table()



