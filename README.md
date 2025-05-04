## TRIP PLANNER API
This REST API for Trip planning was built with FastAPI, SQLAlchemy, and SQLWorkbench.

## How to run the Project
- Install MySQL Workbench
- Install Python,Pydantic<2.0
- Create your virtualenv with `python -m venv env` and activate it `env/Scripts/activate`.
- Install the following requirements:
       -`pip install fastapi`
       -`pip install uvicorn` the server
       -`pip install sqlalchemy psycopg2-binary` ORM
       -`pip install sqlalchemy_utils`
       -`pip install pymysql`
       -`pip install cryptography` data encryption
       -`pip install werkzeug` for password hashing
- For MySQLWorkbench `mysql -u root -p` in the cmd, then create a user with a password `CREATE USER '< username> @ 'localhost' IDENTIFIED BY '<password>';`
  and grant all privileges `GRANT ALL PRIVILIGES ON *.* TO '<username' @ 'locahost';`
- Set up your MySQL Workbench database and set its URI in your ```database.py```
```
engine=create_engine("mysql+pymysql://<username>:<password>@localhost/<db_name>", echo=True)
```

- Create your database by running ``` python init_db.py ```
- Finally, run the API
```python -m  uvicorn main: app ``


## ROUTES TO IMPLEMENTED
is_staff - identifies a superuser
| METHOD | ROUTE | FUNCTIONALITY |ACCESS|
| ------- | ----- | ------------- | ------------- |
| *POST* | ```/auth/signup/``` | _Register new user_| _All users_|
| *POST* | ```/auth/login/``` | _Login user_|_All users_|
| *POST* | ```/trips/trip/``` | _Plan a trip_|_All users_|
| *PUT* | ```/trips/trip/update/{trip_id}/``` | _Update a trip_|_All users_|
| *PUT* | ```/trips/trip/status/{trip_id}/``` | _Update trip status_|_Superuser_|
| *DELETE* | ```/trips/trip/delete/{trip_id}/``` | _Delete/Remove a trip_ |_All users_|
| *GET* | ```/trips/user/ttrips/``` | _Get user's trips_|_All users_|
| *GET* | ```/trips/trips/``` | _List all trips made_|_Superuser_|
| *GET* | ```/trips/tripss/{trip_id}/``` | _Retrieve a trip_|_Superuser_|
| *GET* | ```/trips/user/trip/{trip_id}/``` | _Get user's specific trip_|
| *GET* | ```/docs/``` | _View API documentation_|_All users_|
