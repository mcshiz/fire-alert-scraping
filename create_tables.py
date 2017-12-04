from database_connect import connect
from sqlalchemy import Table, Column, Integer, String, Float, DateTime, Text
from config_methods import config_section_map

db_user = config_section_map('database')['user']
db_password = config_section_map('database')['password']
db_name = config_section_map('database')['database']


def create_table():
    con, meta = connect(db_user, db_password, db_name)
    fire = Table('fire', meta,
                 Column('id', Integer, primary_key=True, nullable=False),
                 Column('lat', Text),
                 Column('log', Text),
                 Column('name', Text),
                 Column('status', Text),
                 Column('unit_code', Text),
                 Column('acres', Text),
                 Column('inciweb_published_date', Text),
                 Column('start_date', Text),
                 Column('last_updated', Text),
                 Column('summary', Text),
                 Column('remarks', Text),
                 Column('location_description', Text),
                 Column('containment', Text),
                 Column('ros', Text),
                 Column('roc', Text),
                 Column('alternate_name', Text),
                 Column('irwin_id', Text),
                 Column('complex_parent', Text),
                 Column('radio_frequency', Text),
                 Column('inciweb_url', Text),
                 Column('country', Text),
                 Column('state', Text),
                 Column('region', Text),
                 Column('county', Text),
                 Column('fire_number', Text),
                 Column('initial_attack_acres', Text),
                 Column('official_acres', Text),
                 Column('fuel_type', Text),
                 Column('land_owner', Text),
                 Column('life_threatened', Text),
                 Column('structures_threatened', Text),
                 Column('road_closures', Text),
                 Column('evacuations', Text),
                 Column('special_hazards', Text),
                 Column('injuries_reported', Text),
                 Column('national_preparedness_level', Text),
                 Column('details_summary', Text),
                 Column('incident_commander', Text),
                 Column('type', Text),
                 Column('planned_actions', Text)
                 )
    meta.create_all(con)

create_table()



