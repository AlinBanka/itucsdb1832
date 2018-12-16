from flask import Flask, render_template, url_for, flash, request, session, redirect, Markup, g
from form import RegistrationForm, LoginForm, Course, Database, teacher_course, teacher_db, message, messages
from dbinit import initialize
import psycopg2 as db
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234w7ecF4gh321q'

APP_ROOT = os.path.dirname(os.path.abspath('_file_'))

url = "postgres://postgres@localhost:5432/postgres"
initialize(url)

course_list = {int(101):("Mathematics I", "Monday 8:30 - 11:30", 8),
               int(103):("Mathematics II", "Monday 8:30 - 11:30", 9),
               int(102):("English I", "Monday 13:30 - 16:30", 8),
               int(104):("English II", "Monday 13:30 - 16:30", 9),
               int(105):("Physics", "Tuesday 8:30 - 11:30", 9),
               int(106):("Chemistry", "Tuesday 13:30 - 16:30", 9),
               int(107):("Biology", "Wednesday 8:30 - 11:30", 9),
               int(108):("History", "Wednesday 13:30 - 16:30", 8),
               int(109):("Geography", "Thurday 8:30 - 11:30", 8),
               int(110):("Art", "Thursday 13:30 - 16:30", 8),
               int(111):("Computer Science", "Friday 8:30 - 11:30", 8),
               int(112):("Music", "Friday 13:30 - 16:30", 8),
               int(113):("Turkish I", "Monday 8:30 - 11:30", 9)}
@app.route('/')
def home():
    return redirect(url_for('home_page'))

@app.route('/home_page', methods=['GET', 'POST'])
def home_page():
    if request.method=="POST":
        login = LoginForm(request.form["username"], request.form["password"])
        if request.form["opt"]=="student":
            try:
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
            except db.DatabaseError:
                connection.rollback()
                flash('Unsuccessful', 'danger')
            finally:
                connection.close()
        elif request.form["opt"]=="teacher":
            try:
                connection = db.connect(url)
                cursor = connection.cursor()
                statement = """SELECT code FROM teachers WHERE ((username = '%s') AND (password = '%s'));""" %(login.username, login.password)
                cursor.execute(statement)
                result = cursor.fetchall()
                for (code, ) in result:
                    user = code
                cursor.close()
                session.pop('tuser', None)
                if user!=None:
                    session['tuser'] = (login.username)
                    return redirect(url_for('teacher_profile', mid=user))
                return redirect(url_for('teacher_profile', mid=user))
            except db.DatabaseError:
                connection.rollback()
                flash('Unsuccessful', 'danger')
            finally:
                connection.close()
    return render_template("home.html")

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=="POST":
        myform = RegistrationForm(request.form["studentno"], request.form["username"], request.form["password"], request.form["name"], request.form["surname"])
        if request.form["opt"]=="student":
            try:
                connection = db.connect(url)
                cursor = connection.cursor()
                statement = """INSERT INTO student(st_id, username, password, name, surname, grade)
                                    VALUES({}, \'{}\', \'{}\', \'{}\', \'{}\', {});""".format(myform.studentno, myform.username, myform.password, myform.name, myform.surname, int(request.form["grade"]))
                print(statement)
                cursor.execute(statement)
                connection.commit()
                statement = """INSERT INTO FINANCE(paid, topay, studentno, last_confirmed, isConfirmed) Values(DEFAULT, DEFAULT, {}, -1, 'f');""".format(request.form["studentno"])
                cursor.execute(statement)
                connection.commit()
                #result = cursor.fetchone()
                cursor.close()
                flash('Your account was created successfully')
                return redirect(url_for('home_page'))
            except db.DatabaseError:
                connection.rollback()
                flash('Unsuccessful', 'danger')
            finally:
                connection.close()
        elif request.form["opt"]=="teacher":
            try:
                connection = db.connect(url)
                cursor = connection.cursor()
                statement = """INSERT INTO teachers(code, username, password, name, surname)
                                    VALUES({}, \'{}\', \'{}\', \'{}\', \'{}\');""".format(myform.studentno, myform.username, myform.password, myform.name, myform.surname)
                print(statement)
                cursor.execute(statement)
                connection.commit()
                cursor.close()
                flash('Your account was created successfully')
                return redirect(url_for('home_page'))
            except db.DatabaseError:
                connection.rollback()
                flash('Unsuccessful', 'danger')
            finally:
                connection.close()
    return render_template('register.html')

