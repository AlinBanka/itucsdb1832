from flask import Flask, render_template, url_for, flash
from form import RegistrationForm
import psycopg2 as db

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234w7ecF4gh321q'

statement = """CREATE TABLE IF NOT EXISTS students(
        username VARCHAR PRIMARY KEY,
        password VARCHAR NOT NULL,
        studentno VARCHAR NOT NULL,
        name VARCHAR NOT NULL,
        surname VARCHAR NOT NULL
        )"""

url = "postgres://ffpzkcsbsmkffc:0bf6c8ea8127f14cb4da7d50542d9dadffa30fd97640dc6260cdac27f9762656@ec2-79-125-8-105.eu-west-1.compute.amazonaws.com:5432/d4280d6o5jiga1"
connection = db.connect(url)
cursor = connection.cursor()
cursor.execute(statement)
connection.commit()
cursor.close()


@app.route("/")
def home_page():
    return render_template("home.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        name = form.name.data
        surname = form.surname.data
        studentno = form.studentno.data
        try:
            connection = db.connect(url)
            cursor = connection.cursor()
            statement = "INSERT INTO students VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(statement, (username, password, studentno, name, surname))
            result = cursor.fetchone()
            flash('Your account was created successfully')
            return redirect(url_for('login'))
        except db.DatabaseError:
            connection.rollback()
            flash('Unsuccessful', 'danger')
        finally:
            connection.close()
    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
