# from website import db, create_app
# db.create_all(app=create_app())


import sqlite3
con = sqlite3.connect('website/database.db')

cur = con.cursor()

# Create Users Table
cur.execute(
''' 
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(25) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    detail VARCHAR(500)
);
'''
)

# Create Course Table
cur.execute(
'''
CREATE TABLE course (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL UNIQUE
);
'''
)

# Create Topic Table
cur.execute(
'''
CREATE TABLE topic (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(250) NOT NULL,
    course_id INTEGER,
    FOREIGN KEY(course_id) REFERENCES course (id)
);
'''
)

# Create Videos Table
cur.execute(
'''
CREATE TABLE videos (
    vid VARCHAR(20) PRIMARY KEY,
    title VARCHAR(250) NOT NULL,
    vtype VARCHAR(20) NOT NULL,
    topic_id INTEGER NOT NULL,
    FOREIGN KEY(topic_id) REFERENCES topic (id)
);
'''
)

# for row in cur.execute('SELECT * FROM stocks ORDER BY price'):
#     print(row)

# for row in cur.execute("select sql from sqlite_master where type = 'table' and name = 'videos'").fetchall():
#     for i in row:
#         print(i)
    
# print(cur.execute("select * from course").fetchall())
con.close()