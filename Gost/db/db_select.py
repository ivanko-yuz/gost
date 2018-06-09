import pyodbc

from model.song import Song
from db.db_connect import connect


def select():

    conn, cursor = connect()

    songs_list = [];

    sql = "select * from SONGS"

    try:
       # Execute the SQL command
       cursor.execute(sql)
       # Fetch all the rows in a list of lists.
       results = cursor.fetchall()

       for row in results:
           songs_list.append(Song(row[0], row[1], row[2]));
    except:
       print ("Error: unable to fetch data")
    
    # disconnect from server
    conn.close()

    return songs_list

