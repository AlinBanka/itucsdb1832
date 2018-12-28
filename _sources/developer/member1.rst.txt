Parts Implemented by Alin Banka
================================

The following section will give detailed information about the operations on the main tables

************
Student
************

1.CREATION
~~~~~~~~~~~

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS student(
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
        )
		
| The code for the creation is a classic SQL code which consists of definition of the variables and the constraints.

.. code-block:: python

	cursor = connection.cursor()
	statement = """INSERT INTO student(st_id, username, password, name, surname, grade)
						VALUES({}, \'{}\', \'{}\', \'{}\', \'{}\', {});""".format(myform.studentno, myform.username, myform.password, myform.name, myform.surname, int(request.form["grade"]))
	print(statement)
	cursor.execute(statement)
	connection.commit()
	
| The code above makes it possible to add a new student account to the system.

2.READING
~~~~~~~~~~

.. code-block:: python

	connection = db.connect(url)
	cursor = connection.cursor()
	statement = """SELECT st_id FROM student WHERE ((username = '%s') AND (password = '%s'));""" %(login.username, login.password)
	cursor.execute(statement)
	result = cursor.fetchall()
	user = None
	for (st_id, ) in result:
		user = st_id
	cursor.close()
	session.pop('user', None)
	if user!=None:
		session['user'] = (login.username)
		return redirect(url_for('profile', mid=user))
	else:
		flash("Wrong username or password!")
		return redirect(url_for('home'))
		
		
| The code above is part of the function which reads the username and the password from the table and enables login

.. code-block:: python

	connection = db.connect(url)
	cursor = connection.cursor()
	statement = """SELECT name, surname, gpa, grade FROM student
						WHERE st_id="""+mid
	cursor.execute(statement)
	result = cursor.fetchall()
	
| Whereas above you can see the code that reads the data of the student and fills up the profile page.

3.UPDATING
~~~~~~~~~~~

.. code-block:: python

	connection = db.connect(url)
	cursor = connection.cursor()
	statement = """UPDATE student SET username = \'{}\', password = \'{}\', name = \'{}\', surname = \'{}\'
	WHERE st_id = \'{}\';""".format(myform.username, myform.password, myform.name, myform.surname, no)   
	cursor.execute(statement, (myform.username, myform.password, myform.name, myform.surname))
	connection.commit()
	cursor.close()
	
| The code above is part of the update function. It makes it possible for the student to update his/her/their credentials.

4.DELETION
~~~~~~~~~~~

.. code-block:: python

	connection = db.connect(url)
	cursor = connection.cursor()
	statement = """DELETE FROM student WHERE st_id = {};""".format(studentno, studentno)
	print(statement)
	cursor.execute(statement)
	connection.commit()
	cursor.close()
	
| The code above makes it possible for the student to delete the account.

************
Teachers
************

1.CREATION
~~~~~~~~~~~

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS TEACHERS(
        code SERIAL PRIMARY KEY,
        username VARCHAR UNIQUE NOT NULL,
        password VARCHAR NOT NULL,
        name VARCHAR NOT NULL,
        surname VARCHAR NOT NULL,
        credit INTEGER DEFAULT 0,
        image BOOL DEFAULT FALSE,
        CHECK(credit <= 27)
        )
		
| The code for the creation is a classic SQL code which consists of definition of the variables and the constraints.

.. code-block:: python

	elif request.form["opt"]=="teacher":
		try:
			connection = db.connect(url)
			cursor = connection.cursor()
			statement = """INSERT INTO teachers(code, username, password, name, surname)
								VALUES({}, \'{}\', \'{}\', \'{}\', \'{}\');""".format(myform.studentno, myform.username, myform.password, myform.name, myform.surname)
			print(statement)
			cursor.execute(statement)
			connection.commit()
			continues...
			

| The code above makes it possible to add a new teacher account to the system.

2.READING
~~~~~~~~~~

.. code-block:: python

	connection = db.connect(url)
	cursor = connection.cursor()
	statement = """SELECT code FROM teachers WHERE ((username = '%s') AND (password = '%s'));""" %(login.username, login.password)
	cursor.execute(statement)
	result = cursor.fetchall()
		
		
| The code above is part of the function which reads the username and the password from the table and enables login

.. code-block:: python

	cursor = connection.cursor()
	statement = "SELECT name, surname FROM teachers WHERE code=" + mid
	cursor.execute(statement)
	result = cursor.fetchall()
	
