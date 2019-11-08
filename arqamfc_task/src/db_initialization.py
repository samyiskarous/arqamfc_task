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
my_database = db_connection.cursor()

# 3- Create the needed tables
create_shifts_table_query = """CREATE TABLE shifts (
                                    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                                    user_id INT(10) UNSIGNED NOT NULL,
                                    date DATE NOT NULL,
                                    type ENUM("morning", "night") NOT NULL
                                )"""

my_database.execute(create_shifts_table_query);

create_matches_table_query = """CREATE TABLE matches (
                                    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                                    deadline DATE NOT NULL
                                )"""

my_database.execute(create_matches_table_query);

# 4- commit the tables to database
db_connection.commit()


# 5- start generating fake data 

# myFactory for generating fake data
myFactory = Faker()

# generate fake data for matches table
for match in range(100):
    deadline = myFactory.date_between_dates(date_start=date(2010, 7, 1), date_end=date(2010, 7, 20))
    
    new_match_query = """INSERT INTO matches 
                            (deadline) VALUES ('{}')""".format(deadline)
                            
    my_database.execute(new_match_query)
    
    db_connection.commit()
    
# generate fake data for shifts table
for shift in range(150):
    if((shift % 2) == 0):
        shift_type = "morning"
    else:
        shift_type = "night"
    
    shift_date = myFactory.date_between_dates(date_start=date(2010, 7, 1), date_end=date(2010, 7, 20))
    
    user_id = myFactory.random_int()
    
    new_shift_query = """INSERT INTO shifts 
                            (user_id, date, type) VALUES ({}, '{}', '{}')""".format(user_id, shift_date, shift_type)
                            
    my_database.execute(new_shift_query)
    
    db_connection.commit()

# Task - START
# Main Functions
def listUserSchedule(user_id):
    user_schedule_query = """SELECT * 
                                FROM shifts
                                """
    my_database.execute(user_schedule_query)
    print(my_database.rowcount) 
#def matchIsDeliverable():

#def addSchedule():
#def editSchedule():
#def deleteSchedule():
#def validScheduleDate():
    
#def listMatches():
#def getMatchDeliveryDate():
    
from flask import Flask
# Task - END