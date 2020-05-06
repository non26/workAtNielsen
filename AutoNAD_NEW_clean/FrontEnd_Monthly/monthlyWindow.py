import tkinter as tk
import json
import datetime
# from PyNielsen.AutoNAD import menu_setting as ms
# from .. import menu_setting as ms # must be solved
from .. import searchingword as sw, menu_showDetail_showMBD as menu_showMBD
from ..DataBase.configurations import *
# old version
# from ..BackEnd_Monthly import monthly_class as mc
# new version
from ..BackEnd_Monthly import monthly_class_revamped as mc
# from ..progressBar import ProgressBar
import os
from ..FrontEnd_Monthly import conclusionSection_Monthly as ccm


class MonthWindow():
    def __init__(self, master):
        self.master = master
        # create variable
        self.nadVar = tk.StringVar()
        self.trendVar = tk.StringVar()
        self.checkListVar = tk.StringVar()
        self.serviceVar = tk.StringVar()
        # # Label
        self.rootFolder = tk.Label(self.master, text="Root NAD Monthly Folder: ").grid(row=0, column=0, padx=(10, 5), sticky='w')
        self.trendFile = tk.Label(self.master, text="Trend Check File: ").grid(row=1, column=0, padx=(10, 5), sticky='w')
        self.checkList = tk.Label(self.master, text="Check List File: ").grid(row=2, column=0, padx=(10, 5), sticky='w')
        self.chooseService = tk.Label(self.master, text="Choose Service: ").grid(row=3, column=0, padx=(10, 5), sticky='w')
        # # Entry
        # Entry---nad
        self.nad = tk.Entry(self.master, textvariable=self.nadVar, width=40, state="readonly")
        self.nad.grid(row=0, column=1, columnspan=5)
        # Entry---trend
        self.trend = tk.Entry(self.master, textvariable=self.trendVar, width=40, state="readonly")
        self.trend.grid(row=1, column=1, columnspan=5)
        # Entry---checkList
        self.checkList = tk.Entry(self.master, textvariable=self.checkListVar, width=40, state="readonly")
        self.checkList.grid(row=2, column=1, columnspan=5)
        # Entry---service searching
        self.service = tk.Entry(self.master, textvariable=self.serviceVar, width=40)
        self.service.grid(row=3, column=1, columnspan=5)
        sw.ServiceAutoCompleteEntry(master=self.service, mastervariable=self.serviceVar
                                    , parentMaster=self.master, row=4, column=1)
        # # button Run
        self.run_button = tk.Button(self.master, text="RUN", command=self.running)
        self.run_button.grid(row=4, column=1, columnspan=5, sticky="EW")
        self.setMonthlyDetail()

        self.conclude = ccm.conclude(self.master)
        ccm.openLogButton(self.master)

    def running(self):
        del self.conclude.runningDate
        del self.conclude.totalFail
        del self.conclude.totalFiles
        del self.conclude.totalTime
        self.conclude.runningDate = datetime.datetime.now().strftime("%c")
        month = mc.Monthly(selectedService=self.serviceVar.get(), conclude=self.conclude)
        month.mainCompare()
    def setMonthlyDetail(self):
        path = pathConfigurations
        with open(path + "\\" + "configFile.json") as infile:
            content = json.load(infile)
            self.nadVar.set(os.path.basename(content["rootNADMonthly"]))
            self.trendVar.set(os.path.basename(content["trendCheck"]))
            self.checkListVar.set(os.path.basename(content["checkList"]))

class Menu_ShowDetail_ShowMBD(menu_showMBD.ShowMBDCode):
    def __init__(self, master):
        menu_showMBD.ShowMBDCode.__init__(self, master)



