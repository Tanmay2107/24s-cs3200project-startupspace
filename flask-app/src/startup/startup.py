from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


startup = Blueprint('startup', __name__)

# Get all the products from the database
@startup.route('/startup', methods=['GET'])
def get_startup():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('SELECT name FROM Startup')

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

@startup.route('/startup', methods=['POST'])
def create_startup():
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    Name = the_data['Name']
    City = the_data["City"]
    GrowthStage = the_data["GrowthStage"]
    Industry = the_data["Industry"]
    acqID = the_data["acqID"]



    # Constructing the query
    query = 'insert into customers (Name, City, GrowthStage, Industry, acqID) values ("'
    query += Name + '", "'
    query += City + '", "'
    query += GrowthStage + '", "'
    query += Industry + '", "'
    query += acqID + ')'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'


@startup.route('/startup/<StartupID>', methods=['GET'])
def get_startup_detail (id):

    query = 'SELECT StartupID, Name, City, GrowthStage, Industry, acqID FROM products WHERE StartupID = ' + str(id)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)



@startup.route('/startup/<StartupID>', methods=['PUT'])
def update_startup_detail(startup_id):
    
    data = request.json
    current_app.logger.info(f"Update request for StartupID {startup_id} with data: {data}")

    try:
        startup = startup.query.get(startup_id)
        if not startup:
            return jsonify({"error": "Startup not found"}), 404

        # Update fields from JSON data if available
        startup.Name = data.get('Name', startup.Name)
        startup.City = data.get('City', startup.City)
        startup.GrowthStage = data.get('GrowthStage', startup.GrowthStage)
        startup.Industry = data.get('Industry', startup.Industry)
        startup.acqID = data.get('acqID', startup.acqID)

        db.session.commit()  # Commit the changes to the database
        return jsonify({"success": "Startup details updated successfully"}), 200

    except Exception as e:
        current_app.logger.error(f"Error updating startup: {e}")
        db.session.rollback()
        return jsonify({"error": "Failed to update startup details"}), 500


@startup.route('/startup/<StartupID>/document', methods=['GET'])
def get_documents(startup_id):

    query = 'SELECT * FROM Document WHERE StartupID = ' + str(startup_id)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)


@startup.route('/startup/<StartupID>/document/<docID>', methods=['GET'])
def get_documents1(startup_id, docID):

    query = 'SELECT * FROM Document WHERE StartupID = ' + str(startup_id) + "AND docID = " + str(docID)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)


@startup.route('/startup/<int:StartupID>/documents', methods=['POST'])
def create_document(StartupID):
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    documentType = the_data['documentType']
    fileSize = the_data["fileSize"]
    pageCount = the_data["pageCount"]
    wordCount = the_data["wordCount"]
    characterCount = the_data["characterCount"]
    startupID = StartupID



    # Constructing the query
    query = 'insert into customers (documentType, fileSize, pageCount, wordCount, characterCount, StartupID) values ("'
    query += documentType + '", "'
    query += fileSize + '", "'
    query += pageCount + '", "'
    query += wordCount + '", "'
    query += characterCount + '", "'
    query += startupID + ')'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

@startup.route('/startup/<StartupID>/documents/<docID>', methods=['DELETE'])
def delete_document(docID):
    query = 'DELETE FROM Documents WHERE docID = ' + str(docID)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)



@startup.route('/startup/<StartupID>/investmentOffers', methods=['GET'])
def get_invOpps(StartupID, OppID):
    query = 'SELECT * FROM InvestmentOpportunities WHERE StartupID = ' + str(StartupID) + "AND OppID = " + str(OppID)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)


@startup.route('/startup/<StartupID>/teamMembers', methods=['GET'])
def getTeamMembers(StartupID):
    query = 'SELECT * FROM TeamMembers WHERE StartupID = ' + str(id)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

@startup.route('/startup/<StartupID>/teamMembers', methods=['POST'])
def add_new_member(StartupID):
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    PhoneNumber = the_data['PhoneNumber']
    Name = the_data['Name']
    Email = the_data['Email']
    StartupID=StartupID


    # Constructing the query
    query = 'insert into customers (PhoneNumber, Name, StartupID, Email) values ("'
    query += PhoneNumber + '", "'
    query += Name + '", "'
    query += StartupID + '", "'
    query += Email + ')'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

@startup.route('/startup/<StartupID>/teamMembers', methods=['DELETE'])
def delete_teamMember(MemberID, StartupID):
    query = 'DELETE FROM TeamMembers WHERE StartupID = ' + str(StartupID) + "AND MemberID = " + str(MemberID)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)