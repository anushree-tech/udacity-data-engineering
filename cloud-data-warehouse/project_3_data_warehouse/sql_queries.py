import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

#SET VARIABLES
LOG_DATA = config.get('S3','LOG_DATA')
LOG_JSONPATH =config.get('S3','LOG_JSONPATH')
SONG_DATA = config.get('S3','SONG_DATA')
ARN = config.get('IAM_ROLE','ARN')

# DROP TABLES

staging_events_table_drop = " DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF  EXISTS staging_songs "
songplay_table_drop = "DROP TABLE IF EXISTS fact_songplay "
user_table_drop = "DROP TABLE IF EXISTS dim_user "
song_table_drop = "DROP TABLE IF EXISTS dim_song"
artist_table_drop = "DROP TABLE IF EXISTS dim_artist "
time_table_drop = "DROP TABLE IF EXISTS dim_time"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_events (
artist          VARCHAR,
auth            VARCHAR, 
firstName       VARCHAR,
gender          VARCHAR,   
itemInSession   INTEGER,
lastName        VARCHAR,
length          FLOAT,
level           VARCHAR, 
location        VARCHAR,
method          VARCHAR,
page            VARCHAR,
registration    BIGINT,
sessionId       INTEGER,
song            VARCHAR,
status          INTEGER,
ts              TIMESTAMP,
userAgent       VARCHAR,
userId          INTEGER );
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs (
song_id            VARCHAR,
num_songs          INTEGER,
title              VARCHAR,
artist_name        VARCHAR,
artist_latitude    FLOAT,
year               INTEGER,
duration           FLOAT,
artist_id          VARCHAR,
artist_longitude   FLOAT,
artist_location    VARCHAR );
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS fact_songplay 
(songplay_id INTEGER IDENTITY(0,1) PRIMARY KEY , 
 start_time  TIMESTAMP sortkey, 
 user_id     INTEGER, 
 level       VARCHAR, 
 song_id     VARCHAR,
 artist_id   VARCHAR, 
 session_id  INTEGER, 
 location    VARCHAR, 
 user_agent  VARCHAR);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS dim_user
(
user_id INTEGER PRIMARY KEY distkey,
first_name      VARCHAR,
last_name       VARCHAR,
gender          VARCHAR,
level           VARCHAR
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS dim_song
(
song_id     VARCHAR PRIMARY KEY,
title       VARCHAR,
artist_id   VARCHAR distkey,
year        INTEGER,
duration    FLOAT
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS dim_artist
(
artist_id          VARCHAR PRIMARY KEY distkey,
name               VARCHAR,
location           VARCHAR,
latitude           FLOAT,
longitude          FLOAT
);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS dim_time
(
start_time    TIMESTAMP PRIMARY KEY sortkey distkey,
hour          INTEGER,
day           INTEGER,
week          INTEGER,
month         INTEGER,
year          INTEGER,
weekday       INTEGER
);
""")

# STAGING TABLES

staging_events_copy = ("""
COPY staging_events FROM {}
CREDENTIALS 'aws_iam_role={}'
COMPUPDATE OFF region 'us-west-2'
TIMEFORMAT as 'epochmillisecs'
TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL
FORMAT AS JSON {};
""").format(LOG_DATA,ARN,LOG_JSONPATH)

staging_songs_copy = ("""
COPY staging_songs FROM {}
CREDENTIALS 'aws_iam_role={}'
COMPUPDATE OFF region 'us-west-2'
TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL
FORMAT AS JSON 'auto';
""").format(SONG_DATA,ARN)

# FINAL TABLES

songplay_table_insert = (""" 
INSERT INTO fact_songplay (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
select  DISTINCT  to_timestamp(to_char(e.ts, '9999-99-99 99:99:99'),'YYYY-MM-DD HH24:MI:SS'),
e.userId,
e.level,
s.song_id,
s.artist_id,
e.sessionID,
e.location,
e.userAgent 
from staging_events e
join staging_songs s on 
e.song = s.title AND e.artist = s.artist_name;
""")

user_table_insert = ("""
INSERT INTO dim_user (user_id, first_name, last_name, gender, level)
select DISTINCT userId,
firstName,
lastName,
gender,
level 
from staging_events
where userId IS NOT NULL;;

""")

song_table_insert = ("""
INSERT INTO dim_song(song_id, title, artist_id, year, duration)
SELECT DISTINCT song_id as song_id,
                title as title,
                artist_id as artist_id,
                year as year,
                duration as duration
FROM staging_songs
WHERE song_id IS NOT NULL;
""")

artist_table_insert = ("""
INSERT INTO dim_artist(artist_id, name, location, latitude, longitude)
select DISTINCT artist_id,
artist_name,
artist_location,
artist_latitude,
artist_longitude
from staging_songs
WHERE artist_id IS NOT NULL;
""")

time_table_insert = ("""
INSERT INTO dim_time(start_time, hour, day, week, month, year, weekday)
select
DISTINCT  ts,
EXTRACT(hour from ts),
EXTRACT(day from ts),
EXTRACT(week from ts),
EXTRACT(month from ts),
EXTRACT(year from ts),
EXTRACT(weekday from ts)
from staging_events
where ts is not null;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
