import mysql.connector
from faker import Faker
from datetime import date

# 1- Set the database connection parameters
db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="arqamfc_task"
)

# 2- Database handling object
cursor = db_connection.cursor()
#
## 3- Create the needed tables
#create_shifts_table_query = """CREATE TABLE shifts (
#                                    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
#                                    user_id INT(10) UNSIGNED NOT NULL,
#                                    date DATE NOT NULL,
#                                    type ENUM("morning", "night") NOT NULL
#                                )"""
#
#cursor.execute(create_shifts_table_query);
#
#create_matches_table_query = """CREATE TABLE matches (
#                                    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
#                                    deadline DATE NOT NULL
#                                )"""
#
#cursor.execute(create_matches_table_query);
#
## 4- commit the tables to database
#db_connection.commit()
#
#
## 5- start generating fake data 
#
## myFactory for generating fake data
#myFactory = Faker()
#
## generate fake data for matches table
#for match in range(100):
#    deadline = myFactory.date_between_dates(date_start=date(2010, 7, 1), date_end=date(2010, 7, 20))
#    
#    new_match_query = """INSERT INTO matches 
#                            (deadline) VALUES ('{}')""".format(deadline)
#                            
#    cursor.execute(new_match_query)
#    
#    db_connection.commit()
#    
# generate fake data for shifts table
#for shift in range(150):
#    if((shift % 2) == 0):
#        shift_type = "morning"
#    else:
#        shift_type = "night"
#    
#    shift_date = myFactory.date_between_dates(date_start=date(2010, 7, 1), date_end=date(2010, 7, 20))
#    
#    user_id = myFactory.random_int()
#    
#    new_shift_query = """INSERT INTO shifts 
#                            (user_id, date, type) VALUES ({}, '{}', '{}')""".format(user_id, shift_date, shift_type)
#                            
#    cursor.execute(new_shift_query)
#    
#    db_connection.commit()

# Task - START
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from datetime import datetime
import array as arr
from cerberus import Validator
import json

app = Flask(__name__)
# that Api is built on top of App
api = Api(app)

def getUserSchedule(user_id):
    # Query for getting the schedule for a certain collector
    get_collector_schedule_sql = """
                                    SELECT date, type
                                    FROM shifts
                                    WHERE user_id = {}
                                    """.format(user_id)
    # execute the query
    cursor.execute(get_collector_schedule_sql)
    rows = cursor.fetchall()
    return rows

# Verify whether a match can be delivered, or will be delayed 
def matchIsDeliverable(match_id):
    # If the match is deliverable, there must be 2 conditions
    # 1- its deadline must have not come yet
    # AND
    # 2- there should be TWO collectors for that match, 2 conditions here too
        # A) Night collector + Morning collector
        # B) their date attribute MUST be before the match's deadline
    
    # compare match's deadline with today's date
    # getting a certain match query
    match_deliverable_sql = """
                                SELECT deadline
                                FROM matches
                                WHERE id = {}""".format(match_id)
    cursor.execute(match_deliverable_sql)
    match = cursor.fetchone()
    match_deadline_string = match[0].strftime('%Y-%m-%d')
    match_deadline = datetime.strptime(match_deadline_string, '%Y-%m-%d')
    # get the current date
    if(datetime.now() > match_deadline):
        # Match deadline has not come yet
    
        # Now check if we have TWO collectors for this match
        # TWO collectors with a date BEFORE match's deadline
        
        #count the morning collectors
        match_morning_coll_by_date_sql = """
                                            SELECT count(*) 
                                            FROM shifts
                                            WHERE date <= '{}'
                                            AND type = 'morning'
                                            """.format(match_deadline_string)
        cursor.execute(match_morning_coll_by_date_sql)
        match_morning_coll_count = cursor.fetchone()[0]
        
        #count the night collectors
        match_night_coll_by_date_sql = """
                                        SELECT count(*)
                                        FROM shifts
                                        WHERE date <= '{}'
                                        AND type = 'night'
                                        """.format(match_deadline_string)
        cursor.execute(match_night_coll_by_date_sql)
        match_night_coll_count = cursor.fetchone()[0]
        
        match_collectors_count = match_morning_coll_count + match_night_coll_count
        
        if(match_collectors_count >= 2):
            # Match IS deliverable
            return 0
        else:
            # Match is NOT deliverable - Lack of Collectors
            return 2            
    else:
        # Match is NOT deliverable - Deadline
        return 1

