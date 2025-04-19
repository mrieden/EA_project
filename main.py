# from display import *
import mysql.connector
from mysql.connector import errorcode

config = {
    'user': 'root',           # change this if you're using another user
    'password': 'mrieden',  # replace with your MySQL password
    'host': 'localhost',
    'port': 3306
}

DB_NAME = 'timetable'

def load_data_from_database():
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        
        cnx.database = DB_NAME
        
        cursor.execute("SELECT * FROM departments")
        departments = cursor.fetchall()

        cursor.execute("SELECT * FROM courses")
        courses = cursor.fetchall()

        cursor.execute("SELECT * FROM instructors")
        instructors = cursor.fetchall()

        cursor.execute("SELECT * FROM rooms")
        rooms = cursor.fetchall()
        
        cursor.execute("SELECT * FROM timeslots")
        timeslots = cursor.fetchall()

        cnx.commit()
        print("successfully loaded data from database")
        
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()
        cnx.close()
    return departments, courses, instructors, rooms, timeslots
        
        
departments, courses, instructors, rooms, timeslots = load_data_from_database()
print(departments)
print(courses)
