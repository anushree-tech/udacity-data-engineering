## Project : Postgres

### Introduction

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

This project is to create a Postgres database with tables designed to optimize queries on song play analysis. I have created a database schema and ETL pipeline for this analysis. 

### Dataset

**Song datasets**
All json files are nested in subdirectories under /data/song_data. 
A sample of this files is:
```
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
```
**Log datasets** 
All json files are nested in subdirectories under /data/log_data. 
A sample of a single row of each files is:
```
{"artist":"Pavement", "auth":"Logged In", "firstName":"Sylvie", "gender", "F", "itemInSession":0, "lastName":"Cruz", "length":99.16036, "level":"free", "location":"Klamath Falls, OR", "method":"PUT", "page":"NextSong", "registration":"1.541078e+12", "sessionId":345, "song":"Mercy:The Laundromat", "status":200, "ts":1541990258796, "userAgent":"Mozilla/5.0(Macintosh; Intel Mac OS X 10_9_4...)", "userId":10}
```
### Schema Description

**Fact Table**

* songplays - records in log data associated with song plays i.e. records with page NextSong
Columns:
songplay_id (SERIAL) PRIMARY KEY: ID of each user song play
start_time (TIMESTAMP) NOT NULL: Timestamp of beggining of user activity
user_id (INT) NOT NULL: ID of user
level (VARCHAR): User level {free | paid}
song_id (VARCHAR): ID of Song played
artist_id (VARCHAR) : ID of Artist of the song played
session_id (INT) NOT NULL: ID of the user Session
location (VARCHAR): User location
user_agent (VARCHAR): Agent used by user to access Sparkify platform

**Dimension Tables**
* users - users in the app
Columns:
user_id (INT) PRIMARY KEY: ID of user
first_name (VARCHAR) NOT NULL: Name of user
last_name (VARCHAR) NOT NULL: Last Name of user
gender (CHAR): Gender of user {M | F}
level (VARCHAR): User level {free | paid}

* songs - songs in music database
Columns:
song_id (VARCHAR) PRIMARY KEY: ID of Song
title (VARCHAR) NOT NULL: Title of Song
artist_id (VARCHAR) NOT NULL: ID of song Artist
year (INT): Year of song release
duration (FLOAT) NOT NULL: Song duration in milliseconds

* artists - artists in music database
Columns:
artist_id (VARCHAR) PRIMARY KEY: ID of Artist
name (VARCHAR) NOT NULL: Name of Artist
location (VARCHAR): Name of Artist city
lattitude (FLOAT): Lattitude location of artist
longitude (FLOAT): Longitude location of artist

* time - timestamps of records in songplays broken down into specific units
Columns:
start_time (TIMESTAMP) PRIMARY KEY: Timestamp of row
hour (INT): Hour associated to start_time
day (INT): Day associated to start_time
week (INT): Week of year associated to start_time
month (INT): Month associated to start_time
year (INT): Year associated to start_time
weekday (INT): Name of week day associated to start_time

* Files:

sql_queries.py: Containing all SQL Queries to drop table , create table and insert data(To be run in terminal). It is imported in below three files.
create_tables.py: drop and create tables (To be run in terminal).
etl.ipnyb: Reads and load data from 1 file from directories to database for testing.
etl.py: loads data from json files for song_data and log_data from specified directories into database.
test.ipynb: To check the data in tables for testing.


### steps followed

1) Wrote DROP, CREATE and INSERT query statements in sql_queries.py

2) Run in console

`python create_tables.py`

3) Used test.ipynb Jupyter Notebook to interactively verify that all tables were created correctly.

4) Followed the instructions and completed etl.ipynb Notebook to create the blueprint of the pipeline to process and insert all data into the tables.

5) Once verified that base steps were correct by checking with test.ipynb, filled in etl.py program.

6) Run etl.py in console, and verify results 

`python etl.py`





