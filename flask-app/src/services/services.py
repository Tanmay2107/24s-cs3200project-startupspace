from flask import Blueprint, request, jsonify, make_response
from src import db

services = Blueprint('services', __name__)

# Get investment pipeline analytics for a specific VC
@services.route('/investmentAnalytics/<int:analytics_id>', methods=['GET'])
def get_investment_analytics(analytics_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM InvestmentAnalytics WHERE AnalyticsID = %s', (analytics_id,))
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    if not the_data:
        return jsonify({'message': 'Investment analytics not found for the given ID'}), 404
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

# Update a given VC’s investment analytics
@services.route('/investmentAnalytics/<int:analytics_id>', methods=['PUT'])
def update_investment_analytics(analytics_id):
    the_data = request.json
    updates = {key: val for key, val in the_data.items() if key in ['NumberOfDeals', 'TotalInvested', 'PortfolioDiversity', 'PerformanceMetric'] and val is not None}
    if not updates:
        return jsonify({'message': 'No data provided for update'}), 400
    set_clause = ', '.join(f"{k} = %s" for k in updates)
    query = f"UPDATE InvestmentAnalytics SET {set_clause} WHERE AnalyticsID = %s"
    cursor = db.get_db().cursor()
    cursor.execute(query, tuple(updates.values()) + (analytics_id,))
    db.get_db().commit()
    if cursor.rowcount == 0:
        return jsonify({'message': 'No matching investment analytics found to update'}), 404
    return jsonify({'message': 'Investment analytics updated successfully'}), 200

# Retrieves details for a specific investment opportunity
@services.route('/investmentOpportunities/<int:opp_id>', methods=['GET'])
def get_investment_opportunity(opp_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM InvestmentOpportunities WHERE OppID = %s', (opp_id,))
    column_headers = [x[0] for x in cursor.description]
    the_data = cursor.fetchone()
    if not the_data:
        return jsonify({'message': 'Investment opportunity not found'}), 404
    return jsonify(dict(zip(column_headers, the_data)))

# Add a new investment opportunity
@services.route('/investmentOpportunities', methods=['POST'])
def add_investment_opportunity():
    the_data = request.json
    query = 'INSERT INTO InvestmentOpportunities (FundingRound, Description, Terms, StartupID) VALUES (%s, %s, %s, %s)'
    values = (the_data.get('FundingRound'), the_data.get('Description'), the_data.get('Terms'), the_data.get('StartupID'))
    cursor = db.get_db().cursor()
    cursor.execute(query, values)
    db.get_db().commit()
    return jsonify({'message': 'Investment opportunity added successfully'}), 201

# Update details for a given investment opportunity
@services.route('/investmentOpportunities/<int:opp_id>', methods=['PUT'])
def update_investment_opportunity(opp_id):
    the_data = request.json
    query = 'UPDATE InvestmentOpportunities SET FundingRound = %s, Description = %s, Terms = %s, StartupID = %s WHERE OppID = %s'
    values = (the_data.get('FundingRound'), the_data.get('Description'), the_data.get('Terms'), the_data.get('StartupID'), opp_id)
    cursor = db.get_db().cursor()
    cursor.execute(query, values)
    db.get_db().commit()
    return jsonify({'message': 'Investment opportunity updated successfully'}), 200

# Delete an opportunity from the tracker
@services.route('/investmentOpportunities/<int:opp_id>', methods=['DELETE'])
def delete_investment_opportunity(opp_id):
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM InvestmentOpportunities WHERE OppID = %s', (opp_id,))
    db.get_db().commit()
    return jsonify({'message': 'Investment opportunity deleted successfully'}), 204

@services.route('/vcids', methods=['GET'])
def get_VCID():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT VCID FROM VentureCapitalist')
    column_headers = [x[0] for x in cursor.description]
    json_data = [dict(zip(column_headers, row)) for row in cursor.fetchall()]
    return jsonify(json_data)
