import feedparser
import urllib2
import httplib
import re
from bs4 import BeautifulSoup

from dateutil.parser import parse

from sqlalchemy.sql import exists
from orm_mapper import FireMap
from fires_orm import Fires
from rss_name_maps import rss_to_db
from Logger import my_logger
from config_methods import config_section_map

calfire_rss = config_section_map('calfire')['rss_url']

# open rss feed and parse it
calfire = feedparser.parse('%s' % calfire_rss)
if calfire.bozo:
    my_logger("could not open calfire feed %s" % calfire.bozo_exception)

# open up a database session (connection pool)
db = FireMap()

# initialize an empty list that will hold all of the objects so we can bulk insert with session.add_all(list)
information_objects_list = []
# iterate over each incident
for idx, incident in enumerate(calfire.entries):
    # this is used to map our objects to the Fires class (the table metadata)
    calfire_details = Fires()
    calfire_details.__setattr__('source', 'calfire')
    # we don't want to collect data on prescribed burns
    if incident.title.lower().find('prescribed') > -1:
        continue
    # Gather some elements from the RSS feed before opening the link and
    # Scraping the web page for the remaining elements (columns)
    for key, value in incident.iteritems():
        formatted_key = rss_to_db(key)
        if formatted_key:
            if formatted_key == "published_date":
                value = parse(value).isoformat()
            # Sometimes lat and lon are received as "-" or " "
            # we need to check for those cases by trying to cast to float
            # because they will cause errors when inserting into a Numeric column

            # fucking calfire has their RSS lat / lon reversed. Emailed them to fix it 12/10
            if formatted_key == "lat":
                try:
                    calfire_details.__setattr__('lon', float(value))
                except Exception:
                    value = None
                    calfire_details.__setattr__('lon', value)
            elif formatted_key == "lon":
                try:
                    calfire_details.__setattr__('lat', float(value))
                except Exception:
                    value = None
                    calfire_details.__setattr__('lat', value)
            else:
                calfire_details.__setattr__(formatted_key, value.encode("utf-8"))

    if hasattr(incident, 'link'):
        link = incident.link
        try:
            # the ID can be found at the end of the URL i.e
            # http://www.fire.ca.gov/current_incidents/incidentdetails/Index/1933
            # we only want the digits at the end - Using anchors to increase performance
            calfire_id = re.search('^.*/(\d+)$', link).group(1)
            calfire_details.__setattr__('calfire_id', calfire_id.encode("utf-8"))
        except AttributeError:
            my_logger("Could not parse calfire id %s" % link)
    else:
        # Skipping fires without links
        continue
    try:
        page = urllib2.urlopen(link)
    except urllib2.HTTPError, e:
        my_logger('HTTPError = %s - %s' % (str(e.code), link))
        continue
    except urllib2.URLError, e:
        my_logger('URLError = %s - %s' % (str(e.reason), link))
        continue
    except httplib.HTTPException, e:
        my_logger('HTTPException - %s' % link)
        continue
    except Exception:
        import traceback
        my_logger('generic exception: ' + traceback.format_exc())
        continue

    parsed = BeautifulSoup(page, 'html.parser')
    table = parsed.find_all('table', attrs={'id': 'incident_information'})
    title = parsed.find_all('h3', attrs={'class': 'incident_h3'})
    # get the title from the H3 tag
    if title is not None and title is not []:
        calfire_details.__setattr__('name', title[0].text)

    if table is None or not table:
        my_logger("Could not find content table %s" % link)
        continue

    for tags in table:
        rows = tags.find_all('tr')
        for row in rows:
            if row.select_one('td:nth-of-type(2)') is None:
                continue
            trLabel = row.select_one('td:nth-of-type(1)').text.replace(': ', '')
            trValue = row.select_one('td:nth-of-type(2)').text
            formatted_key = rss_to_db(trLabel)
            if formatted_key:
                if formatted_key == 'acres':
                    try:
                        # parse int from string
                        value = re.search(r'\d+(?:,\d+)?', trValue.text.replace(',', '')).group()
                    except Exception as e:
                        value = None
                    calfire_details.__setattr__(formatted_key, value)
                elif formatted_key == "start_date":
                    calfire_details.__setattr__(formatted_key, parse(trValue).isoformat())
                else:
                    calfire_details.__setattr__(formatted_key, trValue)
            elif trLabel == "Acres Burned - Containment":
                values = trValue.split('-')
                if len(values) == 2:
                    acres = re.search(r'\d+(?:,\d+)?', values[0].replace(',', '')).group()
                    calfire_details.__setattr__('acres', acres)
                    calfire_details.__setattr__('containment', values[1].strip())
        # check to see if this calfire_id is already in the DB
        if db.session.query(exists().where(Fires.calfire_id == calfire_details.calfire_id)).scalar():
            # UPDATE
            # because we are dynamically iterating over all of the columns and updating the row with the most
            # current information, we have to get the ID because that comes from the DB and can't insert Null
            id = db.session.query(Fires).filter(Fires.calfire_id == calfire_details.calfire_id).first().id
            calfire_details.__setattr__('id', id)
            db.session.query(Fires).filter_by(calfire_id=calfire_details.calfire_id).update(
                {column: getattr(calfire_details, column) for column in Fires.__table__.columns.keys()}
            )
        else:
            # INSERT
            information_objects_list.append(calfire_details)
try:
    db.session.add_all(information_objects_list)
except Exception as e:
    my_logger("Could not add calfire rows to DB")
    print(e)
try:
    db.session.commit()
except Exception as e:
    my_logger("Could not commit DB session")
    print(e)
db.session.close()


