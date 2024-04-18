from flask import Blueprint, request, jsonify, make_response, abort
import json
from src import db

insights = Blueprint('insights', __name__)

# Get all insights from the DB
@insights.route('/insights', methods=['GET'])
def get_insights():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Insights')
    column_headers = [x[0] for x in cursor.description]
    json_data = [dict(zip(column_headers, row)) for row in cursor.fetchall()]
    return jsonify(json_data)

# Get insights from a specific researcher
@insights.route('/insights/<int:researcher_id>', methods=['GET'])
def get_insights_researcher(researcher_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Insights WHERE GeneralResearcher = %s', (researcher_id))
    column_headers = [x[0] for x in cursor.description]
    json_data = [dict(zip(column_headers, row)) for row in cursor.fetchall()]
    return jsonify(json_data)

# Get a list of comments for a given Insight ID
@insights.route('/insights/<int:InsightID>/comments', methods=['GET'])
def get_comments(InsightID):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM InsightComments WHERE InsightID = %s', (InsightID,))
    column_headers = [x[0] for x in cursor.description]
    json_data = [dict(zip(column_headers, row)) for row in cursor.fetchall()] if cursor.rowcount > 0 else ('', 404)
    return jsonify(json_data)

# Create a new comment on a given Insight ID
@insights.route('/insights/<int:InsightID>/comments', methods=['POST'])
def create_comment(InsightID):
    cursor = db.get_db().cursor()
    the_data = request.json

    content = the_data['Content']
    insightID = str(InsightID)
    researcherID = the_data['researcherID']

    query = "INSERT INTO InsightComments (Content, GeneralResearcher, InsightID) VALUES "
    query = query + "("
    query = query + "'" + content + "', "
    query = query + researcherID + ","
    query = query + insightID  + ")"

    cursor.execute(query)

    db.get_db().commit()
    new_comment_id = cursor.lastrowid
    return jsonify({"commentID": new_comment_id}), 201

# Update an insight for a specific general researcher
@insights.route('/insights/<int:InsightID>', methods=['PUT'])
def update_insight(InsightID):
    cursor = db.get_db().cursor()
    the_data = request.json
    new_content = the_data['Content']  

    # Construct the query using string concatenation
    query = "UPDATE Insights SET "
    query += "Content = '"+ new_content + "' "  
    query += "WHERE InsightID = " + str(InsightID)

    # Execute the query
    cursor.execute(query)
    db.get_db().commit()

    return jsonify({"message": "Insight updated"}), 200

# General researcher creates an insight
@insights.route('/insights', methods=['POST'])
def create_insight():
    cursor = db.get_db().cursor()
    the_data = request.json

    content = the_data['Content']  
    researcherID = the_data['researcherID']  

    
    query = "INSERT INTO InsightComments (Content, GeneralResearcher) VALUES ("
    query += "'" + content.replace("'", "''") + "', "  
    query += str(researcherID) + ")"

    cursor.execute(query)
    db.get_db().commit()  
    new_insight_id = cursor.lastrowid 

    return jsonify({"InsightID": new_insight_id}), 201  

# Delete an insight
@insights.route('/insights/<int:insight_id>', methods=['DELETE'])
def delete_insight(insight_id):
    # Get a cursor object from the database
    cursor = db.get_db().cursor()

    # Directly delete the insight based on the InsightID provided in the URL
    query = "DELETE FROM Insights WHERE InsightID = " + str(insight_id)
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'
