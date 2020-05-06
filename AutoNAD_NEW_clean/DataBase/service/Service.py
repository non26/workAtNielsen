import pandas as pd
import os
import json
import sqlite3
from sqlite3 import Error
import numpy as np
# SQLite3 doesn't have json data type , need to load json extension for SQLite3
# The json_remove() function
class Service():
    """
    This class is used to extract only Service name uot of the CheckList of each other
    and write to the json file and store in the same directory of this file
    """
    def __init__(self, pathCheckList=None):
        self.pathCheckList = pathCheckList
        self.service = None
        self.thisFilePath = os.path.dirname(os.path.abspath(__file__))

    def finding_fromCheckList(self, column="Service", sheet="Generate Checklist"):
        """
        this method is used to extracted the service corresponding to the checkList's user
        :param column:
        :param sheet:
        :return:
        """
        sr_service = pd.Series(pd.read_excel(self.pathCheckList, sheet_name=sheet)[column]).unique()
        service = sr_service.tolist()
        return service # return list

    def writing_service(self, fileName="service.json", value=None, key="service"):
        """
        this class is writing the service'name to the json file in the same directory
        :param fileName:
        :param value: list of service'name
        :param key: "service"
        :return:
        """
        service_dict = {}
        with open(self.thisFilePath + "\\" + fileName, "w") as infile:
            service_dict[key] = value
            json.dump(service_dict, infile)

    def reading_service(self, fileName="service.json"):
        """
        reading the service's name from the json file in this directory
        :param fileName:
        :return:
        """
        with open(self.thisFilePath + "\\" + fileName, "r") as infile:
            service_dict = json.load(infile)
            return service_dict

    def matching_service(self, sheet="Generate Checklist"):
        df_service = pd.read_excel(self.pathCheckList, sheet_name=sheet)[["Service", "DB Name"]]
        return df_service

# class ConnDatabaseService():
#     """This class is used to math the Service name to the corresponding DBName(reportName)"""
#     def __init__(self, dbName="serviceMatchingDBName.db"):
#         self.thisFilePath = os.path.dirname(os.path.abspath(__file__))
#         self.dataBase = dbName
#         self.conn = None
#         self.cursorObj = None
#         self.connectDataBase()
#
#     def connectDataBase(self):
#         try:
#             self.conn = sqlite3.connect(self.thisFilePath + "\\" + self.dataBase)
#             self.cursorObj = self.conn.cursor()
#             print("connecting to the DataBase...")
#         except Error as e:
#             print(e)
#
#     def sql_createTable(self):
#         try:
#             creation = "CREATE TABLE service (serviceName text, DBName text )"
#             self.cursorObj.execute(creation)
#             self.conn.commit()
#         except Error:
#             print("The table has already created")
#             pass
#
#     def sql_insert(self, serviceName = None, DBName = None):
#             command = f"INSERT INTO service( DBName, serviceName ) VALUES ('{DBName}', '{serviceName}')"
#             self.cursorObj.execute(command)
#             self.conn.commit()
#
#     def sql_truncate(self, table=None):
#         command = f"TRUNCATE TABLE {table}"
#         self.cursorObj.execute(command)
#         self.conn.commit()
#
#     def sql_allQuery(self):
#         command = "SELECT * FROM service "
#         alls = self.cursorObj.execute(command)
#         return alls.fetchall()
#     def sql_allServiceNameQuery(self):
#         command = f"SELECT DISTINCT serviceName FROM service "
#         rows = self.cursorObj.execute(command)
#         return rows.fetchall()
#     def sql_DBNameQuery(self, serviceName):
#         command = f"SELECT DBName FROM service WHERE serviceName = '{serviceName}'"
#         rows = self.cursorObj.execute(command)
#         return rows.fetchall()
#
#     def sql_serviceNameDelete(self, serviceName = None):
#         command = f"DELETE FROM service WHERE serviceName = '{serviceName}'"
#         self.cursorObj.execute(command)
#         self.conn.commit()
#     def sql_dbNameDelete(self, DBName = None):
#         command = f"DELETE FROM service WHERE DBName = '{DBName}'"
#         self.cursorObj.execute(command)
#         self.conn.commit()
#
#     def sql_update(self, DBName=None):
#         command = f"UPDATE service SET DbName = '{DBName}'"
#         self.cursorObj.execute(command)
#         self.conn.commit()

# if __name__=="__main__":
#     test1 = Service(pathCheckList=r"C:\Users\EiCh9001\PycharmProjects\PyNielsen\AutomateNAD\Koi.xlsm")
#     # value = test1.finding_fromCheckList()
#     # test1.writing_service(value=value)
#     print(test1.matching_service())
#     # ############################################
#     test2 = connDatabaseService()
#     test2.sql_createTable()
#     x=test1.matching_service()
#     for index in range(len(x)):
#         if str(x.iloc[index, 0]) != 'nan':
#             test2.sql_insert(serviceName=str(x.iloc[index, 0]), DBName=str(x.iloc[index, 1]))
#     print(test2.sql_allQuery())

