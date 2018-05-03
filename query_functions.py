from models import Fema
from sqlalchemy import extract


def get_fema_data(year=None, disaster_type=None, order=None):
    """Return a SQLAlchemy BaseQuery object of federally declared disasters.

    Optional paramters:
    - 'year': disasters that occurred in the year of interest.
        Example: 2013
    - 'disaster_type': disasters of a certain type.
        Example:
            - Chemical
            - Coastal Storm
            - Dam/Levee Break
            - Drought
            - Earthquake
            - Fire
            - Fishing Losses
            - Flood
            - Freezing
            - Human Cause
            - Hurricane
            - Mud/Landslide
            - Other
            - Severe Ice Storm
            - Severe Storm(s)
            - Snow
            - Terrorist
            - Tornado
            - Toxic Substances
            - Tsunami
            - Typhoon
            - Volcano
    - 'order': order results by date in ascending or descending order.
        Example:
            - asc
            - desc
    """

    result = None
    base_query = Fema.query.with_entities(
                Fema.incident_begin_date,
                Fema.state, Fema.incident_type)

    # Handle ordering by ascending or descending incident_begin_date.
    if order == 'asc':
        base_query = base_query.order_by(
                    Fema.incident_begin_date.asc(), Fema.state.asc())
    else:
        base_query = base_query.order_by(
                    Fema.incident_begin_date.desc(), Fema.state.asc())

    # Handle filtering by year and/or disaster_type.
    if year and disaster_type:
        result = base_query.filter(
                extract('year', Fema.incident_begin_date) == year,
                Fema.incident_type == disaster_type)
    elif year:
        result = base_query.filter(
                extract('year', Fema.incident_begin_date) == year)
    elif disaster_type:
        result = base_query.filter(Fema.incident_type == disaster_type)
    # No filters have been applied so just return.
    elif not year or not disaster_type:
        return base_query

    return result