# Prepare a list of matches and whether they're deliverable or not
def getPrepareMatchesList():
    get_all_matches_sql = """
                            SELECT *
                            FROM matches"""
    cursor.execute(get_all_matches_sql)
    matches = cursor.fetchall()
    
    prepared_matches = []
    match_statuses = ["Deliverable", "Delayed - Deadline", "Delayed - Collectors"]

    for match in matches:
        match_status = match_statuses[matchIsDeliverable(match[0])]
        prepared_matches.append([match[0], match_status])
        
    return prepared_matches

# Validate the schdule request data
def validSchedule(schedule_data, method):
    if(method == 'insert'):
        validation_schema = {
                            'user_id': {
                                        'type': 'integer',
                                        'required': True
                                    },
                            'date': {
                                        'type': 'string',
                                        'required': True
                                    },
                            'type': {
                                        'type': 'string',
                                        'required': True
                                    },
                            }    
    else:
        validation_schema = {
                            'schedule_id' : {
                                        'type': 'integer',
                                        'required': True
                                    },
                            'user_id': {
                                        'type': 'integer',
                                        'required': False
                                    },
                            'date': {
                                        'type': 'string',
                                        'required': False
                                    },
                            'type': {
                                        'type': 'string',
                                        'required': False
                                    },
                            }
            
    validator = Validator(validation_schema)
    if(validator.validate(schedule_data)):
        return True
    else:
        raise ValueError(json.dumps(validator.errors))
        
def createNewSchedule(schedule_data):
    create_new_schedule_sql = """
                            INSERT INTO shifts
                            (user_id, date, type)
                            VALUES
                            ({}, '{}', '{}')
                            """.format(schedule_data['user_id'], 
                                       schedule_data['date'], 
                                    schedule_data['type'])
    cursor.execute(create_new_schedule_sql)
    db_connection.commit()
    
def deleteSchedule(schedule_data):
    validation_schema = {
                            'shift_id' : {
                                        'type': 'integer',
                                        'required': True
                                    }
                            }
    validator = Validator(validation_schema)
    if(validator.validate(schedule_data)):
        delete_schedule_sql = """
                                DELETE FROM shifts
                                WHERE id = {}
                                """.format(schedule_data['shift_id'])
        cursor.execute(delete_schedule_sql)
        db_connection.commit()
    else:
        raise ValueError(json.dumps(validator.errors))

class Schedule(Resource):
    # get the schedule of a collector
    def get(self, user_id):
        # get the user_id
        result = getUserSchedule(user_id)
        response = jsonify({"Schedule for User ({})".format(user_id): result})
        return response
    # add a schedule
    def post(self):
        schedule_data = request.get_json()
        if(validSchedule(schedule_data, 'insert')):
            createNewSchedule(schedule_data)
            return {"data": schedule_data}, 201
    # edit a schedule
    # def put(self):
    # schedule_data = request.get_json()
    # if(validSchedule(schedule_data, 'update')):
    # if()
            
    # delete a schedulte
    def delete(self):
        schedule_data = request.get_json()
        deleteSchedule(schedule_data)
        
        return {"data": {"message": "Schedule ({}) has been deleted!".format(schedule_data['shift_id'])}}
        
    
class Match(Resource):
    def get(self):
        matches_list = getPrepareMatchesList()
        response = jsonify({"Matches List": matches_list})
        return response
        
# API Endpoints
api.add_resource(Schedule, '/schedules/users/<int:user_id>', '/schedules')
api.add_resource(Match, '/matches')

if __name__ == '__main__':
    app.run(debug=True)

# Main Functions
#def matchIsDeliverable():

#def addSchedule():
#def editSchedule():
#def deleteSchedule():
#def validScheduleDate():
    
#def listMatches():
#def getMatchDeliveryDate():
# Task - END