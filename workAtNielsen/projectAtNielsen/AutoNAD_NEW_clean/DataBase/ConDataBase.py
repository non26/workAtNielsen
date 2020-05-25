import os
import sqlite3
from sqlite3 import Error
class ConDataBase:
    def __init__(self, dbName="serviceMatchingDBName.db", table=service):
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

    def sql_createTable(self, table="service"): pass