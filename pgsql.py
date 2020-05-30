'''
Author: pyrotank
Project Name: Three Comas
description: "A class to interact with postgreSQL"
'''
import psycopg2
from psycopg2 import Error
class Pgsql:
    # constructor ----------------------------------------------------------
    # establishes a connection to the database and holds it open untll destructor is called.
    def __init__(self, usrname, password, dbname, host, port='5432'):
        try:
            self.connection = psycopg2.connect(user = usrname,
                                        password = password,
                                        host = host,
                                        port = port,
                                        database = dbname)

            self.cursor = self.connection.cursor()
            # Print PostgreSQL Connection properties
            print ( self.connection.get_dsn_parameters(),"\n")

            # Print PostgreSQL version
            self.cursor.execute("SELECT version();")
            record = self.cursor.fetchone()
            print("You are connected to - ", record,"\n")
  
        except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while establishing the connection: ", error)
  
    # destructor------------------------------------------------------------
    def __del__(self):
        #closing database connection.
        if(self.connection):    
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection is closed")
    
    # executeQuery ----------------------------------------------------------
    def executeSelectQuery(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            info = self.cursor.fetchall()

        except (Exception, psycopg2.DatabaseError) as error:
            print('Error while executing a query: ', error)

        return info
    # getTables --------------------------------------------------------
    def getTables(self):
        q = "SELECT table_schema, table_name FROM information_schema.tables "+ \
            "WHERE (table_schema = 'public')" + \
            "ORDER BY table_schema, table_name;"
        self.cursor.execute(q)
        return self.cursor.fetchall()
        
    # addTable --------------------------------------------------------------
    def addTable(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            print(cursor.fetchall())
            
        
        except (Exception, psycopg2.DatabaseError) as error:
            print('Error while creating a table: ', error)
        