Developer Guide
===============

Database Design
---------------

This project utilizes SQL to build the database system, and Flask to build the web application. In addition, it uses css/bootstrap and javascript for the UI.

**Database Design of the project**

The project consists of 6 tables. Three of them are main tables and the three others are auxiliary.

**Main Tables:**

| Student
| Teacher
| Courses

**Auxiliary Tables:**

| Finance
| Messages
| Available


**The main E/R diagram**

.. figure:: images/er.png
     :scale: 100 %
     :alt: Diagram

     Main relationship
	 
**The full relationships between all tables**

.. figure:: images/database.png
     :scale: 100 %
     :alt: Full relationship

     Full relationship

Code
----

**Structure of code**

| So basically there is a file called server.py. In that file all the backend functions are located. There you can find the code that renders the html templates, handles the database operations and deals with the session etc. There is another file called form.py where helper classes for the server file are located. Whereas in the dbinit.py file, you can find all the tables' creation code and the initialization code provided below.



**Initialization**

| The code for the initialization of the database is provided below

.. code-block:: python

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

**Python Framework**

| Flask is used as the main framework for the development of this project. The following python libraries and functions are used heavily

.. code-block:: python

	from flask import Flask, render_template, url_for, flash, request, session, redirect, Markup, g
	from dbinit import initialize
	import psycopg2 as db
	import os
	
| Flask templates are sometimes used to render the webpages. An example is shown below.

.. code-block:: html

	{% extends "layout.html" %}
	{% block title %}Create{% endblock %}
	{% block content %}
    <div class="form" style="margin-left:37%;padding-left:40px;padding-top:30px;padding-bottom:30px;">
        <form name="myForm", style="border:white;" method="POST" action="" onsubmit="return validateForm()">
		<fieldset style="border:0px;">      		  
		<input name="username" type="text" placeholder="username" required>
		<input name="password" type="password" placeholder="password" required>
		<input name="confirm" type="password" placeholder="confirm" required>
		<input name="name" type="text" placeholder="name" required>
		<input name="surname" type="text" placeholder="surname" required>
		<input name="studentno" type="text" placeholder="studentno" required>
		<input name="grade" type="text" placeholder="Grade"/>
		<div style="margin-bottom:10px;">
		  <p class="message" style="display:inline;">I am a:   
			  <select name="opt" style="width:150px;">
			  <option value="student">Student</option>
			  <option value="teacher">Teacher</option>
			  </select>
		  </p>
	  </div>
		<button>CREATE</button>
		</fieldset>
      		  <p class="message" style="margin-top:-2px;">Already have an account? <a href="{{ url_for('home_page') }}">Login</a></p>
        </form>
    </div>
	{% endblock %}
	
| Although Javascript is rarely used an example of its usage as a validator is written below

.. code-block:: javascript

	function validateForm() {
	  var x = document.forms["myForm"]["password"].value;
	  var y = document.forms["myForm"]["confirm"].value;
	  if (x != y) {
		alert("Password and confirmation do not match!");
		return false;
	  }
	  if(x.length <= 6){
		alert("Password length is too short!");
		return false;
	  }
	}
	
| CSS is also used. You can find a css file in the static folder in which the classes are written, but also inline and header style are used.

| Other operations are done like uploading a file etc. For more information check the source code.

.. toctree::

   member1
