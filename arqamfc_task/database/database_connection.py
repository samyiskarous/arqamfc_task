import mysql.connector
from faker import Faker
from datetime import date

# 1- Set the database connection parameters
db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root112233",
        database="restful_apis"
)

# 2- Database handling object
my_database = db_connection.cursor()
