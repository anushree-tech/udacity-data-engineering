## Project : Cloud Datawarehouse

### Introduction

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

ETL pipeline is build to extract  data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to.

### Project Description

Application of Data warehouse and AWS to build an ETL Pipeline for a database hosted on Redshift Will need to load data from S3 to staging tables on Redshift and execute SQL Statements that create fact and dimension tables from these staging tables to create analytics

### Project Datasets
```
Song Data Path --> s3://udacity-dend/song_data 
Log Data Path --> s3://udacity-dend/log_data 
Log Data JSON Path --> s3://udacity-dend/log_json_path.json
```

1) Song Dataset:

The first dataset is a subset of real data from the Million Song Dataset(https://labrosa.ee.columbia.edu/millionsong/). Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example:

*song_data/A/B/C/TRABCEI128F424C983.json*
*song_data/A/A/B/TRAABJL12903CDCF1A.json*

And below is an example of what a single song file, TRAABJL12903CDCF1A.json, looks like.

```
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
```

2) Log Dataset

The second dataset consists of log files in JSON format. The log files in the dataset with are partitioned by year and month. For example:

*log_data/2018/11/2018-11-12-events.json*
*log_data/2018/11/2018-11-13-events.json*

And below is an example of what a single log file, 2018-11-13-events.json, looks like.

```
{"artist":"Pavement", "auth":"Logged In", "firstName":"Sylvie", "gender", "F", "itemInSession":0, "lastName":"Cruz", "length":99.16036, "level":"free", "location":"Klamath Falls, OR", "method":"PUT", "page":"NextSong", "registration":"1.541078e+12", "sessionId":345, "song":"Mercy:The Laundromat", "status":200, "ts":1541990258796, "userAgent":"Mozilla/5.0(Macintosh; Intel Mac OS X 10_9_4...)", "userId":10}
```

### Schema for Song Play Analysis

A Star Schema would be required for optimized queries on song play queries

**Fact Table:**

* songplays - records in event data associated with song plays i.e. records with page NextSong songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

**Dimension Tables:**

* users - users in the app user_id, first_name, last_name, gender, level

* songs - songs in music database song_id, title, artist_id, year, duration

* artists - artists in music database artist_id, name, location, lattitude, longitude

* time - timestamps of records in songplays broken down into specific units start_time, hour, day, week, month, year, weekday

### Project

**Project include six files:**

1. create_table.py : In this file fact and dimension tables are created for the star schema in Redshift .

2. etl.py: In this file we load data from S3 into staging tables on Redshift and then process that data into your analytics tables on Redshift.

3. sql_queries.py  : In this file SQL statements are defined, which will be imported into the two other files above.

4. create_redshift_cluster.py : In this file we create Iam role, attach policy and create cluster.

5. dwh.cfg : This file has configuration details.

6. README.md : In this file is detailed information about the project and files.

### How to Run

1. open Terminal and execute create_tables file using below command
python create_tables.py

2. After ist step is successfully completed execute etl file using below command
python etl.py