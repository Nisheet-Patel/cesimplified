import sqlite3
import os
import urllib.parse as urlparse
from pytube import YouTube, Playlist

con = sqlite3.connect('website/database.db')

cur = con.cursor()

CLEAR = 'cls'

def get_yt_video_id(url):
    if len(url) > 11:
        url_data = urlparse.urlparse(url)
        query = urlparse.parse_qs(url_data.query)
        video_id = query["v"][0]
        return video_id
    else:
        return url

def commit_changes(cur):
    print('''[ 1 ]  Save Changes\n[ 2 ]  Don't Save''')
    _input = input(":")
    if _input == '1':
        cur.execute('commit')
        print("Commit successfully")
    elif _input == '2':
        cur.execute('rollback')
        print("Rollback successfully")
    else:
        print("Input Invalid")
        commit_changes(cur)

def get_yt_video_title(link):
    video = YouTube(link)
    return video.title

def get_playlist_video_link(link):
    playlist = Playlist(link)
    return playlist.video_urls

def display_table(cur, table_name):
    Columns = []
    data = cur.execute(f'''select * from {table_name};''')
    for col in data.description:
        Columns.append(col[0])
    print(Columns)
    for row in data:
        print(row)

def display_row(cur, table_name, row_condition):
    Columns = []
    data = cur.execute(f'''SELECT * FROM {table_name} WHERE {row_condition}''')
    for col in data.description:
        Columns.append(col[0])
    print(Columns)
    for row in data:
        print(row)

def add_comma():
    global Qc, Query
    Qc += 1
    if Qc > 1:
        Query += ','
