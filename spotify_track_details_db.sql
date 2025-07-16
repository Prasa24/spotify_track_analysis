create database for_spotify;
use for_spotify;
create table if not exists spotify_tracks (
    id int auto_increment primary key,
    track_name varchar(255),
    artist varchar(255),
    album varchar(255),
    popularity int,
    duration_minutes float,
    release_date date
)
select * from spotify_tracks;
truncate table spotify_tracks;
