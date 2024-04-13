from flask import Blueprint, request, jsonify, make_response
from src import db

investment_analytics = Blueprint('investment_analytics', __name__)

# Get investment pipeline analytics for a specific VC
@investment_analytics.route('/investmentAnalytics/<analytics_id>', methods=['GET'])
def get_investment_analytics(analytics_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM InvestmentAnalytics WHERE AnalyticsID = %s', (analytics_id,))
    row_headers = [x[0] for x in cursor.description]  # Get the headers
    json_data = []
    theData = cursor.fetchall()  # Get the actual data
    if not theData:
        return jsonify({'message': 'Investment analytics not found for the given ID'}), 404
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))  # Combine headers and data into a dictionary
    the_response = make_response(jsonify(json_data))  # Make a response object
    the_response.status_code = 200  # Set the status code
    the_response.mimetype = 'application/json'  # Set the mimetype
    return the_response

# Update a given VC’s investment analytics
@investment_analytics.route('/investmentAnalytics/<analytics_id>', methods=['PUT'])
def update_investment_analytics(analytics_id):
    the_data = request.json
    # Begin constructing the query
    query = 'UPDATE InvestmentAnalytics SET '
    query_fragments = []
    query_values = []

    # For each field, check if it's present in the_data, then add to the query
    if 'NumberOfDeals' in the_data:
        query_fragments.append('NumberOfDeals = %s')
        query_values.append(the_data['NumberOfDeals'])
    if 'TotalInvested' in the_data:
        query_fragments.append('TotalInvested = %s')
        query_values.append(the_data['TotalInvested'])
    if 'PortfolioDiversity' in the_data:
        query_fragments.append('PortfolioDiversity = %s')
        query_values.append(the_data['PortfolioDiversity'])
    if 'PerformanceMetric' in the_data:
        query_fragments.append('PerformanceMetric = %s')
        query_values.append(the_data['PerformanceMetric'])

    # Finalize the query
    if not query_fragments:
        return jsonify({'message': 'No data provided for update'}), 400

    query += ', '.join(query_fragments)
    query += ' WHERE AnalyticsID = %s'
    query_values.append(analytics_id)

    # Execute the query
    cursor = db.get_db().cursor()
    cursor.execute(query, tuple(query_values))
    db.get_db().commit()
    
    if cursor.rowcount == 0:
        return jsonify({'message': 'No matching investment analytics found to update'}), 404

    return jsonify({'message': 'Investment analytics updated successfully'}), 200