'''
-- Display Table --
users
Course
Topic
Videos

-- New --
Create Course
Create Topic
Add Videos

-- Modify --
Course
Topic
Videos

-- Delete --
Course
Topic
Videos

-- Manage User --
Add User
Remove User
Update User

-- Custom --
Custom Query

'''
while True:
    os.system(CLEAR)

    print(''' 
    [ 1 ]  Display Any Table
    [ 2 ]  Insert | Add New Entry
    [ 3 ]  Modify
    [ 4 ]  Delete
    [ 5 ]  Manage User
    [ 6 ]  Run Custom Query
    [ 0 ]  Exit''')
    _input = input(":")


    if _input == '1':
        while True:
            os.system(CLEAR)
            print('''- Display Any Table\n
            [ 1 ]  Users
            [ 2 ]  Course
            [ 3 ]  Topic
            [ 4 ]  Videos
            [ 0 ]  Back''')
            c_intput = input(':')
            if c_intput == '1':
                display_table(cur, 'users')
                input("\nPress Enter To Clear")
            elif c_intput == '2':
                display_table(cur, 'course')
                input("\nPress Enter To Clear")
            elif c_intput == '3':
                display_table(cur, 'topic')
                input("\nPress Enter To Clear")
            elif c_intput == '4':
                display_table(cur, 'videos')
                input("\nPress Enter To Clear")
            elif c_intput == '0':
                break
    elif _input == '2':
        while True:
            os.system(CLEAR)
            print('''- Add New Entry\n
            [ 1 ]  Course
            [ 2 ]  Topic
            [ 3 ]  Videos
            [ 0 ]  Back''')
            c_input = input(":")

            if c_input == '1':
                title = input("Title: ")
                cur.execute(f"INSERT INTO COURSE(TITLE) VALUES('{title}')")
                display_table(cur, 'course')
                commit_changes(cur)

            elif c_input == '2':
                title = input("Title: ")
                course_title = input("Course Title: ") 
                course_id = cur.execute(F"SELECT ID FROM COURSE WHERE TITLE = '{course_title}';").fetchall()
                course_id = course_id[0][0] if len(course_id) == 1 else 0
                cur.execute(f"INSERT INTO TOPIC(TITLE,COURSE_ID) VALUES('{title}', {course_id});")
                display_table(cur, 'topic')
                commit_changes(cur)

            elif c_input == '3':
                topic_title = input("Topic Title: ") 
                topic_id = cur.execute(F"SELECT ID FROM TOPIC WHERE TITLE = '{topic_title}';").fetchall()
                topic_id = topic_id[0][0] if len(topic_id) == 1 else 0
                print('[ 1 ] Videos Links [ 2 ] Playlist link')
                vp = input(':')
                if vp == '1':
                    video_links = input('YouTube videos links: ')
                    video_links = video_links.split(',')
                    for link in video_links:
                        video_id = get_yt_video_id(link)
                        title = get_yt_video_title(link)
                        cur.execute(f'''INSERT INTO VIDEOS VALUES("{video_id}", "{title}", "yt", {topic_id});''')
                        print(f"+ {video_id} | {title}")
                    print('\n')
                elif vp == '2':
                    playlist_link = input('Playlist Link: ')
                    playlist_link = get_playlist_video_link(playlist_link)

                    for link in playlist_link:
                        video_id = get_yt_video_id(link)
                        title = get_yt_video_title(link)
                        cur.execute(f'''INSERT INTO VIDEOS VALUES("{video_id}", "{title}", "yt", {topic_id});''')
                        print(f"+ {video_id} | {title}")
                    print('\n')

                display_table(cur, 'videos')
                commit_changes(cur)
            elif c_input == '0':
                break

    elif _input == '3':
        while True:
            print('''- Modify Existing Table Row|Entry
            [ 1 ]  Course
            [ 2 ]  Topic
            [ 3 ]  Videos
            [ 0 ]  Back''')
            c_input = input(': ')
            if c_input == '1':
                display_table(cur, 'course')
                id = input('Input ID: ')
                title = input("New Title: ")
                cur.execute(f"UPDATE COURSE SET TITLE = '{title}' WHERE ID = {id};")
                display_row(cur, 'course', f"ID={id}")
                commit_changes(cur)
            elif c_input == '2':
                print('''
                [ 1 ] Title
                [ 2 ] Course
                ''')
                cc = input(': ')
                if cc == '1':
                    display_table(cur, 'topic')
                    id = input('Input ID: ')
                    title = input("New Title: ")
                    cur.execute(f"UPDATE TOPIC SET TITLE = '{title}' WHERE ID = {id};")
                    display_row(cur, 'course', f"ID={id}")
                elif cc == '2':
                    display_table(cur, 'topic')
                    id = input('Input Topic ID: ')
                    os.system(CLEAR)
                    display_table(cur, 'course')
                    cid = input('New Course ID: ')
                    cur.execute(f"UPDATE TOPIC SET course_id = {cid} WHERE ID = {id};")
                    display_row(cur, 'topic', f"ID={id}")
                commit_changes(cur)
            elif c_input == '3':
                Qc = 0
                Query = '''UPDATE VIDEOS SET '''
                display_table(cur, 'videos')
                print("\nNOTE: Press [ Enter ] If you don't want to change\n")
                old_vid = input("Enter Old Video vid: ")
                new_link = input('New Video Link: ')
                new_title = input('New Video Title: ')
                new_vtype = input('New video Type [Ex: yt]: ')
                display_table(cur, 'topic')
                new_topic = input('New Topic ID: ')
                new_vid = None
                if new_link != '':
                    add_comma()
                    new_vid = get_yt_video_id(new_link)
                    
                    Query += f" vid = '{new_vid}'"
                
                if new_title != '':
                    add_comma()
                    Query += f" title = '{new_title}'"
                else:
                    add_comma()
                    new_title_ = get_yt_video_title(new_link)
                    Query += f" title = '{new_title_}'"
                
                if new_vtype != '':
                    add_comma()
                    Query += f" vtype = '{new_vtype}'"
                
                if new_topic != '':
                    add_comma()
                    Query += f" topic_id = {new_topic}"

                Query += f" WHERE vid = '{old_vid}';"
                
                print(Query)
                cur.execute(Query)
                display_row(cur, 'videos', f"vid = '{new_vid}'")
                commit_changes(cur)
            elif c_input == '0':
                break


    elif _input == '5':
        print('''- Manage User
    [ 1 ]  Add User
    [ 2 ]  Remove User
    [ 3 ]  Update User
    [ 0 ]  Back''')

    elif _input =='5':
        print('- Run Custom Query')

cur.close()