@app.route("/profile/<mid>")
def profile(mid):
    if g.user:
        connection = db.connect(url)
        cursor = connection.cursor()
        statement = """SELECT name, surname, gpa, grade FROM student
                            WHERE st_id="""+mid
        cursor.execute(statement)
        result = cursor.fetchall()
        for name, surname, gpa, grade in result:
            print(name)
            sname = name+" "+surname
            ngpa = gpa
            ngrade = grade
        statement = """SELECT crn, name, grade, attendance, last, last_weight, last_grade FROM courses
                            WHERE studentno="""+mid
        cursor.execute(statement)
        result = cursor.fetchall()
        dtb = Database()
        for crn, name, grade, attendance, last, last_weight, last_grade in result:
            #output="<td>"+str(crn)+"</td> <td>"+name+"</td> <td>"+str(grade)+"</td> <td>"+str(attendance)+"</td>"
            print(crn, name, grade, attendance, last, last_weight, last_grade)
            dtb.add_course(Course(crn, name, grade, attendance, last, last_weight, last_grade))
        courses = dtb.get_courses()
        statement = """SELECT crn FROM courses WHERE studentno = {}""".format(mid)
        cursor.execute(statement)
        result = cursor.fetchall()
        check = True
        if not result:
            check = False
        #output = Markup(output)
        statement = """SELECT image FROM student WHERE st_id = {}""".format(mid)
        cursor.execute(statement)
        result = cursor.fetchall()
        for (image, ) in result:
            d = image
        if d:
            imagename = str(mid) + ".jpg"
        else:
            imagename = "default.png"
            print(imagename)
        return render_template("profile.html", name=sname, st=mid, gpa=ngpa, grade=ngrade, courses=courses, check=check, imagename=imagename)

@app.route("/update/<no>/<t>", methods=['GET', 'POST'])
def update(no, t):
    if request.method=="POST":
        myform = RegistrationForm(no, request.form["username"], request.form["password"], request.form["name"], request.form["surname"])
        if t=='s':
            try:
                connection = db.connect(url)
                cursor = connection.cursor()
                statement = """UPDATE student SET username = \'{}\', password = \'{}\', name = \'{}\', surname = \'{}\'
                WHERE st_id = \'{}\';""".format(myform.username, myform.password, myform.name, myform.surname, no)   
                cursor.execute(statement, (myform.username, myform.password, myform.name, myform.surname))
                connection.commit()
                cursor.close()
                flash('Your account was updated successfully')
                return redirect(url_for('profile', mid=no))
            except db.DatabaseError:
                connection.rollback()
                flash('Unsuccessful', 'danger')
            finally:
                connection.close()
        elif t=='t':
            try:
                connection = db.connect(url)
                cursor = connection.cursor()
                statement = """UPDATE teachers SET username = \'{}\', password = \'{}\', name = \'{}\', surname = \'{}\'
                WHERE code = \'{}\';""".format(myform.username, myform.password, myform.name, myform.surname, no)
                cursor.execute(statement, (myform.username, myform.password, myform.name, myform.surname))
                connection.commit()
                cursor.close()
                flash('Your account was updated successfully')
                return redirect(url_for('teacher_profile', mid=no))
            except db.DatabaseError:
                connection.rollback()
                flash('Unsuccessful', 'danger')
            finally:
                connection.close() 
    return render_template('update.html', st=no)

@app.route("/teacher_profile/<mid>")
def teacher_profile(mid):
        connection = db.connect(url)
        cursor = connection.cursor()
        statement = "SELECT name, surname FROM teachers WHERE code=" + mid
        cursor.execute(statement)
        result = cursor.fetchall()
        sname = result
        for name, surname in result:
            sname = name + " " + surname
        statement = """SELECT crn, name, count(studentno) FROM courses
                            WHERE teacherno = {}
                            GROUP BY crn, name""".format(mid)
        cursor.execute(statement)
        result = cursor.fetchall()
        dtb = teacher_db()
        for crn, name, no in result:
            dtb.add_course(teacher_course(crn, name, no))
        courses = dtb.get_courses()
        statement = """SELECT crn FROM available WHERE teacherno = {}""".format(mid)
        cursor.execute(statement)
        result = cursor.fetchall()
        check = True
        if not result:
            check = False
        statement = """SELECT image FROM teachers WHERE code = {}""".format(mid)
        cursor.execute(statement)
        result = cursor.fetchall()
        for (image, ) in result:
            d = image
        if d:
            imagename = str(mid) + ".jpg"
        else:
            imagename = "default.png"
            print(imagename)
        return render_template("teacher_profile.html", name=sname, scode=mid, courses=courses, check=check, imagename=imagename)


