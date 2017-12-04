from sqlalchemy.orm import mapper, create_session
from sqlalchemy import Table, Column, Integer, Text, MetaData, create_engine
from config_methods import config_section_map

db_user = config_section_map('database')['user']
db_password = config_section_map('database')['password']
db_name = config_section_map('database')['database']

def do_insert():

    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(db_user, db_password, 'localhost', 5432, db_name)

    # The return value of create_engine() is our connection object
    con = create_engine(url, client_encoding='utf8')
    metadata = MetaData(bind=con)

    info_columns = [
        "lat",
        "lon",
        "name",
        "status",
        "unit_code",
        "acres",
        "inciweb_published_date",
        "start_date",
        "last_updated",
        "summary",
        "remarks",
        "location_description",
        "containment",
        "ros",
        "roc",
        "alternate_name",
        "irwin_id",
        "complex_parent",
        "radio_frequency",
        "inciweb_url",
        "country",
        "state",
        "region",
        "county",
        "fire_number",
        "initial_attack_acres",
        "official_acres",
        "fuel_type",
        "land_owner",
        "life_threatened",
        "structures_threatened",
        "road_closures",
        "evacuations",
        "special_hazards",
        "injuries_reported",
        "national_preparedness_level",
        "details_summary",
        "incident_commander",
        "type",
        "planned_actions",
        "inciweb_url",
        "inciweb_id",
        "description"
    ]

    table = Table('fires', metadata,
              Column('id', Integer, primary_key=True),
              *(Column(detail, Text) for detail in info_columns))

    metadata.create_all()

    insert_session = create_session(bind=con, autocommit=False, autoflush=True)
    return insert_session, table

