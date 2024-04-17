from flask import Blueprint, request, jsonify, make_response, abort
import json
from src import db

insights = Blueprint('insights', __name__)

# Get all insights from the DB
@insights.route('/insights', methods=['GET'])
def get_insights():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT `InsightID`, `DateCreated`, `Content`, `Likes` FROM Insights')
    column_headers = [x[0] for x in cursor.description]
    json_data = [dict(zip(column_headers, row)) for row in cursor.fetchall()]
    return jsonify(json_data)

# Get a list of comments for a given Insight ID
@insights.route('/insights/<int:InsightID>/comments', methods=['GET'])
def get_comments(InsightID):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Comments WHERE InsightID = %s', (InsightID,))
    column_headers = [x[0] for x in cursor.description]
    json_data = [dict(zip(column_headers, row)) for row in cursor.fetchall()] if cursor.rowcount > 0 else ('', 404)
    return jsonify(json_data)

# Create a new comment on a given Insight ID
@insights.route('/insights/<int:InsightID>/comments', methods=['POST'])
def create_comment(InsightID):
    comment_content = request.json.get('content')
    if not comment_content:
        abort(400, description="No content provided.")
    
    cursor = db.get_db().cursor()
    cursor.execute(
        'INSERT INTO InsightsComments (InsightID, Content) VALUES (%s, %s)',
        (InsightID, comment_content)
    )
    db.get_db().commit()
    new_comment_id = cursor.lastrowid
    return jsonify({"commentID": new_comment_id}), 201

# Update an insight for a specific general researcher
@insights.route('/insights/<int:InsightID>', methods=['PUT'])
def update_insight(InsightID):
    new_content = request.json.get('content')
    if not new_content:
        abort(400, description="No content provided for update.")

    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Insights WHERE InsightID = %s', (InsightID,))
    if cursor.fetchone() is None:
        abort(404, description="Insight not found.")

    cursor.execute(
        'UPDATE Insights SET Content = %s WHERE InsightID = %s',
        (new_content, InsightID)
    )
    db.get_db().commit()
    return jsonify({"message": "Insight updated"}), 200

# General researcher creates an insight
@insights.route('/insights', methods=['POST'])
def create_insight():
    content = request.json.get('Content')
    general_researcher_id = request.json.get('researcherID')

    if not content or not general_researcher_id:
        abort(400, description="Missing content or researcherID.")

    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM GeneralResearcher WHERE researcherID = %s', (general_researcher_id,))
    if cursor.fetchone() is None:
        abort(404, description="GeneralResearcher not found.")

    cursor.execute(
        'INSERT INTO Insights (Content, GeneralResearcherID) VALUES (%s, %s)',
        (content, general_researcher_id)
    )
    db.get_db().commit()
    new_InsightID = cursor.lastrowid
    return jsonify({"insightID": new_InsightID}), 201

# Delete an insight
@insights.route('/insights/<int:insight_id>/researcher/<int:researcher_id>', methods=['DELETE'])
def delete_insight(insight_id, researcher_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT GeneralResearcherID FROM Insights WHERE InsightID = %s', (insight_id,))
    result = cursor.fetchone()
    if result is None:
        abort(404, description="Insight not found.")
    if result[0] != researcher_id:
        abort(403, description="Permission denied: Cannot delete another researcher's insight.")

    cursor.execute('DELETE FROM Insights WHERE InsightID = %s', (insight_id,))
    db.get_db().commit()
    return jsonify({"message": "Insight deleted"}), 200