@app.route("/teacher_update/<code>", methods=['GET', 'POST'])
def teacher_update(code):
    if request.method=="POST":
        myform = RegistrationForm(studentno, request.form["username"], request.form["password"], request.form["name"], request.form["surname"])
        try:
            connection = db.connect(url)
            cursor = connection.cursor()
            print(studentno)
            statement = """UPDATE teachers SET username = \'{}\', password = \'{}\', name = \'{}\', surname = \'{}\'
            WHERE st_id = \'{}\';""".format(myform.username, myform.password, myform.name, myform.surname, studentno)   
            print(statement)
            cursor.execute(statement, (myform.username, myform.password, myform.name, myform.surname))
            connection.commit()
            cursor.close()
            flash('Your account was updated successfully')
            return redirect(url_for('profile', mid=studentno))
        except db.DatabaseError:
            connection.rollback()
            flash('Unsuccessful', 'danger')
        finally:
            connection.close()
    return render_template('update.html', st=studentno)

@app.route("/add_course/<studentno>", methods=['GET', 'POST'])
def add_course(studentno):
    print(studentno)
    temp = {}
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """SELECT crn FROM available;"""
    cursor.execute(statement)
    result = cursor.fetchall()
    for (crn, ) in result:
        temp[crn]=course_list[crn]
    for crn, name in temp.items():
        print(name)
    statement = """SELECT crn, timeslot FROM courses WHERE studentno = """+ studentno +";"
    cursor.execute(statement)
    result = cursor.fetchall()
    t = []
    if(result!=None):
        for crn, timeslot in result:
            del temp[int(crn)]
            t.append(timeslot)
    statement = """SELECT grade FROM student WHERE st_id = {};""".format(studentno)
    cursor.execute(statement)
    result = cursor.fetchall()
    x = []
    for (grade, ) in result:
        ngrade = grade
    for i in t:
        for key, l in temp.items():
            if(i==l[1]):
                x.append(key)
    for i in x:
        del temp[i]
    y = []
    for key, l in temp.items():
        if l[2]!=int(ngrade):
            y.append(key)
    for i in y:
        del temp[i]
    if request.method=="POST":
        try:
            if(request.form["course"]!="none"):
                name = temp[int(request.form["course"])]
                statement = "SELECT teacherno FROM available WHERE crn = "+request.form["course"]
                connection = db.connect(url)
                cursor = connection.cursor()
                cursor.execute(statement)
                result = cursor.fetchall()
                for (teacherno, ) in result:
                    t = teacherno
                statement = """INSERT INTO courses(crn, name, grade, attendance, timeslot, studentno, teacherno)
                                        VALUES({}, \'{}\', DEFAULT, DEFAULT, \'{}\', {}, {});""".format(int(request.form["course"]), name[0], (course_list[int(request.form["course"])])[1], (studentno), int(t))
                print(statement)
                cursor.execute(statement)
                connection.commit()
                statement = """UPDATE student SET credit = {} WHERE st_id = {};""".format("credit + 3", int(studentno))
                cursor.execute(statement)
                connection.commit()
                cursor.close()
                flash('Your account was updated successfully')
                return redirect(url_for('profile', mid=studentno))
        except db.DatabaseError:
            connection.rollback()
            flash('Unsuccessful', 'danger')
        finally:
            connection.close()
    return render_template('add_course.html', courses=temp)


@app.route("/enable_course/<teacherno>", methods=['GET', 'POST'])
def enable_course(teacherno):
    temp = {}
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """SELECT crn FROM available;"""
    cursor.execute(statement)
    result = cursor.fetchall()
    l=[]
    for (crn, ) in result:
        l.append(int(crn))
    for key, data in course_list.items():
        if key in l:
            continue
        else:
            temp[key]=data
    statement = """SELECT timeslot FROM available WHERE teacherno = """+ teacherno +";"
    cursor.execute(statement)
    result = cursor.fetchall()
    x = []
    for (timeslot, ) in result:
        for key, data in temp.items():
            if timeslot==data[1]:
                x.append(key)
    for i in x:
        del temp[i]
    if request.method=="POST":
        try:
            if(request.form["course"]!="none"):
                name = temp[int(request.form["course"])]
                print(name)
                connection = db.connect(url)
                cursor = connection.cursor()
                statement = """INSERT INTO available(crn, teacherno, available, timeslot)
                                        VALUES({}, {}, 't', \'{}\');""".format(int(request.form["course"]), teacherno, (course_list[int(request.form["course"])])[1])
                print(statement)
                cursor.execute(statement)
                connection.commit()
                statement = """UPDATE teachers SET credit = {} WHERE code = {};""".format("credit + 3", int(teacherno))
                cursor.execute(statement)
                connection.commit()
                cursor.close()
                flash('Your account was updated successfully')
                return redirect(url_for('teacher_profile', mid=teacherno))
        except db.DatabaseError:
            connection.rollback()
            flash('Unsuccessful', 'danger')
        finally:
            connection.close()
    return render_template('enable_course.html', courses=temp)

