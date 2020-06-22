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
    def __init__(self, usrname, password, dbname, host, port='5432', debug=False):
        try:
            self.connection = psycopg2.connect(user = usrname,
                                        password = password,
                                        host = host,
                                        port = port,
                                        database = dbname)
            print(f"[*] Connected to postgreSQL server @ {host}:{port}\n")
            cursor = self.connection.cursor()
            # Print PostgreSQL Connection properties
            if debug: print ( self.connection.get_dsn_parameters(),"\n")

            # Print PostgreSQL version
            if debug:
                cursor.execute("SELECT version();")
                record = cursor.fetchone()
                print(record,"\n")
  
        except (Exception, psycopg2.DatabaseError) as error :
            print ("[*] Error while establishing the connection: ", error)
        finally:
            cursor.close()
  
    # Destructor ------------------------------------------------------------------
    def __del__(self):
        #closing database connection.
        if(self.connection):    
            self.connection.close()
            print("\n[x] Connection to PostgreSQL server is closed ...")

    # Returns the connection to the db -------------------------------------------- 
    def getConnection(self):
        return self.connection

    # ExecuteQuery -----------------------------------------------------------------
    def executeQuery(self, query, q_type=''):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            return cursor.fetchall()
            
        except (Exception, psycopg2.DatabaseError) as error:
            if str(error) != "no results to fetch": 
                print(query)
                print(f'Error while executing {q_type} Query: ', error)
            else: 
                return str(error)
            # if error has occured, cancle the changes and rollback to orignal state 
            # before the the query was executed. 
            self.connection.rollback()
        
        finally:
            # print("closing cursor")
            cursor.close()        
    
    # getTables ------------------------------------------------------------------
    def getTables(self):
        q = "SELECT table_schema, table_name FROM information_schema.tables "+ \
            "WHERE (table_schema = 'public')" + \
            "ORDER BY table_schema, table_name;"
        res =  self.executeQuery(q, 'SELECT')
        if res: return res     
    # getColumns -----------------------------------------------------------------
    def getColumns(self, table_name):
        q = f"select column_name, data_type from information_schema.columns where table_name = '{table_name}';"
        res = self.executeQuery(q)
        return res
    
    # addTable --------------------------------------------------------------
    def addTable(self, query):
        self.executeQuery(query, 'Get Table')
        