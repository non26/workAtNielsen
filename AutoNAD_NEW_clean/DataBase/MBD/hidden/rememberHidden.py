import pandas as pd
import sqlite3
from sqlite3 import Error
import numpy as np
import os
class ConnDataBaseHiddenMBD():
    def __init__(self, dataBaseName="rememberHiddenMBD"):
        self.allRow = None
        try:
            self.conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "\\" + f"{dataBaseName}.db")
            self.cursorObj = self.conn.cursor()
            print("connecting to the DataBase...")
        except Error as e:
            print(e)

    def sql_createTable(self, catCode):
        try:
            print("creating the table")
            creation = f"""CREATE TABLE {catCode}_hiddenMBD (hiddenMBD text)"""
            self.cursorObj.execute(creation)
            self.conn.commit()
        except Error:
            print("The table has already created")
            pass

    def sql_insertion(self, catCode, hiddenMBD=""):
        """

        :param iteration: it's the container of a pair of tuple MBDName, MBDCode
        :return:
        """
        try:
            insertion = f"""INSERT INTO {catCode}_hiddenMBD (hiddenMBD, hiddenFact) VALUES ('{hiddenMBD}')"""
        except Error:
            pass
        else:
            self.cursorObj.execute(insertion)
            self.conn.commit()

    def sql_queryingAllData(self, catCode):
        query = f"SELECT  * FROM {catCode}_hiddenMBD"
        rows = self.cursorObj.execute(query)
        self.allRow = rows.fetchall()
        for elem in self.allRow:
            yield elem
    def sql_update(self, catCode, hiddenMBD=""):
            if hiddenMBD:
                update = f"""UPDATE {catCode}_hiddenMBD SET hiddenMBD='{hiddenMBD}' """
                self.cursorObj.execute(update)
                self.conn.commit()
class ConnDataBaseHiddenFact():
    def __init__(self, dataBaseName="rememberHiddenFact"):
        self.allRow = None
        try:
            self.conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "\\" + f"{dataBaseName}.db")
            self.cursorObj = self.conn.cursor()
            print("connecting to the DataBase...")
        except Error as e:
            print(e)

    def sql_createTable(self, catCode):
        try:
            print("creating the table")
            creation = f"""CREATE TABLE {catCode}_hiddenFact (hiddenFact text)"""
            self.cursorObj.execute(creation)
            self.conn.commit()
        except Error:
            print("The table has already created")
            pass

    def sql_insertion(self, catCode, hiddenFact=""):
        """

        :param iteration: it's the container of a pair of tuple MBDName, MBDCode
        :return:
        """
        try:
            insertion = f"""INSERT INTO {catCode}_hiddenFact  (hiddenFact) VALUES ('{hiddenFact}')"""
        except Error:
            pass
        else:
            self.cursorObj.execute(insertion)
            self.conn.commit()

    def sql_queryingAllData(self, catCode):
        query = f"SELECT  * FROM {catCode}_hiddenFact "
        rows = self.cursorObj.execute(query)
        self.allRow = rows.fetchall()
        for elem in self.allRow:
            yield elem

    def sql_queryingHiddenMBD(self, catCode):
        query = f"SELECT hiddenMBD FROM {catCode}_hiddenFact "
        rows = self.cursorObj.execute(query)
        self.allRow = rows.fetchall()
        for elem in self.allRow:  # list of MBDName
            yield elem

    def sql_queryingHiddenFact(self, catCode):
        query = f"SELECT hiddenFact FROM {catCode}_hiddenFact "
        rows = self.cursorObj.execute(query)
        self.allRow = rows.fetchall()
        for elem in self.allRow:  # list of MBDName
            yield elem

    def sql_update(self, catCode, hiddenFact=""):
            if hiddenFact:
                update = f"""UPDATE {catCode}_hiddenFact  SET hiddenFact='{hiddenFact}' """
                self.cursorObj.execute(update)
                self.conn.commit()

class rememberHidden():
    def __init__(self, hiddenMBD: list, hiddenFact: list, fileNAD):
        self.hiddenMBD = hiddenMBD
        self.hiddenFact = hiddenFact
        self.fileName = fileNAD
        self.modify()
    def modify(self):
        lengthMBD = len(self.hiddenMBD)
        lengthFact = len(self.hiddenFact)
        if lengthFact > lengthMBD:
            lengthDiff = lengthFact-lengthMBD
            for _ in range(lengthDiff):
                self.hiddenMBD.append("")
        else:
            lengthDiff = lengthMBD-lengthFact
            for _ in range(lengthDiff):
                self.hiddenFact.append("")