@app.route("/finance/<studentno>", methods=['GET', 'POST'])
def finance(studentno):
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """SELECT paid, topay, last_confirmed, isConfirmed FROM FINANCE WHERE studentno = {};""".format(studentno)
    cursor.execute(statement)
    result = cursor.fetchall()
    for paid, topay, last_confirmed, isConfirmed in result:
        mypaid = paid
        mytopay = topay
        mycode = int(last_confirmed)
        mybool = isConfirmed
    if request.method=="POST":
        try:
            print(mybool)
            if mybool == False and mycode!=-1:
                print("Your last payment has not been confirmed! You either have to wait for its confirmation or ask for assistance!")
            elif((mybool == False and mycode == -1) or mybool==True):
                paid = int(request.form["paid"])
                confirmation = int(request.form["confirm"])
                statement = """UPDATE FINANCE SET paid = {}, topay = {}, last_confirmed = {}, isConfirmed = 'f' WHERE studentno = {};""".format((mypaid+paid), (mytopay-paid), confirmation, studentno)
                print(statement)
                cursor.execute(statement)
                connection.commit()
                cursor.close()
                return redirect(url_for('profile', mid=studentno))
        except db.DatabaseError:
            connection.rollback()
            flash('Unsuccessful', 'danger')
        finally:
            connection.close()
            
    return render_template('finance.html', no = studentno, paid = mypaid, topay = mytopay, code = mycode)

@app.route("/add_grade/<courseno>/<course>", methods=['GET', 'POST'])
def add_grade(courseno, course):
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """SELECT courses.studentno, student.name FROM courses, student WHERE (courses.studentno =  student.st_id) AND (courses.crn = """+courseno+" );"
    cursor.execute(statement)
    result = cursor.fetchall()
    students = {}
    for studentno, name in result:
        students[studentno] = name
    if request.method=="POST":
        try:
            connection = db.connect(url)
            cursor = connection.cursor()
            weight = float(request.form["weight"])
            cname = request.form["type"]
            for key, name in students.items():
                statement = """SELECT grade FROM courses WHERE (studentno = {}) AND (crn = {});""".format(key, courseno)
                cursor.execute(statement)
                result = cursor.fetchall()
                ngrade = int(request.form[str(key)])
                print(ngrade)
                for (grade, ) in result:
                    ograde = int(grade)
                    print(ograde)
                statement = """UPDATE courses SET grade = {}, last = \'{}\', last_weight = {}, last_grade = {} WHERE (studentno = {}) AND (crn = {});""".format((ograde + weight*ngrade), cname, weight, request.form[str(key)], key, courseno)
                print(statement)
                cursor.execute(statement)
                connection.commit()
                statement = """SELECT gpa, credit FROM student WHERE st_id = {};""".format(key)
                cursor.execute(statement)
                result = cursor.fetchall()
                for gpa, credit in result:
                    ngpa = int(gpa)
                    ncredit = int(credit)
                ngpa = ngpa + (3/ncredit)*weight*int(request.form[str(key)])
                statement = """UPDATE student SET gpa = {} WHERE st_id = {};""".format(ngpa, key)
                cursor.execute(statement)
                connection.commit()
        except db.DatabaseError:
            connection.rollback()
            flash('Unsuccessful', 'danger')
        finally:
            connection.close()
    
    return render_template('add_grade.html', students = students, course=course)

@app.route("/add_attendance/<courseno>/<course>", methods=['GET', 'POST'])
def add_attendance(courseno, course):
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """SELECT courses.studentno, student.name FROM courses, student WHERE (courses.studentno =  student.st_id) AND (courses.crn = """+courseno+" );"
    cursor.execute(statement)
    result = cursor.fetchall()
    students = {}
    for studentno, name in result:
        students[studentno] = name
    if request.method=="POST":
        try:
            for key, value in (request.form).items():
                connection = db.connect(url)
                cursor = connection.cursor()
                statement = """SELECT attendance FROM courses WHERE (studentno = {}) AND (crn = {});""".format(int(key), int(courseno))
                cursor.execute(statement)
                result = cursor.fetchall()
                for (attendance, ) in result:
                    oattendance = attendance
                statement = """UPDATE courses SET attendance = {} WHERE (studentno = {}) AND (crn = {});""".format((oattendance+1), int(key), int(courseno))
                cursor.execute(statement)
                connection.commit()
        except db.DatabaseError:
            connection.rollback()
            flash('Unsuccessful', 'danger')
        finally:
            connection.close()
    
    return render_template('add_attendance.html', students = students, course=course)

