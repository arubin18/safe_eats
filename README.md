
First, we must populate the database. 
Assuming psql is setup correctly, run the following. 

>> dropdb safe_eats
>> createdb safe_eats
>> psql safe_eats -af safe_eats.sql

=======================================================================================

We followed this tutorial when making our flask app: 
https://medium.com/@dushan14/create-a-web-application-with-python-flask-postgresql-and-deploy-on-heroku-243d548335cc

Make sure that you have flask and all necesary requirements installed. 

>> pip install Flask

Make sure the following have been run at some point. 

>> export APP_SETTINGS="config.DevelopmentConfig"
>> export DATABASE_URL="postgresql://localhost/safe_eats"

If there is no migrations or an update to migrations need to be made, run the following. 

>> python manage.py db init
>> python manage.py db migrate
>> python manage.py db upgrade

To delete the db and migrations and re-run, the following should do the trick:
>> dropdb safe_eats
>> createdb safe_eats
>> psql safe_eats -af safe_eats.sql
>> rm -rf migrations 

Once this has all been complete, run the following to run the app. 

>> python manage.py runserver


=======================================================================================

We have also provided all the web scraping code in the code portion of this submission.