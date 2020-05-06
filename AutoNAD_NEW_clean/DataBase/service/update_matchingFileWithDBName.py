import pandas as pd
import re
import json
from ..configurations import *
from ..service import *
from . import connDatabaseService as cdbs

class MatchingFile():
    column = ("Service", "DB Name")
    def __init__(self):
        self.pathServiceName = pathService # comes from __init__ method of service
        self.pathSetting = pathConfigurations # comes from __init__ method od service
        self.conn = cdbs.ConnDatabaseService()
        self.conn.sql_deleteTable()
        self.conn.sql_createTable()

    def getServiceName(self):
        """
        this method gets the service's name from the service database
        :return:
        """
        with open(self.pathServiceName+"\\"+"service.json") as file:
            serviceName = json.load(file)
        return serviceName["service"] # including Weekly and Monthly

    def getSetting(self):
        """
        thid method gets the path from the setting configuration at config database
        :return:
        """
        with open(self.pathSetting+"\\"+"configFile.json") as file:
            pathConfig = json.load(file)
        return pathConfig

    def matchDBName(self, pathCheckList):
        """
        this method gets the DBName with the corresponding service
        :param pathCheckList:
        :return:
        """
        df_checkList = pd.read_excel(pathCheckList, sheet_name="Generate Checklist")[["Service", "DB Name"]]
        dfg_checkList = df_checkList.groupby(by="Service")
        return dfg_checkList

    @staticmethod
    def reorder(item):
        """
        this method is to order the iterator that's passed in
        :param item:
        :return:
        """
        compileDBName = re.compile(r"-(.*)\.")
        searchDBName = compileDBName.search(item)
        return searchDBName.group(1)

    @staticmethod
    def binarrySearch(word, target1):
        """
        this method search for the DB Name that match the monthly/weekly NAD file
        :param word: is the DBName
        :param target: is the list of monthly/weekly NAD files
        :return:
        """
        target=target1.tolist()
        target.sort()
        # logging.debug(f"len:{len(target)}")
        while len(target) != 0:
            guess_index = int(len(target)/2)
            guess = target[guess_index]
            # logging.debug(f"guess: {guess}")
            if word.upper() == guess.upper():
                return True
            elif word < guess: #word is the DBName, compare_guess is the file name
                target = target[:guess_index]
            elif word > guess:
                target = target[guess_index+1:]
        return False

    def getCorrespondingFile(self, serviceName, pathConfig, df_DBName):
        """
        :param serviceName: list service name
        :param pathConfig:
        :param df_DBName: it's the DataFrame consisting of 2 columns Service and DBName
        :return:
        """
        rootNADMonthly = pathConfig["rootNADMonthly"]
        rootNADWeekly = pathConfig["rootNADWeekly"]
        if rootNADMonthly:
            # this is the list of the monthly NAD files' name
            filesMonthly = [name for name in os.listdir(rootNADMonthly)
                            if os.path.isfile(rootNADMonthly+"\\"+name) and not name.startswith("_month")]
            filesMonthly.sort(key=self.reorder) # reorder by the DB Name
        else:
            filesMonthly = []
        if rootNADWeekly:
            filesWeekly = [folder+"\\"+file for folder in os.listdir(rootNADWeekly)
                           if os.path.isdir(rootNADWeekly+"\\"+folder)
                           for file in os.listdir(rootNADWeekly+"\\"+folder)] # this is the list of the weekly NAD files' name
            filesWeekly.sort(key=self.reorder) # reorder by the DB Name
        else:
            filesWeekly = []
        for service in serviceName: # loop through the services
            if str(service) != "nan" :
                df_service_DBName = df_DBName.get_group(service)["DB Name"]
                if service.lower().find("monthly") != -1:
                    if filesMonthly:
                        for index, dbname in enumerate(map(self.reorder, filesMonthly)):
                            having = self.binarrySearch(dbname, df_service_DBName)
                            if having:
                                self.conn.sql_insert(serviceName=service, DBName=dbname, file=filesMonthly[index])
                elif filesWeekly:
                    for index, dbname in enumerate(map(self.reorder, filesWeekly)):
                        having = self.binarrySearch(dbname, df_service_DBName)
                        if having:
                            self.conn.sql_insert(serviceName=service
                                                 , DBName=dbname, file=filesWeekly[index])
















