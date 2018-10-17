from models import Fema, State
from sqlalchemy import func


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
    - 'order': order results by state in ascending or descending order.
        Example:
            - asc
            - desc
    """

    result = None
    base_query = Fema.query.with_entities(
                Fema.fy_declared,
                Fema.state, Fema.incident_type)

    # Handle ordering by ascending or descending state name.
    if order == 'desc':
        base_query = base_query.order_by(Fema.state.desc())
    else:
        base_query = base_query.order_by(Fema.state.asc())

    # Handle filtering by year and/or disaster_type.
    if year and disaster_type:
        result = base_query.filter(
                Fema.fy_declared == year,
                Fema.incident_type == disaster_type)
    elif year:
        result = base_query.filter(Fema.fy_declared == year)
    elif disaster_type:
        result = base_query.filter(Fema.incident_type == disaster_type)
    # No filters have been applied so just return.
    elif not year or not disaster_type:
        return base_query

    return result


def get_joined_fema_data(year, order=None):
    result = None
    base_query = Fema.query.join(State).with_entities(
                Fema.state,
                func.max(State.state),
                func.max(Fema.fy_declared),
                func.max(Fema.incident_type),
                func.count(Fema.state)).group_by(Fema.state)

    # Handle ordering by ascending/descending state name
    # or ascending/descending disaster type.
    if order == 'state_desc':
        base_query = base_query.order_by(Fema.state.desc())
    elif order == 'disaster_desc':
        base_query = base_query.order_by(Fema.incident_type.desc())
    elif order == 'disaster_asc':
        base_query = base_query.order_by(Fema.incident_type.asc())
    else:
        base_query = base_query.order_by(Fema.state.asc())

    # Handle filtering by year.
    result = base_query.filter(
            Fema.fy_declared == year)

    return result
