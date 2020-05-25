import pandas as pd
import re
import json
import numpy as np
import time
# from . import write2Excel_monthly as wm
from . import month_excel
from .. import popUp_taskWithoutRootWD as popUp_task
from ..DataBase.configurations import *
from ..DataBase.MBD.hidden import connDataBaseHiddenDB as cdbh
from ..DataBase.service import connDatabaseService as cdbs
from ..INAD import INAD
# # every path needs to be in the form of relative root
"""
-This is to compare the NAD file monthly and TrendCheck monthly at the corresponding to its 
largest MBDCode and check that some hidden categories are invisible
-Notice largest MBDCode by the first row of the information
"""
SALEVALUE = "SALESVALUE"
ND_SELLING = "ND Selling"
WD_SELLING = "WD Selling"
SALEVALUE_NADFILE =  "Sales Value (Tsd.Baht)"
SALEVALUE_TRENDFILE = "SALESVALUE_PROJETED_TSD"
CHECKFACT_NAD = [SALEVALUE_NADFILE, ND_SELLING, WD_SELLING]

class Monthly(INAD):
    dbNameError = "not found DBName"
    def __init__(self, selectedService=None, conclude=None):
        self.service = selectedService
        self.pathRootNAD, self.pathFileTrend = self._readConfiguration()
        self.conclude = conclude
        # this is primarily hidden fact which doesn't include facts with tags
        # self.hiddenFact = ["ND In-Stock", "WD In-Stock", "ND Out-Stock", "WD Out-Stock"]
        self.hiddenFact = []
        self.hiddenMBD = []
        self.skipRow = 0

    def _readConfiguration(self, path=pathConfigurations):
        # path = pathConfigurations # from ..DataBase.configurations import *
        with open(path + "\\" + "configFile.json") as file:
            conn = json.load(file)
        return conn["rootNADMonthly"], conn["trendCheck"]

    @staticmethod
    def _findFactWithStockWord(colName):
        """
        the rest of fact that need to be included is  "ND In-Stock" that
        somehow when it read from User Excel, it may show as "ND In - Stock".
        this method handle those appearance.
        :param colName:
        :return:
        """
        comObj = re.compile(r"((ND|WD)\s+(In|Out)\s*-\s*Stock\s*)")
        for col in colName:
            m = comObj.match(col)
            if m:
                result = m.groups()
                yield result[0]
            else:
                continue

    def _findHiddenFact(self, colName):
        """
        find hidden facts with tag
        :param colName:
        :return:
        """
        tags = []
        # hidden fact that needs to have tag
        baseFact = ["Purchase ", "Forward Stock ", "Reserved Stock "]
        for col in colName:
            compileObj = re.compile(r"Sales Volume\s*(\([A-Za-z0-1.\-]*\))")
            searchObj = compileObj.match(col)
            try:
                tag = searchObj.group(1)
            except Exception: continue
            else:
                tags.append(tag)
        for tag in tags:
            for fact in baseFact:
                # self.hiddenFact.append(fact+tag)
                yield fact+tag
    @staticmethod
    def _findMBDCode(mdbCode):
        comObj = re.compile(r"(M0{1,3})?([A-Za-z0-9]*)")
        matchObj = comObj.match(mdbCode)
        result = matchObj.groups()
        return result[-1]

    def _findHiddenMBD(self, mbd: list, mbdCode: list):
        list_mbd_mbdCode = dict(zip(mbd, map(Monthly._findMBDCode, mbdCode)))
        conn = cdbh.ConnDataBaseHiddenDB()
        for mbd_key in list_mbd_mbdCode:
            try:
                result = conn.sql_queryHiddenOrNot(list_mbd_mbdCode[mbd_key])[0][0]
            except Exception:
                continue
            else:
                if result == "Y":
                    yield mbd_key
                else:
                    continue
        conn.sql_closeConn()

    def _skipRowNull(self, fileNAD, sheetName="WSP_Sheet1"):
        df1 = pd.DataFrame(pd.read_excel(fileNAD, header=None, sheet_name=sheetName))
        skipRow = 0
        # start counting at column 0th
        for row in range(len(df1)):
            null = df1.iloc[:, 0].at[row]
            if str(null) == "nan" or str(null) == "":
                # self.skipRow += 1
                skipRow += 1
            else:
                break
        skipRow -= 1
        return skipRow

    def _readNADFile(self, fileNAD=None, sheetName="WSP_Sheet1"):
        self.skipRow = self._skipRowNull(fileNAD)
        if sheetName:
            df1 = pd.DataFrame(pd.read_excel(fileNAD, skiprows=[i for i in range(self.skipRow)], sheet_name=sheetName))
        else:
            df1 = pd.DataFrame(pd.read_excel(fileNAD, skiprows=[i for i in range(self.skipRow)]))
        # df1.rename(columns={df1.columns[0]:"MBD", df1.columns[1]:"MBDCode", df1.columns[2]:"period"}, inplace=True)
        df1.rename(columns={df1.columns[0]: "MBD", df1.columns[1]: "MBDCode"}, inplace=True)
        # find the rest of hidden fact
        for fact_stock in self._findFactWithStockWord(list(df1.columns)):
            self.hiddenFact.append(fact_stock)
        for fact in self._findHiddenFact(list(df1.columns)):
            self.hiddenFact.append(fact)
        # find the hidden MBD
        mbdcode = [x for x in df1["MBDCode"].to_list() if str(x) != "nan"]
        mbd = df1["MBD"].to_list()[:len(mbdcode)]
        for mbd in self._findHiddenMBD(mbd, mbdcode):
            self.hiddenMBD.append(mbd)

        df1["number"] = np.arange(0, len(df1))  # insert new column called "number" after last column
        largest_MBD = df1["MBD"].iloc[0]  # extract the largest MBD
        mbdCode = df1["MBDCode"].iloc[0]

        df1 = df1.groupby(by='MBD')
        df1 = df1.get_group(largest_MBD)
        new_row = {col: index for index, col in enumerate(df1.columns)}

        df1 = df1.append(new_row, ignore_index=True)  # insert new row after the last row
        needToBeChecked = {largest_MBD: {}, "column": {},
                           "row": df1.at[0, "number"]}  # {largest_MBD: {SALESVALUE:?, ND SELLING:?, WD SELLING:?}}
        for fact in CHECKFACT_NAD:
            needToBeChecked[largest_MBD][fact] = df1.at[0, fact]
            needToBeChecked["column"][fact] = int(df1.at[1, fact])
        return needToBeChecked, largest_MBD, mbdCode

    def _readTrendFileAA1_AAA1(self, fileNAD=None, MBDCode=None, reportName=None):
        """this reads data from AA1 and AAA1 worksheet"""
        """
        fileNADName = catCode_reportName.xlsx
        This function reads the Trendcheck excel file
        :param fileTrend: file trendCheck
        :param fileNAD: NAD file name for extracting the catCode from its name
        :param MBDCode: is the catCode of the largest MBD from the NAD file monthly
        :param category(catCode): if specified sheet's name will refer to ML_STAT_AA1/ML_STAT_AAA1
        :return: # the row of the largest MBD which we extract it from NAD file monthly
        """
        MBDCode = self._findMBDCode(mdbCode=MBDCode)
        compileObj = re.compile(r"[A-Za-z]+(_[A-Za-z]*)?")
        search = compileObj.search(os.path.basename(fileNAD))
        catCode = search.group()  # here is the catCode from the NAD File Monthly
        columnForAA1AAA1 = ["MBDCODE", "CATEGORY", "SALESVALUE_PROJETED_TSD"]
        compareCheck = {}
        get_category = 0
        if MBDCode == "AA1":
            compareCheck = {SALEVALUE: []}  # {'SALESVALUE':[?,?,...,?]}
            df_trend = pd.DataFrame(pd.read_excel(self.pathFileTrend
                                                  , sheet_name="ML_STAT_AA1")[columnForAA1AAA1]).groupby(by="CATEGORY")
            get_category = df_trend.get_group(catCode)  # group it by CATEGORY(catCode)
        elif MBDCode == "AAA1":
            compareCheck = {SALEVALUE: []}  # {'SALESVALUE':[?,?,...,?]}
            df_trend = pd.DataFrame(pd.read_excel(self.pathFileTrend
                                                  , sheet_name="ML_STAT_AAA1")[columnForAA1AAA1]).groupby(by="CATEGORY")
            get_category = df_trend.get_group(catCode)  # group it by CATEGORY(catCode)
        for i in range(len(get_category)):
            # get index of that salesvalue
            indx = get_category.index[0]
            sv = get_category.at[indx, SALEVALUE_TRENDFILE]
            # sv = self._roundDigitToWhole(get_category.at[indx, "SALESVALUE_PROJETED_TSD"])
            sv = self._roundDigitToWhole(sv)
            compareCheck[SALEVALUE].append(sv)

        return compareCheck # {'SALESVALUE':[?,?,...,?]}

    def _readTrendFileAll(self, reportName=None, sheetName="ML_SQL_ALL"):
        """This reads the data from 'ML_SQL_ALL' worksheet"""
        columnForAll = ["CATEGORY", "MBDCODE", "REPORTNAME", "SALESVALUE"]
        compareCheck = {}  # {"SALESVALUE":?}
        df_trend = pd.DataFrame(pd.read_excel(self.pathFileTrend
                                              , sheet_name=sheetName)[columnForAll]).groupby(by=["REPORTNAME"])
        get_category = df_trend.get_group(reportName)  # reportName = DBName
        for col in columnForAll:
            indxLabel = get_category.index[0]
            s = get_category.at[indxLabel, col]
            if col != SALEVALUE:
                compareCheck[col] = s
            else:
                s = self._roundDigitToWhole(s)
                compareCheck[SALEVALUE] = s

        return compareCheck # {"SALESVALUE":?, col1:?, col2:2, ...}

    def _getReportName(self, fileNAD=None):
        """
        :param fileNAD: this is the file's name
        :return: report's name/ report's line
        """
        compileObj = re.compile(r"[A-Z_a-z]*(-|_)([A-Za-z0-9]*)")
        search = compileObj.search(fileNAD)
        reportName = search.group(2) # plan for handle exception
        return reportName # report line from the NAD file monthly

    def _checkingSALESVALUEAA1_AAA1(self, svNeed2Check, svFromTrendCheck):
        """
        :param svNeed2Check:
        :param svFromTrendCheck:
        :return:
        """
        svNeed2Check = abs(svNeed2Check)
        for keySALESVALUE in svFromTrendCheck:
            svList = svFromTrendCheck[keySALESVALUE]
            svList = list(map(abs, svList))
            if svNeed2Check in svList:
                return True
            else: return False

    def _checkingHiddenMBDAndFACT(self, pathFileNAD):
        """
        Checking the hidden MBD which is two dimension consisting of 2 parts
        first: MBD
        second: Fact
        """
        list_column = []
        list_row = []
        list_fact_error = []
        list_mbd_error = []
        # if there is hidden MBD that's not corresponding to criteria, so it need to be marked to original files
        need2Log = {}
        df_nad = pd.DataFrame(pd.read_excel(pathFileNAD, skiprows=[i for i in range(self.skipRow)]))
        # change first two column names to 'MBD' and 'period'
        df_nad.rename(columns={df_nad.columns[0]:"MBD", df_nad.columns[1]:"MBDCode", df_nad.columns[2]:"period"}, inplace=True)
        # add the 'number' column for counting the row
        df_nad["number"] = np.arange(0, len(df_nad))
        # add new row for counting the column
        new_row = {col: index for index, col in enumerate(df_nad.columns)}
        df_nad = df_nad.append(new_row, ignore_index=True)
        df_nad = df_nad.set_index('MBD')  # set column 'MBD' to be index
        for fact in self.hiddenFact:
            for mbd in self.hiddenMBD:
                value = df_nad.at[mbd, fact]
                if str(value) != "nan":
                    column = df_nad[fact].iloc[-1]
                    row = df_nad.loc[mbd].iloc[-1]
                    list_column.append(column)
                    list_row.append(row)
                    list_fact_error.append(fact)
                    list_mbd_error.append(mbd)
                else: continue
        need2Log["log"] = list(zip(list_fact_error, list_mbd_error)) # name of hidden fact and hidden MBD
        need2Log["mark"] = list(zip(list_row, list_column)) # location of that hidden fact and hidden MBD
        need2Log["rowth"] = self.skipRow # start of the row to be marked
        return need2Log

    def mainCompare(self):
        dbNameNotFoundError = {}
        # log
        fileLog = self.pathRootNAD + "/" + "_month_LogFailer.xlsx"
        # toLog = wm.ToLog(pathLogFile=fileLog, sheets=["CheckSV_ND_WD", "Check NAN"])
        toLog = month_excel.Month_ToLog(pathLogFile=fileLog, sheets=["CheckSV_ND_WD", "Check NAN", "notFoundDBName"])
        # toLog.modifyWorkSheet()
        conn = cdbs.ConnDatabaseService()
        dbnameAndFile = conn.sql_DBNameAndFileQuery(self.service)
        counter_total = 0
        counter_fail = 0
        previousFile = None
        start_time = time.time()

        for dbname, fileNAD in dbnameAndFile: # item[0] is DBName, item[1] is corresponding file
            counter_total += 1
            pathFileNAD = self.pathRootNAD + "/" + fileNAD
            # mark = wm.MarkOriginal(pathFileNAD=pathFileNAD)
            mark = month_excel.Month_MarkOriginal(pathNADFile=pathFileNAD)
            reportName = self._getReportName(fileNAD=fileNAD)  # get report name
            need2Check, largest_MBD, largest_MBDCode = self._readNADFile(pathFileNAD)  # from NAD file
            # check SALESVALUE
            svDiff = None
            sv2Check = self._roundDigitToWhole(need2Check[largest_MBD][SALEVALUE_NADFILE])
            if largest_MBDCode in ("AA1", "AAA1"):
                try:
                    valueFromTrendCheck = self._readTrendFileAA1_AAA1(fileNAD=fileNAD
                                                                      , MBDCode=largest_MBDCode
                                                                      , reportName=reportName)
                except KeyError:
                    # in case of dbname did't put into the trend file
                    # in case of can't specify wanted sheet in the CheckTrend file
                    # in case of there is no "REPORTNAME" column header
                    # sv2Check = self._roundDigitToWhole(need2Check[largest_MBD]["Sales Value (Tsd.Baht)"])
                    counter_fail += 1
                    dbNameNotFoundError[dbname] = Monthly.dbNameError
                    continue
                else:
                    resultsv = self._checkingSALESVALUEAA1_AAA1(svNeed2Check=sv2Check
                                                                , svFromTrendCheck=valueFromTrendCheck)
                    # if sv from NAD File(sv2Check) doesn't match sv from trendCheck at AA1, AAA1 sheet
                    # , so it needs to check at 'ML_SQL_ALL' sheet
                    if not resultsv:
                        valueFromTrendCheck = self._readTrendFileAll(reportName=reportName)
                        resultsv, svDiff = self._check_SALEVALUE(sv_trend=valueFromTrendCheck[SALEVALUE]
                                                                        , sv_nad=sv2Check)
            else: # check at 'ML_SQL_ALL' sheet
                valueFromTrendCheck = self._readTrendFileAll(reportName=reportName)
                # resultsv, svDiff = self._check_SALEVALUE(sv_trend=valueFromTrendCheck[SALEVALUE]
                #                              , sv_nad=need2Check[largest_MBD]["Sales Value (Tsd.Baht)"])
                resultsv, svDiff = self._check_SALEVALUE(sv_trend=valueFromTrendCheck[SALEVALUE]
                                             , sv_nad=sv2Check)
            # check ND Selling
            nd2Check = need2Check[largest_MBD][ND_SELLING]
            resultnd, ndDiff = self._check_ND(nd2Check)
            # check WD Selling
            wd2Check = need2Check[largest_MBD][WD_SELLING]
            resultwd, wdDiff = self._check_WD(wd2Check)
            if dbname.upper().startswith("SR"):
                pass
            else:
                # checking Hidden MBD
                result_hidden = self._checkingHiddenMBDAndFACT(pathFileNAD=pathFileNAD)
                # write log for failing hiddenMBD
                if len(result_hidden["log"]) > 0:
                    mark.markHidden(failHidden=result_hidden)
                    toLog.writeLogHidden(failHidden=result_hidden
                                         , pathNADFile=fileNAD
                                         , report_name=dbname)
            # write to log and mark what fails in the NAD File
            if not (resultsv and resultnd and resultwd):
                # mark what fails in the NAD File
                mark.markSVNDWD(markSV=resultsv, markND=resultnd, markWD=resultwd
                                , col_sv=need2Check["column"][SALEVALUE_NADFILE]
                                , col_nd=need2Check["column"][ND_SELLING]
                                , col_wd=need2Check["column"][WD_SELLING]
                                , skipRow=self.skipRow)
                # write to excel log
                toLog.writeLogSVNDWD(logSV=resultsv, logND=resultnd, logWD=resultwd
                                     , valueSV=svDiff, valueND=ndDiff, valueWD=wdDiff
                                     , largest_MBD=largest_MBD
                                     , pathNADFile=fileNAD
                                     , report_name=dbname)
                # if previousFile != fileNAD and not (resultsv and resultnd and resultwd):
                # count the number of files that fail
                if previousFile != fileNAD:
                    counter_fail += 1
                    previousFile = fileNAD
                else: pass
            # # write log for failing hiddenMBD
            # if len(result_hidden["log"]) > 0:
            #     mark.markHidden(failHidden=result_hidden)
            #     toLog.writeLogHidden(failHidden=result_hidden
            #                          , pathNADFile=fileNAD
            #                          , report_name=dbname)
            mark.saveAction()
            mark.closeWorkBook()
            if bool(dbNameNotFoundError): # if there is the unmatched DBName
                toLog.write_logNotFoundDBName(dict_notFoundDBName=dbNameNotFoundError, orderOfSheet=2)
        toLog.saveAction()
        toLog.closeWorkBook()  # it's the same workBook
        end_time = time.time()
        self.conclude.totalTime = "{elapsed} s.".format(elapsed=end_time - start_time)
        self.conclude.totalFiles = counter_total
        self.conclude.totalFail = counter_fail
        popUp_task.alert_popUp(title="NAD Monthly", message=f"Monthly NAD files are finished.",
                               service=self.service)
