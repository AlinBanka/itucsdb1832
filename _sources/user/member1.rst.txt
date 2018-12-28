Parts Implemented by Alin Banka
================================

Login
-----

In this part the user can just enter his primary credentials, which are the username and the password. In the selection box, the user should select 'Student' or 'Teacher'
according to his/her/their account type. Afterwards, he/she/they should click login. If the credentials are correct, the user will be redirected to his or her profile.
Otherwise, the user will be once again directed to the login page where he/she/they can reenter the credentials. If the user does not possess an account, but they
have been provided with a code from the school, which allows them to create an account, they can click 'Create an Account' to register.

.. figure:: images/main.png
     :scale: 50 %
     :alt: Landing page

     Home Page of the app
	 
Register
--------

If the user does not possess an account, but is authorized to have one by the obtainment of a unique code provided by the school, they should create the account right away.
In the register page a form is displayed from which the user can enter his/her/their credentials to start an account. Notice that is the user enters a password less than six characters, 
he/she/they will be shown a validation message that does not allow them to create an account until he/she/they enter a password of the correct length.
Similarly, the user will not be allowed to create an account if they enter a username that has been chosen by another user before them. Also, they will not be allowed to 
create an account if the password and the password confirmation do not match. They can select from the selection box if they are a 'Student' or a 'Teacher'. Notice that teachers do not have to fill
the 'Grade' text box. After completion of all text boxes they can click Create and proceed with their login.

.. figure:: images/register.png
     :scale: 50 %
     :alt: Register page

     Register Page of the app
	 
Student
-------

Notice that this section is only valid for the user of type 'Student'. This is the place where the main interaction happens.
You can upload a picture, update your credentials, look at your attendance and your grades, check tuition, add a course or participate in a message thread for a course
Notice that you can only delete your account as long as you have not enrolled in any course. Once you enroll the delete account option will be removed. That is because it does not make sense to unregister once your have participated courses and it breaks referential integrity.

As we can see, the delete function is allowed in this page because the student has not added any courses.

.. figure:: images/profile_with_delete.png
     :scale: 70 %
     :alt: Profile page

     Profile Page of the app
	 
But deletion is not allowed here. As we can see in the table, the student can view his/her/their cummulative grade, attendance, last grade with the weight and the name, and access the message panel of that course.

.. figure:: images/profile.png
     :scale: 50 %
     :alt: Profile page

     Profile Page of the app
	 
The student can click on the Add button to add courses. A list of enabled courses will appear, but the student will not be shown courses that conflict with his time slot or the year he is in.

.. figure:: images/courses.png
     :scale: 100 %
     :alt: Courses page

     Courses Page of the app

As for the message panel, the user can just click the MSG link and he/she/they will be directed.

.. figure:: images/msg.png
     :scale: 70 %
     :alt: Messages page

     Message Page of the app
	 
The student can drop a course if he/she/they has not received any grade yet. Once the student receives a grade, the drop button will disappear.

.. figure:: images/course_drop.png
     :scale: 70 %
     :alt: Profile page

     Profile Page of the app with one course drop enabled

For the finance part, the student can click in the tuition button and he/she/they will be redirected to the web page where the data will be added.

.. figure:: images/finance.png
     :scale: 70 %
     :alt: Finance page

     Finance Page of the App
	 
To update, just click on the Update link and add the credentials correctly.

.. figure:: images/update.png
     :scale: 70 %
     :alt: Update page

     Update Page of the App
	 
Teacher
-------

The update and delete operations, as well as the message panel, in this mode work exactly the same way as in the student section, so you are advised to take a look there for more information.
In addition to the mutual operations with the student section, the teachers can perform other operations.

.. figure:: images/tprofile.png
     :scale: 70 %
     :alt: Profile page

     Teacher Profile Page of the App

For enabling a course the teachers can select the 'Teach Course' link and be given a list of the courses they can enable for the student to add. Once they enable it
and the student selects it, the course will show up in the table in the profile.

In this table the teacher can a grade for a given task.

.. figure:: images/grade.png
     :scale: 70 %
     :alt: Grade page

     Grade Page of the App

Or they can add attendance for a particular lecture.

.. figure:: images/attendance.png
     :scale: 70 %
     :alt: Attendance page

     Attendance Page of the App
