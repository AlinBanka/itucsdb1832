from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators


class RegistrationForm:
    def __init__(self, studentno, username, password, name, surname):
        self.studentno = studentno
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname

    
class LoginForm:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class Course:
    def __init__(self, crn, name, grade=0, att=0, last=" ", lweight=0, lgrade=0):
        self.crn = crn
        self.name = name
        self.grade = grade
        self.attendance = att
        self.last = last
        self.last_grade = lgrade
        self.last_weight = lweight
        #self.studentno = studentno
        #self.teacherno = teacherno

class Database:
    def __init__(self):
        self.courses = {}
        self._last_key = 0

    def add_course(self, course):
        self._last_key += 1
        self.courses[self._last_key] = course
        return self._last_key

    def delete_course(self, key):
        if key in self.courses:
            del self.courses[key]

    def get_course(self, key):
        course = self.courses.get(key)
        if course is None:
            return None
        course_ = Course(course.crn, course.name, course.grade, course.attendance, course.last, course.last_weight, course.last_grade)
        return course_

    def get_courses(self):
        courses = []
        for key, course in self.courses.items():
            course_ = Course(course.crn, course.name, course.grade, course.attendance, course.last, course.last_weight, course.last_grade)
            courses.append((key, course_))
        return courses

class teacher_course:
    def __init__(self, crn, name, no):
        self.crn = crn
        self.name = name
        self.no = no

class teacher_db:
    def __init__(self):
        self.courses = {}
        self.last_key = 0

    def add_course(self, course):
        self.last_key += 1
        self.courses[self.last_key] = course
        return self.last_key

    def get_courses(self):
        courses = []
        for key, course in self.courses.items():
            course_ = teacher_course(course.crn, course.name, course.no)
            courses.append((key, course))
        return courses
