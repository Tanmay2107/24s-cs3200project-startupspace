from flask import Blueprint, request, jsonify, make_response, abort, current_app
import json
from src import db



founder = Blueprint('founder', __name__)


# Gets a list of founder names
@founder.route('/founder', methods=['GET'])
def get_founder():
    #get cursor object from database
    cursor = db.get_db().cursor()

    #use cursor to query the databse for a list of founders

    cursor.execute('SELECT Name FROM Founder')

    column_headers = [x[0] for x in cursor.description]

    json_data = []

    theData = cursor.fetchall()

    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)




@founder.route('/founder', methods=['POST'])
def create_founder():
    the_data = request.json
    current_app.logger.info(the_data)

    #extract the variable

    Name = the_data['Name']
    PhoneNumber = the_data['PhoneNumber']
    NumberOfCompanies = the_data['NumberOfCompanies']
    CredibilityRanking = the_data['CredibilityRanking']

    query = 'insert into Founder (FounderID, Name, PhoneNumber, NumberOfCompanies, CredibilityRanking) values'
    query += ' ("'
    query += Name + '", "'
    query += PhoneNumber + '", "'
    query += NumberOfCompanies + '", "'
    query += CredibilityRanking + ')'
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'


@founder.route('/founder/<founder_id>', methods=['PUT'])
def update_founder_detail(founder_id):
    data = request.json
    current_app.logger.info(f"Update request for StartupID {founder_id} with data: {data}")

    try:
        founder = founder_id.query.get(founder_id)
        if not founder:
            return jsonify({"error": "Startup not found"}), 404
        
        #update fields from JSON if available

        founder.Name = data.get('Name', founder.Name)
        founder.PhoneNumber = data.get('PhoneNumber', founder.PhoneNumber)
        founder.NumberOfCompanies = data.get('NumberOfCompanies', founder.NumberOfCompanies)
        founder.CredibilityRanking = data.get('CredibilityRanking', founder.CredibilityRanking)

        db.session.commit() # Commit changes to db

        return jsonify({"success" : "Startup details updated successfully"}), 200
    
    except Exception as e:
        current_app.logger.error(f"Error updating startup: {e}")
        db.session.rollback()
        return jsonify({"error": "Failed to update startup details"}), 500
    
@founder.route('/founder/<founder_id>', methods=['DELETE'])
def delete_founder(founder_id):
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM Founder WHERE founderId = %s', (founder_id))
    db.get_db().commit()
    return 'Metrics deleted', 204


@founder.route('/founder/<founder_id>/startup/', method = ['GET'])
def get_founder_startup(founder_id):
    cursor = db.get_db().cursor()

    query = 'SELECT * FROM Startup WHERE StartupID IN (SELECT StartupID FROM StartupFounder WHERE StartupFounder.FounderID = '
    query += founder_id

    cursor.execute(query)

    column_headers = [x[0] for x in cursor.description]

    json_data = []

    the_data = cursor.fetchall()

    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)


# ## These next few ones are to get the startup the founder is working at

# @founder.route('/founder/<int:StartupID>/documents', methods=['POST'])
# def create_document(StartupID):
#     # collecting data from the request object 
#     the_data = request.json
#     current_app.logger.info(the_data)

#     #extracting the variable
#     documentType = the_data['documentType']
#     fileSize = the_data["fileSize"]
#     pageCount = the_data["pageCount"]
#     wordCount = the_data["wordCount"]
#     characterCount = the_data["characterCount"]
#     startupID = StartupID



#     # Constructing the query
#     query = 'insert into Document (documentType, fileSize, pageCount, wordCount, characterCount, StartupID) values ("'
#     query += documentType + '", "'
#     query += fileSize + '", "'
#     query += pageCount + '", "'
#     query += wordCount + '", "'
#     query += characterCount + '", "'
#     query += startupID + ')'
#     current_app.logger.info(query)

#     # executing and committing the insert statement 
#     cursor = db.get_db().cursor()
#     cursor.execute(query)
#     db.get_db().commit()
    
#     return 'Success!'








## these next few ones are to get the documents the founder holds



