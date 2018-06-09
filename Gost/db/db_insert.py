import pyodbc
from datetime import datetime

from model.song import Song
from db.db_connect import connect


def insert(tittle,author):

    conn, cursor = connect()

    songs_list = [];

    sql = """INSERT INTO [dbo].[SONGS]
           (
            [TITTLE]
           ,[AUTHOR]
           ,[CREATED]
           ,[UPDATED])
            VALUES ('{0}','{1}','{2}','{3}')""".format(
                tittle, 
                author, 
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )

    print(sql)
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        conn.commit()
    except:
        # Rollback in case there is any error
        conn.rollback()
    
    # disconnect from server
    conn.close()