from flask import Blueprint, request, jsonify, make_response
from src import db

tracking = Blueprint('tracking', __name__)

# Financial Metrics Routes
# Get all financial metrics for a given startup
@tracking.route('/financialMetrics/<startup_id>', methods=['GET'])
def get_financial_metrics(startup_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM financial_metrics WHERE startup_id = %s', (startup_id,))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Add new financial metrics for a given startup
@tracking.route('/financialMetrics/<startup_id>', methods=['POST'])
def add_financial_metrics(startup_id):
    the_data = request.json
    metric_name = the_data['metric_name']
    metric_value = the_data['metric_value']
    query = 'INSERT INTO financial_metrics (startup_id, metric_name, metric_value) VALUES (%s, %s, %s)'
    cursor = db.get_db().cursor()
    cursor.execute(query, (startup_id, metric_name, metric_value))
    db.get_db().commit()
    return 'Success!', 201

# Update existing financial metrics for a given startup
@tracking.route('/financialMetrics/<startup_id>', methods=['PUT'])
def update_financial_metrics(startup_id):
    the_data = request.json
    metric_id = the_data['metric_id']
    metric_name = the_data['metric_name']
    metric_value = the_data['metric_value']
    query = 'UPDATE financial_metrics SET metric_name = %s, metric_value = %s WHERE id = %s AND startup_id = %s'
    cursor = db.get_db().cursor()
    cursor.execute(query, (metric_name, metric_value, metric_id, startup_id))
    db.get_db().commit()
    return 'Update successful!', 200

# Delete the financial metrics for a given startup
@tracking.route('/financialMetrics/<startup_id>', methods=['DELETE'])
def delete_financial_metrics(startup_id):
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM financial_metrics WHERE startup_id = %s', (startup_id,))
    db.get_db().commit()
    return 'Metrics deleted.', 204

# Followed Deals Routes
# Get a list of a general researcher’s followed deals
@tracking.route('/followedDeals/<researcher_id>', methods=['GET'])
def get_followed_deals(researcher_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM FollowedDeals WHERE GeneralResearcherID = %s', (researcher_id,))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Follow a new deal for a given general researcher
@tracking.route('/followedDeals/<researcher_id>', methods=['POST'])
def follow_deal(researcher_id):
    the_data = request.json
    deal_id = the_data['deal_id']
    query = 'INSERT INTO FollowedDeals (GeneralResearcherID, DealID) VALUES (%s, %s)'
    cursor = db.get_db().cursor()
    cursor.execute(query, (researcher_id, deal_id))
    db.get_db().commit()
    return 'New deal followed successfully.', 201
