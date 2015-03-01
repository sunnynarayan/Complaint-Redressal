# Complaint-Redressal
This is a web application based on Django framework used to implement a web centric Complaint Redressal System. This application uses MySQL database.

Instructions :
* Create a database (name as given in /crs/crs/settings.py) file.
* Change /crs/crs/settings.py->DATABASES according to mysql connection details
* download link of MySQL-Python connector : http://cdn.mysql.com/Downloads/Connector-Python/mysql-connector-python_2.0.3-1debian7.6_all.deb
* for all tables in manage.py comment managed = False
* for using encryption run folowing commands :
1) - sudo apt-get install libffi-dev
2) - sudo pip install bcrypt