| Whereas above you can see the code that reads the data of the teacher and fills up the profile page.

3.UPDATING
~~~~~~~~~~~

.. code-block:: python

	connection = db.connect(url)
	cursor = connection.cursor()
	statement = """UPDATE teachers SET username = \'{}\', password = \'{}\', name = \'{}\', surname = \'{}\'
	WHERE code = \'{}\';""".format(myform.username, myform.password, myform.name, myform.surname, no)
	cursor.execute(statement, (myform.username, myform.password, myform.name, myform.surname))
	connection.commit()
	
| The code above is part of the update function. It makes it possible for the teacher to update his/her/their credentials.

4.DELETION
~~~~~~~~~~~

.. code-block:: python

	connection = db.connect(url)
	cursor = connection.cursor()
	statement = """DELETE FROM teachers WHERE code = {};""".format(code)
	print(statement)
	cursor.execute(statement)
	connection.commit()
	cursor.close()
	return redirect(url_for('home_page'))
	
| The code above makes it possible for the teacher to delete the account.

*********
Courses
*********

1.CREATION
~~~~~~~~~~~

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS COURSES(
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
        )
		
| Above you can find the code that creates the table 'Courses'.

.. code-block:: python

	statement = """INSERT INTO courses(crn, name, grade, attendance, timeslot, studentno, teacherno)
                                        VALUES({}, \'{}\', DEFAULT, DEFAULT, \'{}\', {}, {});""".format(int(request.form["course"]), name[0], (course_list[int(request.form["course"])])[1], (studentno), int(t))
	cursor.execute(statement)
	connection.commit()

| The code that adds courses.

2.READING
~~~~~~~~~~

.. code-block:: python

	statement = """SELECT crn, name, grade, attendance, last, last_weight, last_grade FROM courses
						WHERE studentno="""+mid
	cursor.execute(statement)
	result = cursor.fetchall()
	
| This code reads the list of courses a student has taken and posts it to his/her/their profile

3.UPDATING
~~~~~~~~~~~

.. code-block:: python

	statement = """UPDATE courses SET grade = {}, last = \'{}\', last_weight = {}, last_grade = {} WHERE (studentno = {}) AND (crn = {});""".format((ograde + weight*ngrade), cname, weight, request.form[str(key)], key, courseno)
	cursor.execute(statement)
	connection.commit()
	
| The above code adds a grade and other information for a task

.. code-block:: python

	statement = """UPDATE courses SET attendance = {} WHERE (studentno = {}) AND (crn = {});""".format((oattendance+1), int(key), int(courseno))
	cursor.execute(statement)
	connection.commit()
	
| And the above one updates attendance

4.DELETION
~~~~~~~~~~~

.. code-block:: python

	cursor = connection.cursor()
	statement = """DELETE FROM courses WHERE crn = {} AND studentno = {};""".format(crn, studentno)
	print(statement)
	cursor.execute(statement)
	connection.commit()
	cursor.close()
	
| The code above is responsible for dropping a course

**Notice that these are the main operations. There are many more readings and updates done on the main tables. You should check the source code on Github if you want to cover them all.**

*****************
Auxiliary Tables
*****************

Below you can find the creation code for the auxiliary table. Extensive operations are also done on the auxiliary tables, for which you can check the source code.

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS FINANCE(
	paid INTEGER DEFAULT 0,
	topay INTEGER DEFAULT 500,
	studentno INTEGER REFERENCES student
		ON DELETE CASCADE,
	last_confirmed INTEGER,
	isConfirmed BOOL,
	PRIMARY KEY(studentno),
	CHECK((paid<=500) AND (topay>=0))
	)
	
.. code-block:: sql

	CREATE TABLE IF NOT EXISTS AVAILABLE(
	crn INTEGER UNIQUE,
	teacherno INTEGER REFERENCES TEACHERS
		ON DELETE CASCADE,
	available BOOL,
	timeslot VARCHAR,
	PRIMARY KEY(crn)
	)
	
.. code-block:: sql

	CREATE TABLE IF NOT EXISTS MESSAGES(
	crn INTEGER,
	name VARCHAR,
	message text
	)
	
| This are the main table operations for the database system
| In the messages table a custom type named 'text' is used, which is actually a BLOB-like type.
