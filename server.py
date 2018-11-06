from flask import Flask, render_template, url_for
from form import RegistrationForm
import psycopg2 as db

app = Flask(__name__)
statement = """CREATE TABLE IF NOT EXISTS students(
        username VARCHAR PRIMARY KEY,
        password VARCHAR NOT NULL,
        studentno VARCHAR NOT NULL,
        name VARCHAR NOT NULL,
        surname VARCHAR NOT NULL
        )"""

connection = db.connect("dbname='postgres' user='postgres' host='localhost' password=''")
cursor = connection.cursor()
cursor.execute(statement)
connection.commit()
cursor.close()


@app.route("/")
def home_page():
    return render_template("home.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        name = form.name.data
        surname = form.surname.data
        try:
            connection = db.connect("dbname='postgres' user='postgres' host='localhost' password=''")
            cursor = connection.cursor()
            statement = "INSERT INTO students VALUES(%s, %s, %s, %s)"
            cursor.execute(statement, (usename, password, name, surname))
            result = cursor.fetchone()
            flash('Your account was created successfully')
        except db.DatabaseError:
            connection.rollback()
            flash('Unsuccessful', 'danger')
        finally:
            connection.close()
    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
