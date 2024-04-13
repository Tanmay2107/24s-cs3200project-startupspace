from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


startups = Blueprint('startup', __name__)

# Get all the products from the database
@startups.route('/startup', methods=['GET'])
def get_startups():
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

@startups.route('/startup', methods=['POST'])
def create_document(StartupID):
    data = request.json
    current_app.logger.info(f"Create document request for StartupID {StartupID} with data: {data}")

    # Create a new document instance
    new_startup = Document(
        Name=data.get('Name'),
        City=data.get("City"),
        GrowthStage=data.get("Growth Stage"),
        Industry=data.get("Industry")
    )

    db.session.add(new_startup)
    db.session.commit()  # Commit the new document to the database

    return jsonify({"success": "Document created successfully", "documentID": new_startup.id}), 201


@startups.route('/startup/<StartupID>', methods=['GET'])
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



@startups.route('/startup/<StartupID>', methods=['PUT'])
def update_startup_detail(startup_id):
    
    data = request.json
    current_app.logger.info(f"Update request for StartupID {startup_id} with data: {data}")

    try:
        startup = startups.query.get(startup_id)
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


@startups.route('/startups/<StartupID>/document', methods=['GET'])
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


@startups.route('/startups/<StartupID>/document/<docID>', methods=['GET'])
def get_documents(startup_id, docID):

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


@startups.route('/startup/<int:StartupID>/documents', methods=['POST'])
def create_document(StartupID):
    data = request.json
    current_app.logger.info(f"Create document request for StartupID {StartupID} with data: {data}")

    # Create a new document instance
    new_document = Document(
        documentType=data.get('documentType'),
        fileSize=data.get('fileSize'),
        pageCount=data.get('pageCount'),
        wordCount=data.get('wordCount'),
        characterCount=data.get('characterCount'),
        startup_id=StartupID  
    )

    db.session.add(new_document)
    db.session.commit()  # Commit the new document to the database

    return jsonify({"success": "Document created successfully", "documentID": new_document.id}), 201


@startups.route('/startup/<StartupID>/documents/<docID>', methods=['DELETE'])
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



@startups.route('/startup/<StartupID>/investmentOffers', methods=['GET'])
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


@startups.route('/startup/<StartupID>/teamMembers', methods=['GET'])
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

@startups.route('/startup/<StartupID>/teamMembers', methods=['POST'])
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

@startups.route('/startup/<StartupID>/teamMembers', methods=['DELETE'])
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