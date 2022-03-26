# dashboard_kea4.2-d1
 
 This is a dashboard with fakedata made in Python using Django and Plotly Express.

 Author: Jan Guilherme F. Dissing

 Steps:

 1- Have a postgresql server on Azure or other place.
 (If it is mysqldb you can change the configuration in jan/settings.py)

 2- edit settings.py in folder jan and connection.py in scripts_and_files (remove __EDIT from end.)

 3- Create virtual environment and install requirements.txt

 4- create superuser on django-admin

 5- run pop_database from scripts_and_files

 6- configure nginx and gunicorn on server (maybe u can skip this step if u run on localhost)

 7- go to webpage and see if its working.



 