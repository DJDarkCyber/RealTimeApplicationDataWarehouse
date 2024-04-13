from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DB_USERNAME, DB_PASSWORD, DB_DATABASE
from flask import render_template, jsonify
from flask import request, abort


app = Flask(__name__)

# configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DB_USERNAME}:{DB_PASSWORD}@localhost/{DB_DATABASE}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Start defining your database models here
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Student {self.name}>'

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(100), nullable=False)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)

class Time(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    academic_year = db.Column(db.String(20), nullable=False)
    semester = db.Column(db.String(20), nullable=False)

# Fact Model
class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    time_id = db.Column(db.Integer, db.ForeignKey('time.id'), nullable=False)
    grade = db.Column(db.String(2))
    attendance_percentage = db.Column(db.Float)

Professor.courses = db.relationship('Course', backref='professor')
Student.enrollments = db.relationship('Enrollment', backref='student')
Course.enrollments = db.relationship('Enrollment', backref='course')
Time.enrollments = db.relationship('Enrollment', backref='time')


# You can define more models for Course, Enrollment, etc.

# Create the tables in the database
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    # Query your database for data points
    # Example:
    enrollments_data = Enrollment.query.all()
    
    # Process and structure the data for Chart.js (or your chosen library) here
    data = {
        'labels': [enrollment.course.title for enrollment in enrollments_data],
        'datasets': [{
            'label': 'Grades',
            'data': [enrollment.grade for enrollment in enrollments_data]
        }]
    }
    
    # Return the processed data as JSON
    return jsonify(data)

@app.route('/api/enrollments')
def get_enrollments_data():
    # Fetch course names and the count of enrollments for each course
    data = db.session.query(
        Course.title, db.func.count(Enrollment.id).label('enrollment_count')
    ).join(Enrollment).group_by(Course.title).all()

    labels = [course[0] for course in data]
    values = [course[1] for course in data]
    
    return jsonify(labels=labels, datasets=[{'label': 'Enrollments', 'data': values}])

@app.route('/api/grades')
def get_grades_data():
    # Fetch grades and the count of each grade
    data = db.session.query(
        Enrollment.grade, db.func.count(Enrollment.id).label('grade_count')
    ).group_by(Enrollment.grade).all()

    labels = [grade[0] for grade in data]
    values = [grade[1] for grade in data]
    
    return jsonify(labels=labels, datasets=[{'label': 'Grades', 'data': values}])

@app.route('/api/add_student', methods=['POST'])
def add_student():
    try:
        # Extract student details from incoming JSON request
        data = request.get_json()
        new_student = Student(name=data['name'], email=data['email'])
        db.session.add(new_student)
        db.session.commit()
        return jsonify({'message': 'Student added successfully!', 'student': str(new_student)}), 201
    except Exception as e:
        # In case of an error, rollback the session and return an error message
        db.session.rollback()
        abort(400, description=str(e))

@app.route('/api/add_enrollment', methods=['POST'])
def add_enrollment():
    try:
        # Extract enrollment details from incoming JSON request
        data = request.get_json()
        new_enrollment = Enrollment(
            student_id=data['student_id'],
            course_id=data['course_id'],
            time_id=data['time_id'],
            grade=data['grade'],
            attendance_percentage=data['attendance_percentage']
        )
        db.session.add(new_enrollment)
        db.session.commit()
        return jsonify({'message': 'Enrollment added successfully!', 'enrollment': str(new_enrollment)}), 201
    except Exception as e:
        # In case of an error, rollback the session and return an error message
        db.session.rollback()
        abort(400, description=str(e))

@app.route('/api/students')
def get_students():
    students = Student.query.all()
    student_list = [{'id': student.id, 'name': student.name} for student in students]
    return jsonify(student_list)

@app.route('/api/courses')
def get_courses():
    courses = Course.query.all()
    course_list = [{'id': course.id, 'title': course.title} for course in courses]
    return jsonify(course_list)

@app.route('/api/times')
def get_times():
    times = Time.query.all()
    time_list = [{'id': time.id, 'semester': time.semester} for time in times]
    return jsonify(time_list)


if __name__ == '__main__':
    app.run(debug=True)