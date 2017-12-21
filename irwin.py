import requests
import json
import time
import datetime

from sqlalchemy.sql import exists, func
from orm_mapper import FireMap
from fires_orm import Fires
from rss_name_maps import rss_to_db
from Logger import my_logger


# helper function for getting ms since epoch for today at 0:00:00
def get_ms_since_epoch():
    start_str = time.strftime("%m/%d/%Y") + " 00:00:00"
    start_ts = int(time.mktime(time.strptime(start_str, "%m/%d/%Y %H:%M:%S")))
    beginning_of_day_ms = start_ts * 1000
    return beginning_of_day_ms


ms = get_ms_since_epoch()
# where clauses params
today = "CreatedOnDateTime>%s" % 1512164907000
# today = "CreatedOnDateTime>%s" % ms
acres = "DailyAcres>=5"
category = "IncidentTypeCategory in ('WF')"
contained = "PercentContained<100"
out = "FireOutDateTime is NULL"
valid = "IsValid = 'true'"

# join the where clauses with +and+
conditions = [today, acres, category, contained, out, valid]
query_params_joined = '+and+'.join(map(str, conditions))

# request params
f = "f=json"
outfields = "outFields=*"
token = "token=-Daep_Z7OVI3jWDf-qrauV6UBkslgmPRAd1wEhZIm9poRBWc994CWDAQk6vxtTtOSbPlkSX8Gq51MRCZvnHaBHRxBmUe4udIVFE338HuMB0xVJ3ZxeROYQ-cc2EVS41xJiC52WVTwbpO1J0MjaNW8ZWGE-0kypK49pX-zOuarwZKLS7RlDM8rhIZE6hSFttuBIjO37bqoEvqRYOS8rAg7FHpMWf8iTUUtqW7pa_VvEw."
returnCountOnly = "returnCountOnly=true"

# join the request params with &
requestParams = [f, outfields, token]
params = '&'.join(map(str, requestParams))

# join the where clause and the request params with &where=
paramsString = params + '&where=' + query_params_joined

r = requests.get(
    'https://utility.arcgis.com/usrsvcs/servers/c1033dcbd3814f529d775d22c3b56c73/rest/services/Current_Wildland_Fires/FeatureServer/0/query',
    params=paramsString
    )
result = json.loads(r.text)

# Check for invalid token
# TODO need to figure out a way to generate a token
if 'error' in result and result['error']['message'] == "Invalid token.":
    my_logger("Invalid ARCGIS Token")
    exit(0)

# Check to make sure 'features' is in the response
if 'features' not in result:
    my_logger("Features not returned - %s" % result)
    exit(0)

features = result['features']
# Check to see if any features have been returned
if not features:
    my_logger("Nothing found in IRWIN")
    exit(0)
# Open up a connection to the DB
db = FireMap()
# initialize an empty list that will hold all of the objects so we can bulk insert with session.add_all(list)
information_objects_list = []

# Loop through each feature and add to DB
for feature in features:
    irwin_details = Fires()
    irwin_details.__setattr__('source', 'irwin')
    irwin_details.__setattr__('lat', feature['geometry']['y'])
    irwin_details.__setattr__('lon', feature['geometry']['x'])
    irwin_details.__setattr__('geom', func.ST_SetSRID(func.ST_MakePoint(feature['geometry']['x'], feature['geometry']['y']), 4326))
    attributes = feature['attributes']
    for attr, val in attributes.items():
        formatted_key = rss_to_db(attr)
        # print "%s - %s - %s" % (formatted_key, attr, val)
        if not formatted_key:
            continue
        elif formatted_key == 'state':
            val = val.split('-')[1]
        elif formatted_key == 'start_date' or formatted_key == 'estimated_contained_date' or formatted_key == 'published_date':
            seconds = val / 1000
            val = datetime.datetime.utcfromtimestamp(seconds).isoformat()
        irwin_details.__setattr__(formatted_key, val)
    if db.session.query(exists().where(Fires.irwin_id == irwin_details.irwin_id)).scalar():
        # UPDATE query
        # because we are dynamically iterating over all of the columns and updating the row with the most
        # current information, we have to get the ID because that comes from the DB and can't insert Null
        id = db.session.query(Fires).filter(Fires.irwin_id == irwin_details.irwin_id).first().id
        irwin_details.__setattr__('id', id)
        db.session.query(Fires).filter_by(irwin_id=irwin_details.irwin_id).update(
            {column: getattr(irwin_details, column) for column in Fires.__table__.columns.keys()}
        )
    else:
        # INSERT query
        information_objects_list.append(irwin_details)
try:
    db.session.add_all(information_objects_list)
except Exception as e:
    my_logger("Could not add IRWIN rows to DB")
    print(e)
try:
    db.session.commit()
except Exception as e:
    my_logger("Could not commit DB session")
    print(e)
db.session.close()


