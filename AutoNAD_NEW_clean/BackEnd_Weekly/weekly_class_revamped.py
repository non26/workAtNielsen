import numpy as np
import pandas as pd
import re
from ..handlingException import PrintDialogError
from .. import popUp_taskWithoutRootWD as popUp_task
from ..INAD import INAD # class
import json
import time
# from ..BackEnd_Weekly import write2Excel_weekly as ww
from . import week_excel
from ..DataBase.configurations import * # import path
from ..DataBase.service import connDatabaseService as cdbs
"""
pathRootNAD
--|-chainFOLDER
-----|-NADFile
"""

def findWeek(fileTrendPath):
    """
    find the week from the file name of TrendCheck file
    :param fileTrend:
    :return:
    """
    fileTrend = os.path.basename(fileTrendPath)
    compileObj = re.compile(r"(\d\d)-(\d\d)('|_)(\d\d)")
    search1 = compileObj.search(fileTrend)
    weeks = search1.groups()  # tuple of 3 items: first week, last week, and year
    latest_period = f"{weeks[0]}-{weeks[1]}-20{weeks[-1]}"
    return latest_period

def formatWeek(w):
    weekth = w[:] # w = 01-04-2020
    weekth = weekth.split("-")
    y = weekth[-1][2:]  # takes last 2 digit of the year
    weekth = weekth[:-1]  # takes first 2 index, that is week
    format = []
    for i in range(int(weekth[0]), int(weekth[1])+1):
        if len(str(i)) == 1:
            format.append("W"+"0"+str(i)+y)
        elif len(str(i)) == 2:
            format.append("W" + str(i) + y)
    return format

