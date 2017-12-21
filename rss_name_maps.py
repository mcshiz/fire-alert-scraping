from Logger import my_logger


def rss_to_db(key):
    mappings = {
        # INCIWEB
        "summary": "summary",
        "link": "source_url",
        "title": "name",
        "geo_lat": "lat",
        "geo_long": "lon",
        "published": "published_date",
        "Current as of": "last_updated",
        "Incident Type": "type",
        "Cause": "cause",
        "Date of Origin": "start_date",
        "Location": "location_description",
        "Size": "acres",
        "Percent of Perimeter Contained": "containment",
        "Estimated Containment Date": "estimated_containment_date",
        "Fuels Involved": "fuel_type",
        "Significant Events": "significant_events",
        "Incident Commander": "incident_commander",
        "Total Personnel": "total_personnel",
        "Planned Actions": "planned_actions",
        "Projected Incident Activity": "projected_activity",
        "Weather Concerns": "weather_concerns",
        "Remarks": "remarks",
        "Incident Description": "description",
        # CAL FIRE
        "pubDate": "published_date",
        "geo:lat": "lat",
        "geo:long": "lon",
        "Last Updated": "last_updated",
        "Date/Time Started": "start_date",
        "Administrative Unit": "incident_commander",
        "County": "county",
        "Structures Threatened": "structures_threatened",
        "Structures Destroyed": "structures_destroyed",
        "Evacuations": "evacuations",
        "Road Closures": "road_closures",
        "Conditions": "conditions",
        # IRWIN
        "DailyAcres": "acres",
        "FireDiscoveryDateTime": "start_date",
        "IncidentName": "name",
        "PrimaryFuelModel": "fuel_type",
        "IrwinID": "irwin_id",
        "POOState": "state",
        "POOCounty": "county",
        "POOCity": "city",
        "IncidentShortDescription": "location_description",
        "IncidentTypeCategory": "type",
        "FireBehaviorGeneral": "ros",
        "IncidentCommanderName": "incident_commander",
        "WeatherConcerns": "conditions",
        "PercentContained": "contained",
        "EstimatedContainmentDate": "estimated_contained_date",
        "CreatedOnDateTime": "published_date"
    }
    if key in mappings:
        return mappings[key]
    else:
        # only doing this to see if more columns are being added or I am missing some on
        # some fires so I can add them later.
        # Will stop logging before production
        if key not in ["summary_detail", "links", "published_parsed", "guidislink", "title_detail", "where", "id",
                       "Long/Lat", "Acres Burned - Containment"]:
            my_logger('Key Not Found %s' % key)
            return False
