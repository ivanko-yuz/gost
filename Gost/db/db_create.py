import pyodbc

from db.db_connect import connect

def create_table():
   
    conn, cursor = connect()
    
    
    #Drop table if it already exist using execute() method.
    cursor.execute("DROP TABLE IF EXISTS SONGS")
    cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
    
     #Create table as per requirement
    sql = """CREATE TABLE SONGS (
       ID INT IDENTITY(1,1) PRIMARY KEY,
       TITTLE  CHAR(20) NOT NULL,
       AUTHOR  CHAR(20) NOT NULL,
       CREATED DATETIME NOT NULL,
       UPDATED DATETIME NOT NULL
       )"""
    
    cursor.execute(sql)
    
    #commit changes
    conn.commit()
    
    # disconnect from server
    conn.close()