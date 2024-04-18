from flask import Blueprint, request, jsonify, make_response
from src import db

tracking = Blueprint('tracking', __name__)

# Financial Metrics Routes
@tracking.route('/financialMetrics/<int:StartupID>', methods=['GET'])
def get_financial_metrics(StartupID):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM FinancialMetrics WHERE StartupID = %s', (StartupID,))
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

@tracking.route('/financialMetrics/<int:startup_id>', methods=['POST'])
def add_financial_metrics(startup_id):
    the_data = request.json
    metric_name = the_data['metric_name']
    metric_value = the_data['metric_value']
    query = 'INSERT INTO financial_metrics (startup_id, metric_name, metric_value) VALUES (%s, %s, %s)'
    cursor = db.get_db().cursor()
    cursor.execute(query, (startup_id, metric_name, metric_value))
    db.get_db().commit()
    return 'Success!', 201

@tracking.route('/financialMetrics/<int:startup_id>', methods=['PUT'])
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

@tracking.route('/financialMetrics/<int:startup_id>', methods=['DELETE'])
def delete_financial_metrics(startup_id):
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM financial_metrics WHERE startup_id = %s', (startup_id,))
    db.get_db().commit()
    return 'Metrics deleted.', 204

@tracking.route('/generalResearchers', methods=['GET'])
def get_general_researchers():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM GeneralResearcher')
    column_headers = [x[0] for x in cursor.description]
    researchers = cursor.fetchall()
    cursor.close()
    return jsonify([dict(zip(column_headers, row)) for row in researchers])

# Followed Deals Routes
@tracking.route('/followedDeals/<int:researcher_id>', methods=['GET'])
def get_followed_deals(researcher_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM FollowedDeals WHERE ResearcherID = %s', (researcher_id,))
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

@tracking.route('/followedDeals/<int:researcher_id>', methods=['POST'])
def follow_deal(researcher_id):
    the_data = request.json
    deal_id = the_data['deal_id']
    query = 'INSERT INTO FollowedDeals (researcherID, DealID) VALUES (%s, %s)'
    cursor = db.get_db().cursor()
    cursor.execute(query, (researcher_id, deal_id))
    db.get_db().commit()
    return 'New deal followed successfully.', 201
