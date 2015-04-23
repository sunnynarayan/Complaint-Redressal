# Complaint-Redressal
This is a web application based on Django framework used to implement a web centric Complaint Redressal System. This application uses MySQL database.

Instructions :
* Python version 2.7.6
* django 1.7
* Create a database (name as given in /crs/crs/settings.py) file.
* Change /crs/crs/settings.py->DATABASES according to mysql connection details
* download link of <b>MySQL-Python connector</b> : http://cdn.mysql.com/Downloads/Connector-Python/mysql-connector-python_2.0.3-1debian7.6_all.deb
* for all tables in manage.py comment managed = False if you want to create them using django
* for using encryption run folowing commands : <br><ol>
<li> - sudo apt-get install <b>libffi-dev</b> </li>
<li> - sudo pip install <b>bcrypt</b></li><br>
</ol>
* for generating dynamic pdf by django install report lab : <br> 
<b>sudo pip install reportlab</b>
<br>
<br>
* For viewing ER diagram of MySQL database : <br>
<ol><li> Using MySQL workbench<ol><br>
<li>Install <b>MySQL workbench </b> (<i>sudo apt-get install mysql-workbench</i>)</li> <br>
<li>Either create the ER diagram yourself or see file <b>/crs/login/ER.mwb</b></li><br>
</ol></li>
<li> Directly view pdf or image <br>
<ul>
	<li> You can access .pdf file in <b>/crs/login/ER.pdf</b> </li><br>
	<li> You can access .png file in <b>/crs/login/ER.png</b> </li><br>
</ul>
</li>
</ol> 
