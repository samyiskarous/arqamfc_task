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
from flask_restful import Resource, Api
from datetime import datetime

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
                                WHERE id = 2"""
    cursor.execute(match_deliverable_sql)
    row = cursor.fetchone()
    match_date_string = row[0].strftime('%Y-%m-%d')
    match_date = datetime.strptime(match_date_string, '%Y-%m-%d')
    # get the current date
    if(datetime.now() > match_date):
        # Match deadline has not come yet
        
        # Now check if we have TWO collectors for this match
        # TWO collectors with a date BEFORE match's deadline
        
        
    else:
        return False

class Schedule(Resource):
    def get(self, user_id):
        # get the user_id
        result = getUserSchedule(user_id)
        response = jsonify({"Schedule for User ({})".format(user_id): result})
        return response
    
    
api.add_resource(Schedule, '/schedule/user/<int:user_id>')

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