import tkinter as tk
import datetime
import os
import json
from ..DataBase.configurations import *
from ..handlingException import PrintDialogError
"""
This module is used to show conclusion information at the section of weekly
when all files are executed which include date, Total Time, Total Files, Total Fail
"""
master = None
class conclude():
    """This is wherer conclusion information are shown"""
    def __init__(self, master):
        self.master = master
        self.total_time = None
        self.total_fail = None
        self.total_files = None
        self.date = None
        # date section
        self.date_label = tk.Label(self.master, text="DATE: ")
        self.date_label.grid(row=8, column=0, columnspan=2)
        self.dateInfo_label = tk.Label(self.master)
        self.dateInfo_label.grid(row=8, column=2, columnspan=4)

        # Total time section
        self.ttTime_label = tk.Label(self.master, text="Total Time: ")
        self.ttTime_label.grid(row=9, column=0, columnspan=2)
        self.ttTimeInfo_label = tk.Label(self.master)
        self.ttTimeInfo_label.grid(row=9, column=2, columnspan=4)

        # Total files section
        self.ttFile_label = tk.Label(self.master, text="Total Files: ")
        self.ttFile_label.grid(row=10, column=0, columnspan=2)
        self.ttFileInfo_label = tk.Label(self.master)
        self.ttFileInfo_label.grid(row=10, column=0, columnspan=4)

        # Total Fails section
        self.ttFail_label = tk.Label(self.master, text="Total Fails: ", fg='red')
        self.ttFail_label.grid(row=11, column=0, columnspan=2)
        self.ttFailInfo_label = tk.Label(self.master)
        self.ttFailInfo_label.grid(row=11, column=0, columnspan=4)

    @property
    def runningDate(self):
        return self.date
    @runningDate.setter
    def runningDate(self, t):
        self.date = t
        self.dateInfo_label["text"] = self.date
    @runningDate.deleter
    def runningDate(self):
        self.date = None
        self.dateInfo_label["text"] = self.date

    @property
    def totalTime(self):
        return self.total_time
    @totalTime.setter
    def totalTime(self, ttTime):
        self.total_time = ttTime
        self.ttTimeInfo_label["text"] = self.total_time
    @totalTime.deleter
    def totalTime(self):
        self.total_time = None
        self.ttTimeInfo_label["text"] = self.total_time

    @property
    def totalFiles(self):
        return self.total_files
    @totalFiles.setter
    def totalFiles(self, ttFiles):
        self.total_files = ttFiles
        self.ttFileInfo_label["text"] = self.total_files
    @totalFiles.deleter
    def totalFiles(self):
        self.total_files = None
        self.ttFileInfo_label["text"] = self.total_files

    @property
    def totalFail(self):
        return self.total_fail
    @totalFail.setter
    def totalFail(self, ttFail):
        self.total_fail = ttFail
        self.ttFailInfo_label["text"] = self.total_fail
    @totalFail.deleter
    def totalFail(self):
        self.total_fail = None
        self.ttFailInfo_label["text"] = self.total_fail

class openLogButton():
    """
    this method is used to link to log files when all files are executed
    so the user can easily open the log file
    """
    def __init__(self, master):
        self.master = master
        self.log_button = tk.Button(self.master, text="Open File Log", command=self.openFileWithItsDefault)
        self.log_button.grid(row=12, column=1, columnspan=4, sticky="WE")
    def openFileWithItsDefault(self):
        rootNADLog = self.findPath() +"\\"+ "_week_LogFailer.xlsx" #
        try:
            os.startfile(rootNADLog)
        except Exception as e:
            PrintDialogError().show_error(message=e)

    def findPath(self):
        """
        This method is used to find the path of log file
        """
        path = pathConfigurations
        with open(path + "\\" + "configFile.json") as file:
            configs = json.load(file)
            rootNADFile = configs["rootNADWeekly"]
            return rootNADFile

