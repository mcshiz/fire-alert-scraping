from sqlalchemy import Table, Column, Integer, Text, String, Numeric, DateTime, MetaData
from base import Session, engine


class FireMap:
    def __init__(self):
        self.session = Session()
        self.metadata = MetaData(bind=engine)

        info_columns = {
            "lat": Numeric,
            "lon": Numeric,
            "name": String,
            "status": String,
            "unit_code": String,
            "acres": String,
            "inciweb_published_date": DateTime,
            "start_date": String,
            "last_updated": DateTime,
            "summary": Text,
            "remarks": Text,
            "location_description": Text,
            "containment": String,
            "ros": String,
            "roc": String,
            "alternate_name": String,
            "irwin_id": Integer,
            "complex_parent": String,
            "radio_frequency": String,
            "country": String,
            "state": String,
            "region": String,
            "county": String,
            "fire_number": Integer,
            "initial_attack_acres": String,
            "official_acres": String,
            "fuel_type": String,
            "land_owner": String,
            "life_threatened": String,
            "structures_threatened": String,
            "road_closures": String,
            "evacuations": String,
            "special_hazards": String,
            "injuries_reported": String,
            "national_preparedness_level": String,
            "details_summary": Text,
            "incident_commander": String,
            "type": String,
            "planned_actions": Text,
            "inciweb_url": String,
            "description": Text
        }

        self.table = Table('fires', self.metadata,
                           Column('id', Integer, primary_key=True),
                           Column('inciweb_id', Integer),
                           *(Column(detail, col_type) for detail, col_type in info_columns.iteritems()))
