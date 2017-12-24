from sqlalchemy import Table, Column, Integer, Text, String, Numeric, DateTime, MetaData, func
from geoalchemy2 import Geometry
from base import Session, engine
import datetime


class FireMap:
    def __init__(self):
        self.session = Session()
        self.metadata = MetaData(bind=engine)
        info_columns = {
            "source": String,
            "lat": Numeric,
            "lon": Numeric,
            "name": String,
            "acres": Numeric,
            "published_date": DateTime,
            "start_date": String,
            "last_updated": DateTime,
            "summary": Text,
            "remarks": Text,
            "location_description": Text,
            "containment": String,
            "estimated_contained_date": DateTime,
            "ros": String,
            "roc": String,
            "alternate_name": String,
            "country": String,
            "state": String,
            "city": String,
            "region": String,
            "county": String,
            "fire_number": Integer,
            "initial_attack_acres": String,
            "fuel_type": String,
            "land_owner": String,
            "life_threatened": String,
            "structures_threatened": String,
            "road_closures": String,
            "evacuations": String,
            "special_hazards": String,
            "injuries_reported": String,
            "details_summary": Text,
            "incident_commander": String,
            "type": String,
            "planned_actions": Text,
            "source_url": String,
            "irwin_id": String,
            "inciweb_id": Integer,
            "calfire_id": Integer,
            "description": Text,
            "hashtag": String
        }
        self.table = Table('fires', self.metadata,
                           # These are default values that are set every time
                           Column('id', Integer, primary_key=True),
                           Column('scrape_date', DateTime, default=datetime.datetime.now()),
                           # Column('name', String, default='cats')
                           # Here loop the the info_columns dict above and insert each one
                           * (Column(detail, col_type) for detail, col_type in info_columns.iteritems()))
