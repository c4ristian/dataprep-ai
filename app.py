"""
This script creates a Flask application that provides an API endpoint to retrieve GDP data for a specific country.
"""
import sqlite3
from flask import Flask, request, jsonify


app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('./data/database.sqlite')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/gdp', methods=['GET'])
def get_gdp_data():
    iso_code = request.args.get('iso_code')
    from_year = request.args.get('from_year')
    to_year = request.args.get('to_year')

    if not iso_code or not from_year or not to_year:
        return jsonify({'error': 'Please provide iso_code, from_year, and to_year parameters'}), 400

    conn = get_db_connection()
    query = """
    SELECT year, gdp_total_usd, gdp_per_capita_usd
    FROM G7_GDPs_transformed
    WHERE ISO_codes = ? AND year BETWEEN ? AND ?
    ORDER BY year DESC
    """
    data = conn.execute(query, (iso_code, from_year, to_year)).fetchall()
    conn.close()

    if not data:
        return jsonify({'error': 'No data found for the specified ISO code and year range'}), 404

    result = [dict(row) for row in data]
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
