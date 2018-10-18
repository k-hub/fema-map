import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from helpers.disasters_map import get_formatted_disaster_name


app = Flask(__name__)

# To set the environment variables, use autoenv:
#   $ echo "source `which activate.sh`" >> ~/.bashrc
#   $ source ~/.bashrc
app.config.from_object(os.environ['APP_SETTINGS'])
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# app.config['SQLALCHEMY_BINDS'] = {
#     'coordinates': os.environ['COORDINATES_DATABASE_URL']}
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///fema"
app.config['SQLALCHEMY_BINDS'] = {
    'coordinates': "postgresql:///fema"}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
db.Model.metadata.reflect(db.engine)


@app.route('/api/v1.0/disasters/<int:page_num>', methods=['GET'])
def show_fema_data(page_num=1):
    """Return JSON containing FEMA data, which includes state abbreviation,
    disaster type, and year of incident, number of pages, number of
    previous page, and number of next page.

    Example of how to use endpoint:
        '/api/v1.0/disasters/12'

    Parameter:
    - 'page_num': an integer > 0. If not provided, page_num defaults to 1.
        Example: 12

    This endpoint accepts optional parameters. For example:
        '/api/v1.0/disasters/12?year=2013&disaster-type=Flood&order=desc'
        '/api/v1.0/disasters/12?disaster-type=Flood&order=desc'
        '/api/v1.0/disasters/12?order=asc'

    Optional paramters:
    - 'year': disasters that occurred in the year of interest.
        Example: 2013
    - 'disaster_type': disasters of a certain type.
        Example: Flood
    - 'order': order results by date in ascending or descending order.
        Example: asc or desc
    """

    from models import FemaSchema
    from query_functions import get_fema_data

    RESULTS_PER_PAGE = 100

    year = request.args.get('year', None)
    disaster_type = request.args.get('disaster-type', None)
    order = request.args.get('order', None)

    fema_base_query_obj = get_fema_data(year, disaster_type, order)
    pagination_obj = fema_base_query_obj.paginate(
                        page_num, RESULTS_PER_PAGE, error_out=False)
    fema_schema = FemaSchema(many=True)
    fema_data = fema_schema.dump(pagination_obj.items).data
    print fema_data

    return jsonify({
            'data': fema_data,
            'num_pages': pagination_obj.pages,
            'next_num': pagination_obj.next_num,
            'prev_num': pagination_obj.prev_num
            })


# @app.route('/api/v1.0/disasters-by-year/<int:year>', methods=['GET'])
# def get_fema_results(year):
#     """Return JSON containing FEMA data and State data including
#     state, state abbreviation, disaster type, and year of incident, and count
#     of how many incidences within a particular year.
#
#     Example of how to use endpoint:
#         '/api/v1.0/disasters-by-year/1989'
#
#     Parameter:
#     - 'year': an integer between 1953 - 2018 (inclusive).
#
#     This endpoint accepts a optional parameter. For example:
#         '/api/v1.0/disasters/12?order=asc'
#
#     Optional paramters:
#     - 'order': order results in ascending or descending order by state name or
#         disaster type. If omitted, the default is state_asc.
#         To order by state name: state_asc or state_desc
#         To order by disaster type: disaster_asc or disaster_desc
#     """
#     from models import FemaSchema, StateSchema
#     from query_functions import get_joined_fema_data
#
#     input_year = year
#     order = request.args.get('order', None)
#
#     fema_base_query_obj = get_joined_fema_data(input_year, order)
#     # fema_schema = FemaSchema(many=True)
#     # fema_state_data = fema_schema.dump(fema_base_query_obj).data
#
#     return jsonify({
#             'data': fema_base_query_obj.all()
#             })


if __name__ == '__main__':
    app.run()
