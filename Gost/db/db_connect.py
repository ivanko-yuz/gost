

import pyodbc

def connect():
    server = 'gostserver.database.windows.net'
    database = 'GostSongFinder'
    username = 'gostadmin'
    password = 'Pa$$word!305'
    driver= '{ODBC Driver 11 for SQL Server}'
    
    conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)

    return conn, conn.cursor()