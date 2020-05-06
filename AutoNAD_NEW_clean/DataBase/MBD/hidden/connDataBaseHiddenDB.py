import pandas as pd
import os
import sqlite3
from sqlite3 import Error
# column: Hide MBD
# column: Show Hide
# df = pd.read_excel(r"C:\Users\EiCh9001\Desktop\List Hide_Show MBD in Monthly.xlsx").fillna("-")
# print(df)

class ConnDataBaseHiddenDB():
        def __init__(self, dataBaseName="hiddenMBD", table="hiddenMBD"):
            self.allRow = None

            self.table = table
            self.thisFilePath = os.path.dirname(os.path.abspath(__file__))
            self.dataBase = dataBaseName
            self.conn = None
            self.cursorObj = None
            self.connectDataBase()

        def connectDataBase(self):
            try:
                self.conn = sqlite3.connect(self.thisFilePath + "\\" + self.dataBase + ".db")
                self.cursorObj = self.conn.cursor()
                print("connecting to the DataBase...")
            except Error as e:
                print(e)

        def sql_createTable(self):
            try:
                print("creating the table")
                creation = "CREATE TABLE hiddenMBD (MBDCode text, DESCRIPTION text" \
                           ", 'Hide MBD' text, 'Show Hide' text)"
                self.cursorObj.execute(creation)
                self.conn.commit()
            except Error:
                print("The table has already created")
                pass

        def sql_insert(self, iteration):
            """

            :param iteration: it's the container of a pair of tuple MBDName, MBDCode
            :return:
            """
            for mbd in iteration:
                try:
                    insertion = f"""INSERT INTO hiddenMBD (MBDCode, DESCRIPTION, 'Hide MBD', 'Show Hide') VALUES ('{mbd[0]}', '{mbd[1]}' \
                                , '{mbd[2]}', '{mbd[3]}')"""
                except Error:
                    pass
                else:
                    self.cursorObj.execute(insertion)
                    self.conn.commit()

        def sql_excel2DataBase(self, pathExcel=None):
            """

            :param pathExcel: consisting of 2 columns MBDName and MBDCode
            :return:
            """
            df_mbd = pd.read_excel(pathExcel)
            for row in range(len(df_mbd)):
                if str(df_mbd.iloc[row, 0]) != 'nan':
                    hideMBD = "Y" if str(df_mbd.iloc[row, 2]) != 'nan' else "N"
                    showHide = "Y" if str(df_mbd.iloc[row, 3]) != 'nan' else "N"
                    pair = [(df_mbd.iloc[row, 0], df_mbd.iloc[row, 1], hideMBD, showHide)]
                    self.sql_insert(pair)

        def sql_queryingAllData(self):
            query = "SELECT * FROM hiddenMBD"
            rows = self.cursorObj.execute(query)
            self.allRow = rows.fetchall()
            return self.allRow
        def sql_queryingAllMBDCode(self):
            query = "SELECT MBDCode, DESCRIPTION FROM hiddenMBD"
            rows = self.cursorObj.execute(query)
            self.allRow = rows.fetchall()
            return self.allRow
        def sql_querySomeMBDCode(self, mbd):
            query = f"SELECT MBDCode FROM hiddenMBD WHERE DESCRIPTION = '{mbd}' "
            rows = self.cursorObj.execute(query)
            self.allRow = rows.fetchall()
            return self.allRow
        def sql_queryHiddenOrNot(self, mbdCode):
            query = f"SELECT `Hide MBD` FROM hiddenMBD WHERE MBDCode = '{mbdCode}'"
            rows = self.cursorObj.execute(query)
            self.allRow = rows.fetchall()
            return self.allRow
        def sql_closeConn(self):
            self.conn.commit()
            self.conn.close()

