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

inciweb_rss = config_section_map('inciweb')['rss_url']

# open rss feed and parse it
inciweb = feedparser.parse('%s' % inciweb_rss)
if inciweb.bozo:
    my_logger("could not open inciweb feed %s" % inciweb.bozo_exception)

# open up a database session (connection pool)
db = FireMap()

# initialize an empty list that will hold all of the objects so we can bulk insert with session.add_all(list)
information_objects_list = []
# iterate over each incident
for idx, incident in enumerate(inciweb.entries):
    # this is used to map our objects to the Fires class (the table metadata)
    inciweb_details = Fires()
    inciweb_details.__setattr__('source', 'inciweb')
    # we don't want to collect data on prescribed burns
    if incident.title.lower().find('wildfire') == -1:
        continue
    # Gather some elements from the RSS feed before opening the link and
    # Scraping the web page for the remaining elements (columns)
    for key, value in incident.iteritems():
        formatted_key = rss_to_db(key)
        if formatted_key:
            if formatted_key == "inciweb_published_date":
                value = parse(value).isoformat()
            # Sometimes lat and lon are received as "-" or " "
            # we need to check for those cases by trying to cast to float
            # because they will cause errors when inserting into a Numeric column
            if formatted_key == "lat" or formatted_key == "lon":
                try:
                    inciweb_details.__setattr__(formatted_key, float(value))
                except Exception:
                    value = None
                    inciweb_details.__setattr__(formatted_key, value)
            else:
                inciweb_details.__setattr__(formatted_key,  value.encode("utf-8"))
    if hasattr(incident, 'link'):
        link = incident.link
        try:
            # the ID can be found at the end of the URL i.e https://inciweb.nwcg.gov/incident/5409/
            # we only want the digits at the end - Using anchors to increase performance
            inciweb_id = re.search('^.*/(\d+)/$', link).group(1)
            inciweb_details.__setattr__('inciweb_id',  inciweb_id.encode("utf-8"))
        except AttributeError:
            my_logger("Could not parse inciweb id %s" % link)
    else:
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
    content_div = parsed.find_all('div', attrs={'id': 'content'})

    if content_div is None:
        my_logger("Could not find content div %s" % link)
        continue
    for tag in content_div:
        tables = tag.find_all('table')
        # Sometimes, for some odd reason, I can't find any tables in the content div (even though they are there)
        # So I just have to search the whole document for tables then iterate over them.
        if not tables:
            tables = parsed.find_all('table')
        elif tables is None:
            my_logger("Could not find content tables %s" % link)
            continue
        for trTag in tables:
            rows = trTag.find_all('tr')
            if rows is None:
                continue
            for row in rows:
                trLabel = row.find('th').get_text()
                trValue = row.find('td')
                # parse the javascript date script
                if hasattr(trValue, 'contents') and trValue.contents[0].name == 'script':
                    try:
                        value = re.search('Date\(\"(.*?)\"\)', trValue.contents[0].text).group(1)
                    except AttributeError:
                        my_logger("Could not parse date %s" % link)
                        # continue to next table row
                        continue
                    formatted_key = rss_to_db(trLabel)
                    if formatted_key:
                        inciweb_details.__setattr__(formatted_key, value.encode("utf-8"))
                else:
                    formatted_key = rss_to_db(trLabel)
                    if formatted_key:
                        if formatted_key == 'acres':
                            try:
                                # parse int from string
                                value = re.search(r'\d+(?:,\d+)?', trValue.text.replace(',', '')).group()
                            except Exception as e:
                                value = None
                            inciweb_details.__setattr__(formatted_key, value)
                        else:
                            inciweb_details.__setattr__(formatted_key, trValue.text.encode("utf-8"))
        # check to see if this inciweb_id is already in the DB
        if db.session.query(exists().where(Fires.inciweb_id == inciweb_details.inciweb_id)).scalar():
            # UPDATE
            # because we are dynamically iterating over all of the columns and updating the row with the most
            # current information, we have to get the ID because that comes from the DB and can't insert Null
            id = db.session.query(Fires).filter(Fires.inciweb_id == inciweb_details.inciweb_id).first().id
            inciweb_details.__setattr__('id', id)
            db.session.query(Fires).filter_by(inciweb_id=inciweb_details.inciweb_id).update(
                {column: getattr(inciweb_details, column) for column in Fires.__table__.columns.keys()})
        else:
            # INSERT
            information_objects_list.append(inciweb_details)
try:
    db.session.add_all(information_objects_list)
except Exception as e:
    my_logger("Could not add Inciweb rows to DB")
    print(e)
try:
    db.session.commit()
except Exception as e:
    my_logger("Could not commit DB session")
    print(e)
db.session.close()


