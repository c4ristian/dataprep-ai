"""
This module tests the app.py script.
"""

import pytest
from app import app


def test_get_gdp_data():
    app.testing = True
    client = app.test_client()

    response = client.get('/gdp?iso_code=US&from_year=2010&to_year=2015')
    assert response.status_code == 200
    assert response.json == [
        # The year 2015 is not included in the response because the data is only available up to 2014
        {'year': 2014, 'gdp_total_usd': 17419000000000, 'gdp_per_capita_usd': 54629.495167891204},
        {'year': 2013, 'gdp_total_usd': 16768053000000, 'gdp_per_capita_usd': 52980.043626311905},
        {'year': 2012, 'gdp_total_usd': 16163158000000, 'gdp_per_capita_usd': 51456.658728035305},
        {'year': 2011, 'gdp_total_usd': 15517926000000, 'gdp_per_capita_usd': 49781.357490134},
        {'year': 2010, 'gdp_total_usd': 14964372000000, 'gdp_per_capita_usd': 48374.056456596605}
    ]

    response = client.get('/gdp?iso_code=USA&from_year=2010')
    assert response.status_code == 400
    assert response.json == {'error': 'Please provide iso_code, from_year, and to_year parameters'}

    response = client.get('/gdp?iso_code=USA&from_year=2010&to_year=2016')
    assert response.status_code == 404
    assert response.json == {'error': 'No data found for the specified ISO code and year range'}
