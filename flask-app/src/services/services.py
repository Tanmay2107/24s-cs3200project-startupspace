from flask import Blueprint, request, jsonify, make_response
from src import db

services = Blueprint('services', __name__)

# Get investment pipeline analytics for a specific VC
@services.route('/investmentAnalytics/<analytics_id>', methods=['GET'])
def get_investment_analytics(analytics_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM InvestmentAnalytics WHERE AnalyticsID = %s', (analytics_id,))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    if not theData:
        return jsonify({'message': 'Investment analytics not found for the given ID'}), 404
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Update a given VC’s investment analytics
@services.route('/investmentAnalytics/<analytics_id>', methods=['PUT'])
def update_investment_analytics(analytics_id):
    the_data = request.json
    query = 'UPDATE InvestmentAnalytics SET '
    query_fragments = []
    query_values = []
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
    if not query_fragments:
        return jsonify({'message': 'No data provided for update'}), 400
    query += ', '.join(query_fragments)
    query += ' WHERE AnalyticsID = %s'
    query_values.append(analytics_id)
    cursor = db.get_db().cursor()
    cursor.execute(query, tuple(query_values))
    db.get_db().commit()
    if cursor.rowcount == 0:
        return jsonify({'message': 'No matching investment analytics found to update'}), 404
    return jsonify({'message': 'Investment analytics updated successfully'}), 200

# Retrieves details for a specific investment opportunity
@services.route('/investmentOpportunities/<opp_id>', methods=['GET'])
def get_investment_opportunity(opp_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM InvestmentOpportunities WHERE OppID = %s', (opp_id,))
    row_headers = [x[0] for x in cursor.description]
    theData = cursor.fetchone()
    if not theData:
        response = make_response(jsonify({'message': 'Investment opportunity not found'}), 404)
    else:
        json_data = dict(zip(row_headers, theData))
        response = make_response(jsonify(json_data), 200)
    response.mimetype = 'application/json'
    return response

# Add a new investment opportunity
@services.route('/investmentOpportunities', methods=['POST'])
def add_investment_opportunity():
    the_data = request.json
    funding_round = the_data.get('FundingRound')
    description = the_data.get('Description')
    terms = the_data.get('Terms')
    startup_id = the_data.get('StartupID')
    query = 'INSERT INTO InvestmentOpportunities (FundingRound, Description, Terms, StartupID) VALUES (%s, %s, %s, %s)'
    cursor = db.get_db().cursor()
    cursor.execute(query, (funding_round, description, terms, startup_id))
    db.get_db().commit()
    return make_response(jsonify({'message': 'Investment opportunity added successfully'}), 201)

# Update details for a given investment opportunity
@services.route('/investmentOpportunities/<opp_id>', methods=['PUT'])
def update_investment_opportunity(opp_id):
    the_data = request.json
    funding_round = the_data.get('FundingRound')
    description = the_data.get('Description')
    terms = the_data.get('Terms')
    startup_id = the_data.get('StartupID')
    query = 'UPDATE InvestmentOpportunities SET FundingRound = %s, Description = %s, Terms = %s, StartupID = %s WHERE OppID = %s'
    cursor = db.get_db().cursor()
    cursor.execute(query, (funding_round, description, terms, startup_id, opp_id))
    db.get_db().commit()
    return make_response(jsonify({'message': 'Investment opportunity updated successfully'}), 200)

# Delete an opportunity from the tracker
@services.route('/investmentOpportunities/<opp_id>', methods=['DELETE'])
def delete_investment_opportunity(opp_id):
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM InvestmentOpportunities WHERE OppID = %s', (opp_id,))
    db.get_db().commit()
    return make_response(jsonify({'message': 'Investment opportunity deleted successfully'}), 204)

@services.route('/vcids', methods=['GET'])
def get_VCID():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('SELECT VCID FROM VentureCapitalist')

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

@services.route('/vc', methods=['GET'])
def get_VC_by_ID():
    VCID = request.args.get('VCID', default=1, type=int)  # default to 1 if VCID is not provided
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM VentureCapitalist WHERE VCID=%s', (VCID,))
    column_headers = [x[0] for x in cursor.description]
    json_data = [dict(zip(column_headers, row)) for row in cursor.fetchall()]
    return jsonify(json_data)