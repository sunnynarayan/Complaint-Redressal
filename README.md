# Complaint-Redressal
This is a web application based on Django framework used to implement a web centric Complaint Redressal System. This application uses MySQL database.

Instructions :
* Python version 2.7.6
* django 1.7
* Create a database (name as given in /crs/crs/settings.py) file.
* Change /crs/crs/settings.py->DATABASES according to mysql connection details
* download link of <b>MySQL-Python connector<b> : http://cdn.mysql.com/Downloads/Connector-Python/mysql-connector-python_2.0.3-1debian7.6_all.deb
* for all tables in manage.py comment managed = False if you want to create them using django
* for using encryption run folowing commands : <br>
1) - sudo apt-get install <b>libffi-dev</b> <br>
2) - sudo pip install <b>bcrypt</b>
* for generating dynamic pdf by django install report lab : <br> <b>sudo pip install reportlab</b>
