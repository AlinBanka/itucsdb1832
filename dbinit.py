import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    """CREATE TABLE IF NOT EXISTS student(
        st_id SERIAL PRIMARY KEY,
        username VARCHAR NOT NULL,
        password VARCHAR NOT NULL,
        name VARCHAR NOT NULL,
        surname VARCHAR NOT NULL,
	    gpa INTEGER DEFAULT 0
        )""",
    """CREATE TABLE IF NOT EXISTS courses(
        code INTEGER,
        name VARCHAR NOT NULL,
        grade FLOAT DEFAULT 0.0,
        attendance INTEGER DEFAULT 0,
        studentno INTEGER REFERENCES student,
        PRIMARY KEY(code, studentno),
	    CHECK ((grade<=10.0) AND (attendance<=14))
        )""",
     """CREATE TABLE IF NOT EXISTS teachers(
        code INTEGER,
        username VARCHAR PRIMARY KEY,
        password VARCHAR NOT NULL,
        name VARCHAR NOT NULL,
        surname VARCHAR NOT NULL,
        studentno INTEGER REFERENCES student,
        PRIMARY KEY(code, studentno)
        )""",
     """CREATE TABLE IF NOT EXISTS finance(
	    paid INTEGER DEFAULT 0,
	    topay INTEGER DEFAULT 500,
        studentno INTEGER REFERENCES student,
        PRIMARY KEY(studentno),
	    CHECK((paid<=500) AND (topay>=0))
	    )"""
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()
        connection = dbapi2.connect(url)
        cursor = connection.cursor()
        statement = "INSERT INTO student VALUES (101, 'umut1', 'umutkari', 'Umut', 'kari')"
        cursor.execute(statement)


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    url = "postgres://postgres@localhost:5432/postgres"
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
