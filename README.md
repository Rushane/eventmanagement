# Event Management System Starter Code
Starter code for Event Management System

Commands to set up environment:
1. python -m venv venv

2. Activate virtual environment
source venv/bin/activate (Linux/Mac)
.\venv\Scripts\activate (Windows)

3. pip install -r requirements.txt

4. python run.py

(Use http://127.0.0.1:8080/ to access system)

Database:
1. Start Database server

2. cd C:/xampp/mysql/bin

3. mysql -h localhost -u root -p 

4. create database event_management;

5. python flask-migrate.py db init (not needed to run)
python flask-migrate.py db migrate (use if changes are made to models)
python flask-migrate.py db upgrade

(Alternative but not tested)
# start MySQL. Will create an empty database on first
start
$ mysql-ctl start
# stop MySQL
$ mysql-ctl stop
# run the MySQL interactive shell
$ mysql-ctl cli