@app.route("/drop_student/<studentno>", methods=['GET', 'POST'])
def drop_student(studentno):
    try:
        connection = db.connect(url)
        cursor = connection.cursor()
        statement = """DELETE FROM student WHERE st_id = {};""".format(studentno, studentno)
        print(statement)
        cursor.execute(statement)
        connection.commit()
        cursor.close()
        return redirect(url_for('home_page'))
    except db.DatabaseError:
        connection.rollback()
        flash('Unsuccessful', 'danger')
    finally:
        connection.close()
    return redirect(url_for('home_page'))

@app.route("/drop_teacher/<code>", methods=['GET', 'POST'])
def drop_teacher(code):
    try:
        connection = db.connect(url)
        cursor = connection.cursor()
        statement = """DELETE FROM teachers WHERE code = {};""".format(code)
        print(statement)
        cursor.execute(statement)
        connection.commit()
        cursor.close()
        return redirect(url_for('home_page'))
    except db.DatabaseError:
        connection.rollback()
        flash('Unsuccessful', 'danger')
    finally:
        connection.close()
    return redirect(url_for('home_page'))

@app.route("/drop_course/<crn>/<studentno>", methods=['GET', 'POST'])
def drop_course(crn, studentno):
    try:
        connection = db.connect(url)
        cursor = connection.cursor()
        statement = """DELETE FROM courses WHERE crn = {} AND studentno = {};""".format(crn, studentno)
        print(statement)
        cursor.execute(statement)
        connection.commit()
        cursor.close()
    except db.DatabaseError:
        connection.rollback()
        flash('Unsuccessful', 'danger')
    finally:
        connection.close()
    return redirect(url_for('profile', mid=studentno))

@app.route("/upload/<studentno>", methods=['POST'])
def upload(studentno):
    target = os.path.join(APP_ROOT, 'static/')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    b = studentno
    file = request.files["myFile"]
    filename = b + ".jpg"
    print(b)
    destination = "/".join([target, filename])
    file.save(destination)
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """UPDATE student SET image = True WHERE st_id = {};""".format(b)
    cursor.execute(statement)
    connection.commit()
    print(statement)
    return redirect(url_for('profile', mid=b))

@app.route("/tupload/<studentno>", methods=['POST'])
def tupload(studentno):
    target = os.path.join(APP_ROOT, 'static/')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    b = studentno
    file = request.files["myFile"]
    filename = b + ".jpg"
    print(b)
    destination = "/".join([target, filename])
    file.save(destination)
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """UPDATE teachers SET image = True WHERE code = {};""".format(b)
    cursor.execute(statement)
    connection.commit()
    print(statement)
    return redirect(url_for('teacher_profile', mid=b))

@app.route("/drop_session")
def drop_session():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route("/drop_tsession")
def drop_tsession():
    session.pop('tuser', None)
    return redirect(url_for('home'))

@app.route("/message_board/<crn>/<studentno>/<t>", methods=['GET', 'POST'])
def message_board(crn, studentno, t):
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """SELECT crn, name, message FROM MESSAGES WHERE crn = {};""".format(crn)
    msgs = messages()
    cursor.execute(statement)
    result = cursor.fetchall()
    for crn, name, message1 in result:
        msgs.add_message(message(crn, name, message1))
    output = msgs.get_messages()
    statement = """SELECT name FROM courses WHERE crn = {};""".format(crn)
    cursor.execute(statement)
    result = cursor.fetchall()
    for (name, ) in result:
        f=name
    if request.method=="POST":
        msg=request.form["msg"]
        if t=='s':
            statement = """SELECT name FROM student WHERE st_id = {};""".format(studentno)
        if t=='t':
            statement = """SELECT name FROM teachers WHERE code = {};""".format(studentno)
        cursor.execute(statement)
        result = cursor.fetchall()
        for (name, ) in result:
            sname = name
        statement = """INSERT INTO MESSAGES(crn, name, message) VALUES({}, \'{}\', \'{}\');""".format(crn, sname, msg)
        cursor.execute(statement)
        connection.commit()
        return redirect(url_for('message_board', crn=crn, studentno=studentno, t=t))
    return render_template("message_panel.html", cname=f, messages=output)
        

if __name__ == "__main__":
    app.run(debug=True)
