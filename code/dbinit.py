import os
try:
    os.unlink('moments.db')
except:
    print('First time creating this file!')
    
import sqlite3
conn = sqlite3.connect('moments.db')
cur = conn.cursor()

def show_all_rows(all_rows):
    for row in all_rows:
        print(row)
    print()

# writers table
cur.execute('''CREATE TABLE WRITERS
    (ACCOUNT text, NAME text, PASSWORD text, BIRTHYEAR integer, PROFILE text)''')
# init writers
cur.execute("INSERT INTO WRITERS VALUES ('sample_writer_1', 'Sample Writer', 'samplewriterpassword', 2000, 'Just another Moments maker')")
cur.execute("INSERT INTO WRITERS VALUES ('sample_writer_2', 'Sample Writer', 'samplewriterpassword', 2000, 'Just another Moments maker')")
conn.commit()
# search writers
cur.execute("SELECT * FROM WRITERS")
show_all_rows(cur.fetchall())

# moments table
cur.execute('''CREATE TABLE MOMENTS
    (ID integer, TITLE text, ACCOUNT text, MOMENT text, GENRE text, APPLAUSE integer)''')
# init moments
cur.execute("INSERT INTO MOMENTS VALUES (1, 'Sed Quis Purus', 'sample_writer_1', 'Sed quis purus non tortor auctor molestie maximus a ante. Vestibulum consectetur ligula risus…', 1)")
cur.execute("INSERT INTO MOMENTS VALUES (2, 'Lorem Ipsum', 'sample_writer_2', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua…', 1)")
conn.commit()
# search moments
cur.execute("SELECT * FROM MOMENTS")
show_all_rows(cur.fetchall())

# readers table
cur.execute('''CREATE TABLE READERS
    (ACCOUNT text, NAME text, PASSWORD text, BIRTHYEAR integer)''')
# init readers
cur.execute("INSERT INTO READERS VALUES ('sample_reader_1', 'Sample Reader', 'samplereaderpassword', 2000)")
cur.execute("INSERT INTO READERS VALUES ('sample_reader_2', 'Sample Reader', 'samplereaderpassword', 2000)")
conn.commit()
# search readers
cur.execute("SELECT * FROM READERS")
show_all_rows(cur.fetchall())

# bookmarks table
cur.execute('''CREATE TABLE BOOKMARKS
    (ACCOUNT text, ID integer)''')
# init bookmarks
cur.execute("INSERT INTO BOOKMARKS VALUES ('sample_reader_1', 2)")
cur.execute("INSERT INTO BOOKMARKS VALUES ('sample_reader_2', 1)")
conn.commit()
cur.execute("SELECT * FROM BOOKMARKS")
show_all_rows(cur.fetchall())

#applause table
cur.execute('''CREATE TABLE APPLAUSE
    (ACCOUNT text, ID integer)''')
# init applause
cur.execute("INSERT INTO APPLAUSE VALUES ('sample_reader_1', 2)")
cur.execute("INSERT INTO APPLAUSE VALUES ('sample_reader_2', 1)")
conn.commit()
cur.execute("SELECT * FROM APPLAUSE")
show_all_rows(cur.fetchall())