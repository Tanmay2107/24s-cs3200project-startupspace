from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


acquisitionTarget = Blueprint('acquisitionTarget', __name__)

# Get list of acquisitions for the given acquirerID
@acquisitionTarget.route('/acquisitionTarget/<acqid>', methods=['GET'])
def get_aqctargets(acqid):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    query = 'SELECT at.acqID, s.Name, s.StartupID, at.DateIdentified, at.status  FROM  AcquisitionTarget as at JOIN Startup as s WHERE at.acqID = ' + str(acqid)

    # use cursor to query the database for a list of targets
    cursor.execute(query)

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

# Add a new acquisitionTarget
@acquisitionTarget.route('/acquisitionTarget/<acqID>', methods=['PUT'])
def add_acqtargets(acqid):
    # get a cursor object from the database
    cursor = db.get_db().cursor()
    the_data = request.json
    status = the_data['status']
    StartupID = the_data['StartupID']
    acqID = str(acqid)
    interested = "true"



    query = "INSERT INTO AcquisitionTarget(status,StartupID,interested,acqID)"
    query = query + "VALUES ("
    query = query + "'" + status + "'"
    query = query + "'" + StartupID + "'"
    query = query + "'" + interested + "'"
    query = query + "'" + acqID + "'"
    query = query + ")"


    # use cursor to query the database for a list of targets
    cursor.execute(query)

    db.get_db().commit()
    
    return 'Success!'

# Edit a target
@acquisitionTarget.route('/acquisitionTarget/<targetID>', methods=['PUT'])
def update_aqctargets(targetID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()
    the_data = request.json
    status = the_data['status']
    interested = the_data['status']



    query = "UPDATE AcquisitionTarget SET "
    query = query + "status = "+ "'" + status + "', "
    query = query + "interested = "+ "'" + interested + "' "
    query = query + "WHERE targetID = " + str(targetID)


    # use cursor to query the database for a list of targets
    cursor.execute(query)

    db.get_db().commit()
    
    return 'Success!'


# delete a target
@acquisitionTarget.route('/acquisitionTarget/<targetID>', methods=['DELETE'])
def delete_aqctarget(targetID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()
    the_data = request.json




    query = "DELETE FROM AcquisitionTarget WHERE TargetID = " + str(targetID)

    # use cursor to query the database for a list of targets
    cursor.execute(query)

    db.get_db().commit()
    
    return 'Success!'

#gets all the acquisition targets that have concluded
@acquisitionTarget.route('/acquisitionTarget', methods=['GET'])
def get_alltargets():
    cursor = db.get_db().cursor()
    query = "select acq.Name AS acquirerName, st.Name AS StartUpName, at.status as Status, st.Industry, st.GrowthStage"
    query += " FROM Startup as st JOIN AcquisitionTarget as at on st.StartupID = at.StartupID JOIN Acquirers as acq on "
    query += "acq.acqID = at.acqID"
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response