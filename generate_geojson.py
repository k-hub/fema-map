import json
import psycopg2
from psycopg2.extras import RealDictCursor

db_connect = psycopg2.connect('dbname=fema')
cursor = db_connect.cursor(cursor_factory=RealDictCursor)


def format_fema_query(full_state):
    """Generate SQL query to query fema db for disaster, year disaster was
    reported, and the number of incidences within a state in a given year.
    """

    query = """
        SELECT fema.fy_declared, MAX(fema.incident_type) as incident_type,
            COUNT(fema.fy_declared) as num_incidences
        FROM fema
        JOIN geo_states
        ON fema.state = geo_states.abbrev
        WHERE geo_states.state = '{}'
        GROUP BY fema.fy_declared
        ORDER BY fema.fy_declared
    """.format(full_state)

    return query


def format_state_abbrev_query(full_state):
    """Generate SQL query to query geo_states db for state and
    state abbreviation.
    """

    query = """
        SELECT geo_states.state as state, fema.state as abbreviation
        FROM fema
        JOIN geo_states
        ON fema.state = geo_states.abbrev
        WHERE geo_states.state = '{}'
    """.format(full_state)

    return query


def generate_replacement_properties(full_state):
    """Get SQL query results and format the data as a dictionary. This
    formatted data will replace respective properties for the input state
    within the geojson file.
    """
    # Fema results containing data from all years for a given state
    query = format_fema_query(full_state)
    cursor.execute(query)
    fema_data = cursor.fetchall()

    # State info containing full state name and state abbreviation
    state_query = format_state_abbrev_query(full_state)
    cursor.execute(state_query)
    state_info = cursor.fetchone()

    # Format json
    properties = {}
    event = []

    for data in fema_data:
        event.append({
            data['fy_declared']: {
                'disaster': data['incident_type'],
                'num_incidences': data['num_incidences']
            }
        })

    properties['abbreviation'] = state_info['abbreviation']
    properties['state'] = state_info['state']
    properties['event'] = event

    return (properties)


def read_and_write_json(output_geojson):
    """Read in a geojson file and write to a new geojson file. The
    output geojson file will contain properties regarding Fema disasters.
    """
    with open('us_sample.geojson', 'r') as sample_geojson_file:
        data = json.load(sample_geojson_file)

        for feature in data['features']:
            # Get state name to query. Overwrite the existing properties
            # with new properties needed to generate data on the map.
            state = feature['properties']['name']
            new_properties = generate_replacement_properties(state)
            feature['properties'] = new_properties

    fema_geojson_file = open(output_geojson, 'w')
    fema_geojson_file.write(json.dumps(data, indent=2))

    sample_geojson_file.close()
    fema_geojson_file.close()


# Generate the geojson file.
read_and_write_json('us_fema.geojson')
