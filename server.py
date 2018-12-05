from flask import Flask, render_template, url_for, flash, request, session, redirect
from form import RegistrationForm, LoginForm
from dbinit import initialize
import psycopg2 as db

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234w7ecF4gh321q'

url = """postgres://ffpzkcsbsmkffc:0bf6c8ea8127f14cb4da7d50542d9dadffa30fd97640dc6260cdac27f9762656@ec2-79-125-8-105.eu-west-1.compute.amazonaws.com:5432/d4280d6o5jiga1"""
initialize(url)

@app.route('/home_page', methods=['GET', 'POST'])
def home_page():
    if request.method=="POST":
        login = LoginForm(request.form["username"], request.form["password"])
        try:
            connection = db.connect(url)
            cursor = connection.cursor()
            statement = "SELECT * FROM student WHERE ((username = %s) AND (password = %s))"
            cursor.execute(statement, (login.username, login.password))
            cursor.close()
            return redirect(url_for('profile'))
        except db.DatabaseError:
            connection.rollback()
            flash('Unsuccessful', 'danger')
        finally:
            connection.close()
    return render_template("home.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=="POST":
        myform = RegistrationForm(request.form["studentno"], request.form["username"], request.form["password"], request.form["name"], request.form["surname"])
        try:
            connection = db.connect(url)
            cursor = connection.cursor()
            statement = "INSERT INTO student VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(statement, (myform.studentno, myform.username, myform.password, myform.name, myform.surname))
            #result = cursor.fetchone()
            cursor.close()
            flash('Your account was created successfully')
            return redirect(url_for('home_page'))
        except db.DatabaseError:
            connection.rollback()
            flash('Unsuccessful', 'danger')
        finally:
            connection.close()
    return render_template('register.html')

@app.route("/profile")
def profile():
        connection = db.connect(url)
        cursor = connection.cursor()
        statement = "SELECT name FROM student"
        cursor.execute(statement)
        result = cursor.fetchall()
        sname = result
        for name in result:
            print(name)
            sname = name
        return render_template("profile.html", name=sname)


if __name__ == "__main__":
    app.run(debug=True)
