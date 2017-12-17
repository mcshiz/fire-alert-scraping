from database_connect import connect
from sqlalchemy import Table, Column, Integer, String, Numeric, DateTime, Text
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
                 Column('last_modified', DateTime),
                 Column('lat', Numeric),
                 Column('lon', Numeric),
                 Column('name', String),
                 Column('status', String),
                 Column('unit_code', String),
                 Column('acres', Numeric),
                 Column('inciweb_published_date', DateTime),
                 Column('start_date', String),
                 Column('last_updated', DateTime),
                 Column('summary', Text),
                 Column('remarks', Text),
                 Column('location_description', Text),
                 Column('containment', String),
                 Column('ros', String),
                 Column('roc', String),
                 Column('alternate_name', String),
                 Column('irwin_id', Integer),
                 Column('complex_parent', String),
                 Column('radio_frequency', String),
                 Column('inciweb_url', String),
                 Column('country', String),
                 Column('state', String),
                 Column('region', String),
                 Column('county', String),
                 Column('fire_number', String),
                 Column('initial_attack_acres', Numeric),
                 Column('official_acres', Numeric),
                 Column('fuel_type', String),
                 Column('land_owner', String),
                 Column('life_threatened', String),
                 Column('structures_threatened', String),
                 Column('road_closures', String),
                 Column('evacuations', String),
                 Column('special_hazards', String),
                 Column('injuries_reported', String),
                 Column('national_preparedness_level', String),
                 Column('details_summary', Text),
                 Column('incident_commander', String),
                 Column('type', String),
                 Column('planned_actions', Text),
                 Column('inciweb_id', Integer),
                 Column('inciweb_url', String),
                 Column('description', Text),
                 )
    meta.create_all(con)

create_table()



