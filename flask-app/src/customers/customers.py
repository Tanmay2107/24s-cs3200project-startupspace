########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


customers = Blueprint('customers', __name__)

# Get all customers from the DB
@customers.route('/customers', methods=['GET'])
def get_customers():
    cursor = db.get_db().cursor()
    cursor.execute('select id, company, last_name,\
        first_name, job_title, business_phone from customers')  #added id section
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get customer detail for customer with particular userID
@customers.route('/customers/<userID>', methods=['GET'])
def get_customer(userID):
    cursor = db.get_db().cursor()
    cursor.execute('select * from customers where id = {0}'.format(userID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


@customers.route('/customers', methods=['POST'])
def add_new_customer():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    company = the_data['company']
    lastName = the_data['last_name']
    firstName = the_data['first_name']
    jobTitle = the_data['job_title']
    businessPhone = the_data['business_phone']


    # Constructing the query
    query = 'insert into customers (company, last_name, first_name, job_title, business_phone) values ("'
    query += company + '", "'
    query += lastName + '", "'
    query += firstName + '", "'
    query += jobTitle + '", "'
    query += businessPhone + ')'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'




@customers.route('/customers/<id>', methods=['PUT'])
def update_customer(id):
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    company = the_data['company']
    lastName = the_data['last_name']
    firstName = the_data['first_name']
    jobTitle = the_data['job_title']
    businessPhone = the_data['business_phone']

    # Constructing the query
    query = 'UPDATE customers SET '
    condition_added = False

    if company != '':
        query += "company = '" + company + "'"
        condition_added = True
    if lastName != '':
        if condition_added:
            query += ", "
        query += "last_name = '" + lastName + "'"
        condition_added = True
    if firstName != '':
        if condition_added:
            query += ", "
        query += "first_name = '" + firstName + "'"
        condition_added = True
    if jobTitle != '':
        if condition_added:
            query += ", "
        query += "job_title = '" + jobTitle + "'"
        condition_added = True
    if businessPhone != '':
        if condition_added:
            query += ", "
        query += "business_phone = '" + businessPhone + "'"

    query += " WHERE id = '" + str(id) + "'"
    current_app.logger.info(query)


    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'