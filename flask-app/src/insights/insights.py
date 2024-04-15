from flask import Blueprint, request, jsonify, make_response, abort
import json
from src import db

insights = Blueprint('insights', __name__)

# Get all insights from the DB
@insights.route('/insights', methods=['GET'])
def get_insights():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT Insight_ID, Date Created, Content, Engagement FROM Insights')
    row_headers = [x[0] for x in cursor.description] 
    rv = cursor.fetchall()
    return jsonify([dict(zip(row_headers, row)) for row in rv])

# get a list of comments for a given Insight_ID
@insights.route('/insights/<InsightID>/comments/', methods=['GET'])
def get_comments(Insight_ID):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM comments WHERE InsightID = %s', (Insight_ID,))
    row_headers = [x[0] for x in cursor.description]
    rv = cursor.fetchall()
    return jsonify([dict(zip(row_headers, row)) for row in rv]) if rv else ('', 404)

# Create a new comment on a given Insight_ID
@insights.route('/insights/<InsightID>/comments/', method=['POST'])
def create_comment(InsightID):
    comment_content = request.form['content']

    if not comment_content:
        return '', 400

    cursor = db.get_db().cursor()
    cursor.execute(
        'INSERT INTO InsightsComments (InsightID, Content) VALUES (%s, %s)',
        (InsightID, comment_content)
    )
    db.commit()
    new_comment_id = cursor.lastrowid
    cursor.close()

    return jsonify({"commentID": new_comment_id}), 201

# Update an insight for a specific general researcher
@insights.route('/insights/<int:InsightID>/', methods=['PUT'])
def update_insight(InsightID):
    # Get the new content from the request
    new_content = request.json.get('content')
    if not new_content:
        abort(400, description="No content provided for update.")
    cursor = db.get_db().cursor()

    # Check if insight exists
    cursor.execute('SELECT * FROM Insights WHERE InsightID = %s', (InsightID,))
    result = cursor.fetchone()
    if result is None:
        abort(404, description="Insight not found.")

    cursor.execute(
        'UPDATE Insights SET Content = %s WHERE InsightID = %s',
        (new_content, InsightID)
    )
    db.commit()
    cursor.close()

    return jsonify({"message": "Insight updated"}), 200

# general researcher creates an insight
@insights.route('/Insights', methods=['POST'])
def create_insight():
    content = request.json.get('Content')
    general_researcher_id = request.json.get('researcherID')

    if not content or not general_researcher_id:
        abort(400, description="Missing content or researcherID for the insight.")

    cursor = db.get_db().cursor()

    cursor.execute('SELECT * FROM GeneralResearcher WHERE researcherID = %s', (general_researcher_id,))
    if cursor.fetchone() is None:
        abort(404, description="GeneralResearcher not found.")

    cursor.execute(
        'INSERT INTO Insights (Content, GeneralResearcher) VALUES (%s, %s)',
        (content, general_researcher_id)
    )
    db.commit()
    new_InsightID = cursor.lastrowid
    cursor.close()

    return jsonify({"insightID": new_InsightID}), 201

# delete an insight
@insights.route('/insights/<int:insight_id>/researcher/<int:researcher_id>', methods=['DELETE'])
def delete_insight(insight_id, researcher_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT GeneralResearcher FROM Insights WHERE InsightID = %s', (insight_id,))
    result = cursor.fetchone()

    if result is None:
        abort(404, description="Insight not found.")
    # If the researcher ID does not match, return error
    if result[0] != researcher_id:
        abort(403, description="Permission denied: Cannot delete another researcher's insight.")

    cursor.execute('DELETE FROM Insights WHERE InsightID = %s', (insight_id,))
    db.commit()
    cursor.close()

    return jsonify({"message": "Insight deleted"}), 200