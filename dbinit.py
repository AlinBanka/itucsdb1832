import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    """CREATE TABLE IF NOT EXISTS student(
        st_id SERIAL PRIMARY KEY,
        username VARCHAR UNIQUE NOT NULL,
        password VARCHAR NOT NULL,
        name VARCHAR NOT NULL,
        surname VARCHAR NOT NULL,
	gpa INTEGER DEFAULT 0,
	credit INTEGER DEFAULT 0,
	grade INTEGER,
	image BOOL DEFAULT FALSE,
	CHECK (credit <= 27)
        )""",
    """CREATE TABLE IF NOT EXISTS TEACHERS(
        code SERIAL PRIMARY KEY,
        username VARCHAR UNIQUE NOT NULL,
        password VARCHAR NOT NULL,
        name VARCHAR NOT NULL,
        surname VARCHAR NOT NULL,
        credit INTEGER DEFAULT 0,
        image BOOL DEFAULT FALSE,
        CHECK(credit <= 27)
        )""",
    """CREATE TABLE IF NOT EXISTS COURSES(
        crn INTEGER,
        name VARCHAR NOT NULL,
        grade FLOAT DEFAULT 0.0,
        attendance INTEGER DEFAULT 0,
        last VARCHAR DEFAULT 'none',
        last_weight FLOAT DEFAULT 0.0,
        last_grade INTEGER DEFAULT 0,
        timeslot VARCHAR,
        studentno INTEGER REFERENCES student
            ON DELETE CASCADE,
        teacherno INTEGER REFERENCES TEACHERS
            ON DELETE CASCADE,
        PRIMARY KEY(crn, teacherno, studentno),
	CHECK ((grade<=100.0) AND (attendance<=14))
        )""",
     """CREATE TABLE IF NOT EXISTS FINANCE(
	paid INTEGER DEFAULT 0,
	topay INTEGER DEFAULT 500,
        studentno INTEGER REFERENCES student
            ON DELETE CASCADE,
        last_confirmed INTEGER,
        isConfirmed BOOL,
        PRIMARY KEY(studentno),
	CHECK((paid<=500) AND (topay>=0))
	)""",
    """CREATE TABLE IF NOT EXISTS AVAILABLE(
        crn INTEGER UNIQUE,
        teacherno INTEGER REFERENCES TEACHERS
            ON DELETE CASCADE,
        available BOOL,
        timeslot VARCHAR,
        PRIMARY KEY(crn)
        )""",
    """CREATE TABLE IF NOT EXISTS MESSAGES(
        crn INTEGER,
        name VARCHAR,
        message text
        )"""
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            print(statement)
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = "postgres://ffpzkcsbsmkffc:0bf6c8ea8127f14cb4da7d50542d9dadffa30fd97640dc6260cdac27f9762656@ec2-79-125-8-105.eu-west-1.compute.amazonaws.com:5432/d4280d6o5jiga1"
    initialize(url)
