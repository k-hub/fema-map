from query_functions import get_fema_data
import sys
sys.path.append("..")

"""Run pytest to run tests."""


def test_get_fema_data_no_filters():
    """Should expect to get all records in descending
    order by incident_begin_date."""

    results = get_fema_data()
    assert results.count() == 48131L
    assert str(results[0]) == '(datetime.datetime(2018, 4, 16, 17, 0, '\
        'tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=-420, name=None)), '\
        'u\'TX\', u\'Fire\')'


def test_get_fema_data_asc_order():
    """Should expect to get all records in ascending
    order by incident begin date."""

    results = get_fema_data(order='asc')
    assert results.count() == 48131L
    assert str(results[0]) == '(datetime.datetime(1953, 5, 1, 17, 0, '\
        'tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=-420, name=None)), '\
        'u\'GA\', u\'Tornado\')'


def test_get_fema_data_year_and_diaster_type():
    """Should expect to get all records from a particular year of
        a particular disaster type."""

    results = get_fema_data(year=2013,
                            disaster_type='Snow')
    assert results.count() == 23L
    assert str(results[0]) == '(datetime.datetime(2013, 2, 19, 22, 0, '\
        'tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=-480, name=None)), '\
        'u\'KS\', u\'Snow\')'


def test_get_fema_data_year():
    """Should expect to get all records from a particular year."""

    results = get_fema_data(year=2000)
    assert results.count() == 1348L
    assert str(results[0]) == '(datetime.datetime(2000, 12, 24, 16, 0, '\
        'tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=-480, name=None)), '\
        'u\'OK\', u\'Severe Ice Storm\')'


def test_get_fema_data_disaster_type():
    """Should expect to get all records for a particular disaster type."""

    results = get_fema_data(disaster_type='Tsunami')
    assert results.count() == 9L
    assert str(results[0]) == '(datetime.datetime(2011, 3, 11, 4, 9, 46, '\
        'tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=-480, name=None)), '\
        'u\'OR\', u\'Tsunami\')'


def test_get_fema_data_all_filters_and_order():
    """Should expect to get all records from a particular year of
        a particular disaster type ordered by incident begin date."""

    # incident_begin_date by ascending order
    results_asc = get_fema_data(year=2012,
                                disaster_type='Flood',
                                order='asc')
    assert results_asc.count() == 18L
    assert str(results_asc[0]) == '(datetime.datetime(2012, 1, 16, 16, 0, '\
        'tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=-480, name=None)), '\
        'u\'OR\', u\'Flood\')'

    # incident_begin_date by descending order
    results_desc = get_fema_data(year=2012,
                                 disaster_type='Flood',
                                 order='desc')
    assert results_desc.count() == 18L
    assert str(results_desc[0]) == '(datetime.datetime(2012, 9, 10, 17, 0, '\
        'tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=-420, name=None)), '\
        'u\'UT\', u\'Flood\')'
