import feedparser
import urllib2
import httplib
import re
from bs4 import BeautifulSoup
from dateutil.parser import parse
from sqlalchemy.orm import mapper, create_session

from inciwebLogger import my_logger
from config_methods import config_section_map
from db_insert import do_insert

db_user = config_section_map('database')['user']
db_password = config_section_map('database')['password']
db_name = config_section_map('database')['database']
inciweb_rss = config_section_map('inciweb')['rss_url']


# open rss feed and parse it
inciweb = feedparser.parse(inciweb_rss)


class InciwebInformation(object):
    pass

session, table = do_insert()
# map our custom object to our postgres table via sqlalchemy's mapper function
mapper(InciwebInformation, table)


def rss_to_db(key):
    mappings = {
        "summary": "summary",
        "link": "inciweb_url",
        "title": "name",
        "geo_lat": "lat",
        "geo_long": "lon",
        "published": "inciweb_published_date",
        "Current as of": "last_updated",
        "Incident Type": "type",
        "Cause": "cause",
        "Date of Origin": "start_date",
        "Location": "location_description",
        "Size": "acres",
        "Percent of Perimeter Contained": "percent_contained",
        "Estimated Containment Date": "estimated_containment_date",
        "Fuels Involved": "fuel_type",
        "Significant Events": "significant_events",
        "Incident Commander": "incident_commander",
        "Total Personnel": "total_personnel",
        "Planned Actions": "planned_actions",
        "Projected Incident Activity": "projected_activity",
        "Weather Concerns": "weather_concerns",
        "Remarks": "remarks",
        "Incident Description": "description"

    }
    if key in mappings:
        return mappings[key]
    else:
        if key not in ["summary_detail", "links", "published_parsed", "guidislink", "title_detail", "where", "id"]:
            my_logger('Key Not Found %s' % key)
            return False

# iterate over each incident
for idx, incident in enumerate(inciweb.entries):
    inciweb_details = InciwebInformation()
    for key, value in incident.iteritems():
        formatted_key = rss_to_db(key)
        if formatted_key:
            if formatted_key == "inciweb_published_date":
                value = parse(value).isoformat()
            inciweb_details.__setattr__(formatted_key,  value.encode("utf-8"))

    if hasattr(incident, 'link'):
        link = incident.link
        try:
            # the ID can be found at the end of the URL
            inciweb_id = re.search('.*/(\d+)/$', link).group(1)
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
        if tables is None:
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
                        inciweb_details.__setattr__(formatted_key, trValue.text.encode("utf-8"))

    # using our currently open session return from do_insert() we are going to iterate over all of the
    # items in our object and add them to their respective columns in the postgres table
    # up above there is a function called mapper() (part of sqlalchemy)
    # which is responsible for matching up the column names and the object names

    session.add(inciweb_details)
    session.commit()
    session.close()


