import os
from flask import Flask, jsonify, request
# from werkzeug.contrib.cache import MemcachedCache
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
db.Model.metadata.reflect(db.engine)

# cache = MemcachedCache(['127.0.0.1:11211'])


@app.route('/api/v1.0/disasters/<int:page_num>', methods=['GET'])
def show_fema_data(page_num=1):
    """Return JSON containing FEMA data, number of pages, number of
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
    year = None
    disaster_type = None
    order = None

    if 'year' in request.args:
        year = request.args['year']
    if 'disaster-type' in request.args:
        disaster_type = request.args['disaster-type']
    if 'order' in request.args:
        order = request.args['order']

    fema_base_query_obj = get_fema_data(year, disaster_type, order)
    pagination_obj = fema_base_query_obj.paginate(
                        page_num, RESULTS_PER_PAGE, error_out=False)
    fema_schema = FemaSchema(many=True)
    fema_data = fema_schema.dump(pagination_obj.items).data

    return jsonify({
            'data': fema_data,
            'num_pages': pagination_obj.pages,
            'next_num': pagination_obj.next_num,
            'prev_num': pagination_obj.prev_num
        })


if __name__ == '__main__':
    app.run()
