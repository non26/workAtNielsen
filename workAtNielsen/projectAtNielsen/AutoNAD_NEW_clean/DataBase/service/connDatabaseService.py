import os
import sqlite3
from sqlite3 import Error
class ConnDatabaseService():
    """This class is used to math the Service name to the corresponding DBName(reportName)"""
    def __init__(self, dbName="serviceMatchingDBName.db", table='service'):
        self.table = table
        self.thisFilePath = os.path.dirname(os.path.abspath(__file__))
        self.dataBase = dbName
        self.conn = None
        self.cursorObj = None
        self.connectDataBase()

    def connectDataBase(self):
        try:
            self.conn = sqlite3.connect(self.thisFilePath + "\\" + self.dataBase)
            self.cursorObj = self.conn.cursor()
            print("connecting to the DataBase...")
        except Error as e:
            print(e)

    def sql_createTable(self, table="service"):
        try:
            command = "CREATE TABLE service (serviceName text, dbname text, file text )"
            self.cursorObj.execute(command)
            self.conn.commit()
        except Error:
            print("The table has already created")
            pass

    def sql_deleteTable(self, table="service"):
        command = f"DROP TABLE IF EXISTS {table}"
        self.cursorObj.execute(command)
        self.conn.commit()

    def sql_insert(self, serviceName = None, DBName = None, file=None):
            command = f"""INSERT INTO service( serviceName, dbname, file) VALUES ('{serviceName}' \
                      , '{DBName}', '{file}')"""
            self.cursorObj.execute(command)
            self.conn.commit()

    def sql_truncateTable(self, table=None):
        command = f"TRUNCATE TABLE {table}"
        self.cursorObj.execute(command)
        self.conn.commit()

    def sql_allQuery(self):
        command = "SELECT * FROM service "
        alls = self.cursorObj.execute(command)
        return alls.fetchall()
    def sql_allServiceNameQuery(self):
        command = f"SELECT DISTINCT serviceName FROM service "
        rows = self.cursorObj.execute(command)
        return rows.fetchall()
    def sql_DBNameQuery(self, dbname):
        command = f"SELECT serviceName FROM service WHERE DBName = '{dbname}'"
        rows = self.cursorObj.execute(command)
        return rows.fetchall()
    def sql_DBNameAndFileQuery(self, serviceName):
        command = f"""SELECT DBName, file FROM service WHERE serviceName='{serviceName}'"""
        rows = self.cursorObj.execute(command)
        return rows.fetchall()
    def sql_serviceNameDelete(self, serviceName ):
        command = f"DELETE FROM service WHERE serviceName = '{serviceName}'"
        self.cursorObj.execute(command)
        self.conn.commit()
    def sql_dbNameDelete(self, DBName = None):
        command = f"DELETE FROM service WHERE DBName = '{DBName}'"
        self.cursorObj.execute(command)
        self.conn.commit()
    def sql_update(self, DBName=None):
        command = f"UPDATE service SET DBName = '{DBName}'"
        self.cursorObj.execute(command)
        self.conn.commit()
    def sql_closeConn(self):
        self.conn.commit()
        self.conn.close()
        print("connection was closed")