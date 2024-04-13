from flask import Blueprint, request, jsonify, make_response
from src import db

investment_opportunities = Blueprint('investment_opportunities', __name__)

# Retrieves details for a specific investment opportunity
@investment_opportunities.route('/investmentOpportunities/<opp_id>', methods=['GET'])
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
@investment_opportunities.route('/investmentOpportunities', methods=['POST'])
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

    response = make_response(jsonify({'message': 'Investment opportunity added successfully'}), 201)
    response.mimetype = 'application/json'
    return response

# Update details for a given investment opportunity
@investment_opportunities.route('/investmentOpportunities/<opp_id>', methods=['PUT'])
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

    response = make_response(jsonify({'message': 'Investment opportunity updated successfully'}), 200)
    response.mimetype = 'application/json'
    return response

# Delete an opportunity from the tracker
@investment_opportunities.route('/investmentOpportunities/<opp_id>', methods=['DELETE'])
def delete_investment_opportunity(opp_id):
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM InvestmentOpportunities WHERE OppID = %s', (opp_id,))
    db.get_db().commit()

    response = make_response(jsonify({'message': 'Investment opportunity deleted successfully'}), 204)
    response.mimetype = 'application/json'
    return response
