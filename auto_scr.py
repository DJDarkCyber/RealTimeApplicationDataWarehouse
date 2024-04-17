import mysql.connector
from mysql.connector import Error
import requests
import os
import subprocess

import subprocess

def create_mysql_connection(host_name, user_name, user_password, database_name=None):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=database_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    
    return connection

def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

host_name = input("MySQL hostname > ")
user_name = input("MySQL username > ")
passwd    = input("MySQL password > ")
database_name = input("Enter new database name to create > ")

connection = create_mysql_connection(host_name, user_name, passwd)
create_database_query = f"CREATE DATABASE {database_name}"
create_database(connection, create_database_query)

db_connection = create_mysql_connection(host_name, user_name, passwd, database_name)
create_student_table_query = "CREATE TABLE student (id INTEGER PRIMARY KEY AUTO_INCREMENT, name VARCHAR(50) NOT NULL, email VARCHAR(120) UNIQUE NOT NULL);"
create_professors_table_query = "CREATE TABLE professor (id INTEGER PRIMARY KEY AUTO_INCREMENT, name VARCHAR(50) NOT NULL, department VARCHAR(100) NOT NULL);"
create_course_table_query = "CREATE TABLE course (id INTEGER PRIMARY KEY AUTO_INCREMENT, title VARCHAR(100) NOT NULL, department VARCHAR(100) NOT NULL, professor_id INTEGER, FOREIGN KEY (professor_id) REFERENCES professor(id));"
create_time_table_query = "CREATE TABLE time (id INTEGER PRIMARY KEY AUTO_INCREMENT, academic_year VARCHAR(20) NOT NULL, semester VARCHAR(20) NOT NULL);"
create_enrollment_table_query = "CREATE TABLE enrollment (id INTEGER PRIMARY KEY AUTO_INCREMENT, student_id INTEGER, course_id INTEGER, time_id INTEGER, grade VARCHAR(2), attendance_percentage FLOAT, FOREIGN KEY (student_id) REFERENCES student(id), FOREIGN KEY (course_id) REFERENCES course(id), FOREIGN KEY (time_id) REFERENCES time(id));"

execute_query(db_connection, create_student_table_query)
execute_query(db_connection, create_professors_table_query)
execute_query(db_connection, create_course_table_query)
execute_query(db_connection, create_time_table_query)
execute_query(db_connection, create_enrollment_table_query)


# Web Application Auto deploy

config = f"""DB_USERNAME="{user_name}"
DB_PASSWORD="{passwd}"
DB_DATABASE="{database_name}"
DB_HOSTNAME="{host_name}"
"""
config_file = open("config.py", "w")
config_file.write(config)
config_file.close()

content = requests.get("https://pastebin.com/raw/nkBxBu9q").content.decode()
web_auto_file = open("web_auto.py", "w")
web_auto_file.write(content)
web_auto_file.close()
subprocess.call(["python3 web_auto.py"], shell=True)
