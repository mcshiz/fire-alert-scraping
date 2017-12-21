from sqlalchemy import Column, Numeric, String, DateTime, Text, Integer, func
from sqlalchemy.orm import column_property
from base import Base
import datetime
from geoalchemy2 import Geometry


class Fires(Base):
    __tablename__ = 'fires'
    id = Column(Integer, primary_key=True)
    scrape_date = Column(DateTime)
    source = Column(String, default=md)
    lat = Column(Numeric)
    lon = Column(Numeric)
    name = Column(String)
    acres = Column(Numeric)
    published_date = Column(DateTime)
    start_date = Column(String)
    last_updated = Column(DateTime)
    summary = Column(Text)
    remarks = Column(Text)
    location_description = Column(Text)
    containment = Column(String)
    estimated_contained_date = Column(DateTime)
    ros = Column(String)
    roc = Column(String)
    alternate_name = Column(String)
    country = Column(String)
    state = Column(String)
    region = Column(String)
    county = Column(String)
    fire_number = Column(String)
    initial_attack_acres = Column(Numeric)
    fuel_type = Column(String)
    conditions = Column(String)
    land_owner = Column(String)
    life_threatened = Column(String)
    structures_threatened = Column(String)
    structures_destroyed = Column(String)
    road_closures = Column(String)
    evacuations = Column(String)
    special_hazards = Column(String)
    injuries_reported = Column(String)
    details_summary = Column(Text)
    incident_commander = Column(String)
    type = Column(String)
    planned_actions = Column(Text)
    source_url = Column(String)
    irwin_id = Column(String)
    inciweb_id = Column(Integer)
    calfire_id = Column(Integer)
    description = Column(Text)
    geom = Column(Geometry)

    # by default set everything to null because not all fields will be populated all the time

    def __init__(self, scrape_date=datetime.datetime.now().isoformat(), source=None, lat=None, lon=None, name=None,
                 acres=None, published_date=None, start_date=None, last_updated=None,
                 summary=None, remarks=None, location_description=None, containment=None, estimated_contained_date=None, ros=None, roc=None,
                 alternate_name=None, country=None, state=None, region=None, county=None,
                 fire_number=None, initial_attack_acres=None, fuel_type=None, conditions=None,
                 land_owner=None, life_threatened=None, structures_threatened=None, structures_destroyed=None, road_closures=None,
                 evacuations=None, special_hazards=None, injuries_reported=None, details_summary=None,
                 incident_commander=None, type=None, planned_actions=None, irwin_id=None, inciweb_id=None, calfire_id=None,
                 source_url=None, description=None, geom=None):
        self.scrape_date = scrape_date
        self.source = source
        self.lat = lat
        self.lon = lon
        self.name = name
        self.acres = acres
        self.published_date = published_date
        self.start_date = start_date
        self.last_updated = last_updated
        self.summary = summary
        self.remarks = remarks
        self.location_description = location_description
        self.containment = containment
        self.estimated_contained_date = estimated_contained_date
        self.ros = ros
        self.roc = roc
        self.alternate_name = alternate_name
        self.country = country
        self.state = state
        self.region = region
        self.county = county
        self.fire_number = fire_number
        self.initial_attack_acres = initial_attack_acres
        self.fuel_type = fuel_type
        self.conditions = conditions
        self.land_owner = land_owner
        self.life_threatened = life_threatened
        self.structures_threatened = structures_threatened
        self.structures_destroyed = structures_destroyed
        self.road_closures = road_closures
        self.evacuations = evacuations
        self.special_hazards = special_hazards
        self.injuries_reported = injuries_reported
        self.details_summary = details_summary
        self.incident_commander = incident_commander
        self.type = type
        self.planned_actions = planned_actions
        self.source_url = source_url
        self.irwin_id = irwin_id
        self.inciweb_id = inciweb_id
        self.calfire_id = calfire_id
        self.description = description
        self.geom = geom
