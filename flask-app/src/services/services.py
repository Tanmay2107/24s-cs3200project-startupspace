from flask import Blueprint, request, jsonify, make_response, abort, current_app
from src import db

services = Blueprint('services', __name__)

# Get investment pipeline analytics for a specific VC

@services.route('/investmentAnalytics', methods=['GET'])
def get_vcid_an():
    VCID = request.args.get('VCID', type=int)
    if VCID is None:
        return "VCID is " + str(VCID), 400
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM InvestmentAnalytics WHERE VCID = %s', (VCID,))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(row_headers, row)))
    return jsonify(json_data)

@services.route('/vc', methods=['GET'])
def get_vcid():
    VCID = request.args.get('VCID', type=int)
    if VCID is None:
        return "VCID is " + str(VCID), 400
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM VentureCapitalist WHERE VCID = %s', (VCID,))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(row_headers, row)))
    return jsonify(json_data)


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


@services.route('/vc/investment-opportunities', methods=['GET'])
def get_investment_opportunities():
    vcid = request.args.get('VCID', type=int)
    if vcid is None:
        return "VCID is " + str(vcid), 400

    
    cur = db.get_db().cursor()
    
    # Execute the query
    cur.execute("SELECT InvestmentOpportunities.* FROM InvestmentOpportunities JOIN InvestmentOpportunityToVC ON InvestmentOpportunities.OppID = InvestmentOpportunityToVC.OppID WHERE InvestmentOpportunityToVC.VCID = %s", (vcid,))
    
    # Fetch all rows from the database
    opportunities = cur.fetchall()
    
    # Generate column headers
    column_headers = [desc[0] for desc in cur.description]

    # Create a list of dictionaries, each representing a row from the results
    result = [dict(zip(column_headers, opportunity)) for opportunity in opportunities]
    
    return jsonify(result)


@services.route('/link', methods=['POST'])
def link_startup_to_vc():
    data = request.get_json()  # This will automatically parse the JSON body
    current_app.logger.info(f"Received data: {data}")
    startup_id = data.get('StartupID')
    vcid = data.get('VCID')

    try:
        startup_id = int(data.get('StartupID'))
    except (ValueError, TypeError):
        abort(400, 'StartupID must be an integer')

    cur = db.get_db().cursor()
    dataBase = db.get_db()
    
    # Insert into InvestmentOpportunities and get the OppID
    cur.execute(
            "INSERT INTO InvestmentOpportunities (Description, Terms, StartupID) VALUES (%s, %s, %s)",
            ('', '', startup_id)  # Replace with actual values or variables as needed
        )
    opp_id = cur.lastrowid
    
    # Now, link this OppID with the VCID in InvestmentOpportunityToVC
    cur.execute(
        "INSERT INTO InvestmentOpportunityToVC (VCID, OppID) VALUES (%s, %s);",
        (vcid, opp_id)
    )    
    dataBase.commit()
    return jsonify({'success': True, 'message': 'Startup linked to VC successfully', 'OppID': opp_id, 'vcid': vcid}), 201