class Weekly(INAD):
    checkingFact = ("Sales Value (Baht)", "ND Selling", "WD Selling")
    dbNameError = "not found DBName"
    def __init__(self, selectedService, conclude, weekth=None):
        self.conclude = conclude
        self.skipRow = 1
        self.pathRootNAD, self.pathFileTrend = self._readConfiguration()
        if weekth != findWeek(self.pathFileTrend):
            PrintDialogError().show_error(message="week-th doesn't match the Trend Check File.", title="Week Error")
        self.weekly = formatWeek(weekth)
        self.service = selectedService

    @staticmethod
    def _skipRowNotNull(pathNadFile, checkColumn=1, startRow=0, sheetName="WSP_Sheet1"):
        nadContent = pd.read_excel(pathNadFile
                                   , sheet_name=sheetName
                                   , skiprows=[i for i in range(startRow)]
                                   , header=None)
        startRow = 0
        for row in range(len(nadContent)):
            null = nadContent.iloc[:, checkColumn].at[row]
            if str(null) != "nan":
                startRow += 1
            else:
                break
        return startRow

    @staticmethod
    def _skipRowNull(pathNadFile, checkColumn=1, startRow=0, sheetName="WSP_Sheet1"):
        nadContent = pd.read_excel(pathNadFile
                                   , sheet_name=sheetName
                                   , skiprows=[i for i in range(startRow)]
                                   , header=None)
        startRow = 0
        for row in range(len(nadContent)):
            null = nadContent.iloc[:, checkColumn].at[row]
            if str(null) == "nan":
                startRow += 1
            else:
                break
        return startRow
    @staticmethod
    def _rowToWantedTable(pathFileNAD):
        rowth = 0
        skipRow = Weekly._skipRowNull(pathFileNAD, 2, )
        rowth += skipRow
        skipRow = Weekly._skipRowNotNull(pathFileNAD, 2, skipRow)
        rowth += skipRow
        skipRow = Weekly._skipRowNull(pathFileNAD, 2, rowth)
        rowth += skipRow
        return rowth

    # @override
    def _readConfiguration(self, path = pathConfigurations):
        # pathConfigurations comes from ..DataBase.configurations import *
        with open(path + "\\" + "configFile.json") as file:
            config = json.load(file)
        return config["rootNADWeekly"], config["trendCheck"]

    # @override
    def _readNADFile(self, pathFileNAD=None, sheetName="WSP_Sheet1"):
        """
         This function reads the NAD file and extracts needed columns
        #- The new form name is CATCode.xlsx, this will help us to match the CATCODE
        # in the TrendCheck at the specific Weekly-having-chain-column sheet easily.
        #- This df1_rest will contain
        column 0: MBD,
        column 1: period,
        column 4: SALEVALUE,
        column 5: ND selling,
        column 6: WD selling
        #- df1 will contain 5 columns: MBD, period, SALEVALUE, ND selling, WD selling
        :param pathFileNAD:
        :param largest_MBD:
        :return: df1 = dataFrame of the largest MBD in NAD Weekly
        """
        # self.skipRow = 1
        # self.skipRow = self._skipRowNull(pathFileNAD, 2, self.skipRow) + 1 # +1 is meant for header
        # self.skipRow = self._skipRowNotNull(pathFileNAD, 2, self.skipRow)
        # self.skipRow = self._skipRowNull(pathFileNAD, 2, self.skipRow) + 1 # +1 is meant for header
        self.skipRow = Weekly._rowToWantedTable(pathFileNAD)
        df1 = pd.DataFrame(pd.read_excel(pathFileNAD, skiprows=[i for i in range(self.skipRow)], sheet_name=sheetName))
        df1.rename(columns={df1.columns[0]: "MBD", df1.columns[1]: "period"}, inplace=True)
        df1.iloc[0:15, 0] = df1.iloc[:, 0].fillna(method="ffill")  # fill na for every rows at first column
        df1["number"] = np.arange(0, len(df1))  # insert column after the last column
        largest_MBD = df1.iloc[0, 0]  # this indicates that it is the largest MBD
        new_row = {col: index for index, col in enumerate(df1.columns)}
        df1 = df1.groupby(by="MBD")
        df1 = df1.get_group(largest_MBD)  # group by largest MBD that is first row of MBD
        df1 = df1.groupby(by="period")

        week = {}
        factInWeek = {}
        need2Check = {largest_MBD: week, "column": {}, "row": {}}
        # need2Check = {"largest MBD": {W020543: {"SALESVALUE":123,456,789,"ND Selling":100, "WD Selling":100}, ...}
        # , column:{"SALESVALUE":1, "ND Selling":2, "WD Selling":3}
        # , row:{"W0143":1, "W0144":2}}
        # }
        for w in self.weekly:
            fact2check = df1.get_group(w)
            fact2check = fact2check.append(new_row, ignore_index=True)  # add last row
            weekth = fact2check.at[0, "number"]
            need2Check["row"][w] = int(weekth) + self.skipRow + 2
            # for the row of wanted table, +2 because it starts at first under header.
            for fact in Weekly.checkingFact:
                value = fact2check.at[0, fact]
                columnth = fact2check.at[1, fact]
                if len(need2Check["column"]) != 3:
                    need2Check["column"][fact] = int(columnth)
                factInWeek[fact] = value
            need2Check[largest_MBD][w] = factInWeek.copy()
        return need2Check, largest_MBD

    def _readTrendFile(self, sheetName=None):
        """
        This function reads the Trendcheck excel file
        :param sheet:
        :return:
        """
        # this sheet_name option will correspond to the folder it reside
        df1 = pd.DataFrame(pd.read_excel(self.pathFileTrend, sheet_name=sheetName))  #####
        return df1

    def _valueFromFileTrend(self, sheet, dbName):  #### input the TrendCheck file name
        """This function groups the corresponding category to the NAD file from the TrendCheck file"""
        sv = {dbName: {}} # {dvName:{"W4319":SALES VALUE}}
        df_trend = self._readTrendFile(sheetName=sheet).groupby("REPORTNAME")
        df_trend = df_trend.get_group(dbName) # when dbName isn't found, handle it at where it's called.
        for indx, week in enumerate(self.weekly):
            indxs = df_trend.index[indx]
            sv[dbName][week] = df_trend.at[indxs, "SALESVALUE"]
        return sv

    def mainCompare(self):
        """
        this function does the compare processs from the data from NAD and TrendCheck excel file
        1. rootNAD is where the directory root of created-from-NAD files reside,that is weekly or monthly folder
        2. fileTrend is the path of the file where trend check file located or trend check file name
        """
        # loop all sub-folder in the folder-chain in this  function
        # error is the dictionary for keeping the unmatched 'DBName' from the trendcheck.
        dbNameNotFoundError = {} # key is DBName, value is the message of error
        start_time = time.time()
        counter_fail = 0
        counter_total = 0
        fileLog = self.pathRootNAD + "\\" + "_week_LogFailer.xlsx"
        # toLog = ww.ToLog(pathLogFile=fileLog, sheets=["Sheet1", "notFoundDBName"])
        toLog = week_excel.Week_ToLog(pathLogFile=fileLog, sheets=["Sheet1", "notFoundDBName"])
        # toLog.modifyWorkSheet()
        week = self.weekly
        conn = cdbs.ConnDatabaseService()
        dbnameAndFile = conn.sql_DBNameAndFileQuery(self.service)
        previousFile = None
        for dbname, file in dbnameAndFile:
            counter_total += 1
            pathNADFile = self.pathRootNAD+"\\"+file
            print(pathNADFile)
            chain = file[:file.index("\\")] # service
            # mark = ww.MarkOriginal(pathNADFile=pathNADFile)
            mark = week_excel.Week_MarkOriginal(pathNADFile=pathNADFile, sheetName="WSP_Sheet1")

            dict_get_large_MBD, largeMBD = self._readNADFile(pathNADFile) # df_get_large_MBD is dictionary
            try:
                svFromTrendCheck = self._valueFromFileTrend(sheet=chain, dbName=dbname)
            except KeyError:
                # in case of dbname did't put into the trend file
                # in case of can't specify wanted sheet in the CheckTrend file
                # in case of there is no "REPORTNAME" column header
                counter_fail += 1
                dbNameNotFoundError[dbname] = Weekly.dbNameError
                continue
            for index, item in enumerate(week): # item is weekth
                row_weekth = dict_get_large_MBD["row"][item]
                # check sale value
                column_sv = None
                fromNAD = self._roundDigitToWhole(dict_get_large_MBD[largeMBD][item][Weekly.checkingFact[0]])
                fromTrendCheck = self._roundDigitToWhole(svFromTrendCheck[dbname][item])
                svValue_fromNAD = fromNAD
                svValue_fromTrendCheck = fromTrendCheck
                result_sv, status_sv = self._check_SALEVALUE(sv_trend=svValue_fromTrendCheck, sv_nad=svValue_fromNAD)
                # check nd selling
                column_nd = None
                ndValue = dict_get_large_MBD[largeMBD][item][Weekly.checkingFact[1]]
                result_nd, status_nd = self._check_ND(nd=ndValue)
                # check wd selling
                column_wd = None
                wdValue = dict_get_large_MBD[largeMBD][item][Weekly.checkingFact[2]]
                result_wd, status_wd = self._check_WD(wd=wdValue)
                # check each result
                if not (result_sv and result_wd and result_nd):
                    # print(item, file, result_sv, result_nd, result_wd)
                    toLog.writeLogSVNDWD(chain=chain, pathNADFile=pathNADFile, period=item, largest_MBD=largeMBD
                                         , logSV=result_sv, logND=result_nd, logWD=result_wd,
                                         valueSV=status_sv, valueND=status_nd, valueWD=status_wd
                                         , dbname=dbname)
                    if not result_sv:
                        column_sv = dict_get_large_MBD["column"][Weekly.checkingFact[0]]
                    if not result_nd:
                        column_nd = dict_get_large_MBD["column"][Weekly.checkingFact[1]]
                    if not result_wd:
                        column_wd = dict_get_large_MBD["column"][Weekly.checkingFact[2]]
                    mark.markSVNDWD(skipRow=row_weekth, col_sv=column_sv, col_nd=column_nd
                                    , col_wd=column_wd, markSV=result_sv, markND=result_nd, markWD=result_wd)
                    if previousFile != file and not (result_sv and result_wd and result_nd):
                        counter_fail += 1
                        previousFile = file
                    else: pass
            mark.saveAction()
            mark.closeWorkBook()
        if bool(dbNameNotFoundError): # if there is the unmatched DBName
            toLog.write_logNotFoundDBName(dict_notFoundDBName=dbNameNotFoundError, orderOfSheet=1)
        toLog.saveAction()
        toLog.closeWorkBook()
        end_time = time.time()
        self.conclude.totalTime = "{elapsed} s.".format(elapsed=end_time-start_time)
        self.conclude.totalFiles = counter_total
        self.conclude.totalFail = counter_fail
        popUp_task.alert_popUp("Weekly NAD", f"Weekly NAD files are finished.", service=self.service)
