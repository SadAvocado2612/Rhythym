import pymysql

conn = pymysql.connect(
        host='localhost',
        user='root', 
        password = "",
        db='Songs',
        )
cur = conn.cursor()

cur.execute('''
create database Rhythm;
use Rhythm;
create table Rythm(
songID numeric(6) primary key,
songName varchar(20),
duration numeric(3),
artist varchar(20),
genre varchar(20)
);
select * from Rhythm;
             ''')