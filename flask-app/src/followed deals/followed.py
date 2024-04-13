from flask import Blueprint, request, jsonify, make_response
from src import db

followed_deals = Blueprint('followed_deals', __name__)

# Get a list of a general researcher’s followed deals
@followed_deals.route('/followedDeals/<researcher_id>', methods=['GET'])
def get_followed_deals(researcher_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM FollowedDeals WHERE GeneralResearcherID = %s', (researcher_id,))
    row_headers = [x[0] for x in cursor.description]  # Get the headers
    json_data = []
    theData = cursor.fetchall()  # Get the actual data
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))  # Combine headers and data into a dictionary
    the_response = make_response(jsonify(json_data))  # Make a response object
    the_response.status_code = 200  # Set the status code
    the_response.mimetype = 'application/json'  
    return the_response

# Follow a new deal for a given general researcher
@followed_deals.route('/followedDeals/<researcher_id>', methods=['POST'])
def follow_deal(researcher_id):
    the_data = request.json
    deal_id = the_data['deal_id']  

    query = 'INSERT INTO FollowedDeals (GeneralResearcherID, DealID) VALUES (%s, %s)'
    cursor = db.get_db().cursor()
    cursor.execute(query, (researcher_id, deal_id))
    db.get_db().commit()

    return 'New deal followed successfully.', 201
