import pyodbc

from db.db_connect import connect

def create():
    print('Enabeling connection')
    conn, cursor = connect()
    
    print('Creation Started')
    print('Checking in table exist')
    #Drop table if it already exist using execute() method.
    cursor.execute("DROP TABLE IF EXISTS SONGS")
    
     #Create table as per requirement
    sql = """CREATE TABLE SONGS (
       ID INT IDENTITY(1,1) PRIMARY KEY,
       TITTLE  CHAR(120) NOT NULL,
       AUTHOR  CHAR(120) NOT NULL,
       CREATED DATETIME NOT NULL,
       UPDATED DATETIME NOT NULL
       )"""

    print('Creating new table')
    cursor.execute(sql)

    #commit changes
    print('Commiting changes')
    conn.commit()

    print('Creation ended')

    # disconnect from server
    print('Closing connection')
    conn.close()