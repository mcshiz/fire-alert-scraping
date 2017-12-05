from inciwebLogger import my_logger


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
        # only doing this to see if more columns are being added or I am missing some on
        # some fires so I can add them later.
        if key not in ["summary_detail", "links", "published_parsed", "guidislink", "title_detail", "where", "id"]:
            my_logger('Key Not Found %s' % key)
            return False