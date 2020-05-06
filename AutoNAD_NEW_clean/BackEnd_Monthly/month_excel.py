from ..MarkOriginal import MarkOriginal
from ..ToLog import ToLog
import os

class Month_MarkOriginal(MarkOriginal):
    def __init__(self, pathNADFile=None, sheetName="Sheet1"):
        MarkOriginal.__init__(self, pathNADFile, sheetName)

    def markSVNDWD(self, markSV=True, markND=True, markWD=True
                   , col_sv=None, col_nd=None, col_wd=None, skipRow=None):
        """
        :param markSV:
        :param markND:
        :param markWD:
        :param col_sv:
        :param col_nd:
        :param col_wd:
        :return:
        """
        row_const = skipRow + 2
        if not markSV:
            self.workSheet.cell(row=row_const, column=col_sv+1).fill = self.markColor
        if not markND:
            self.workSheet.cell(row=row_const, column=col_nd+1).fill = self.markColor
        if not markWD:
            self.workSheet.cell(row=row_const, column=col_wd+1).fill = self.markColor

    def markHidden(self, failHidden=None):
        row_const = failHidden["rowth"] + 2
        for rowth, columnth in failHidden["mark"]:
            self.workSheet.cell(row=rowth+row_const, column=columnth+1).fill = self.markColor

class Month_ToLog(ToLog):

    def __init__(self, pathLogFile=None, sheets=None):
        ToLog.__init__(self, pathLogFile=pathLogFile, sheets=sheets)
        self.countRow_hidden = 2
        self.countRow_svndwd = 2

    def writeLogSVNDWD(self, chain=None
                       , pathNADFile=None, period=None, largest_MBD=None
                       , logSV=True, logND=True, logWD=True
                       , valueSV=None, valueND=None, valueWD=None
                       , dbname=None, report_name=None, report_line=None):
        """
         first item of self.workSheets
        :param logSV:
        :param logND:
        :param valueND:
        :param logWD:
        :param valueWD:
        :param valueSV:
        :param large_MBD:
        :param pathNADFile:
        :param report_name:
        :param report_line:
        :return:
        """
        dirName = os.path.dirname(self.pathLogFile)
        pathFile_NAD = dirName + "/" + pathNADFile
        if self.countRow_svndwd == 2:
            self.workSheets[0].cell(column=1, row=1).value = 'file NAD'
            self.workSheets[0].cell(column=2, row=1).value = "Report Name"
            self.workSheets[0].cell(column=3, row=1).value = 'Large MBD'
            self.workSheets[0].cell(column=4, row=1).value = 'Fact'
            self.workSheets[0].cell(column=5, row=1).value = 'Result'
        if not logSV:
            self.workSheets[0].cell(column=1, row=self.countRow_svndwd).value = pathNADFile
            self.workSheets[0].cell(column=1, row=self.countRow_svndwd).hyperlink = pathFile_NAD
            self.workSheets[0].cell(column=2, row=self.countRow_svndwd).value = report_name
            self.workSheets[0].cell(column=3, row=self.countRow_svndwd).value = largest_MBD
            self.workSheets[0].cell(column=4, row=self.countRow_svndwd).value = 'SALE VALUE'
            self.workSheets[0].cell(column=5, row=self.countRow_svndwd).value = "{:,}".format(valueSV)
            self.workSheets[0].cell(column=5, row=self.countRow_svndwd).fill = self.less if valueSV < 0 else self.more
            self.countRow_svndwd += 1
        if not logND:
            self.workSheets[0].cell(column=1, row=self.countRow_svndwd).value = pathNADFile
            self.workSheets[0].cell(column=1, row=self.countRow_svndwd).hyperlink = pathFile_NAD
            self.workSheets[0].cell(column=2, row=self.countRow_svndwd).value = report_name
            self.workSheets[0].cell(column=3, row=self.countRow_svndwd).value = largest_MBD
            self.workSheets[0].cell(column=4, row=self.countRow_svndwd).value = 'ND SELLING'
            self.workSheets[0].cell(column=5, row=self.countRow_svndwd).value = valueND
            self.countRow_svndwd += 1
        if not logWD:
            self.workSheets[0].cell(column=1, row=self.countRow_svndwd).value = pathNADFile
            self.workSheets[0].cell(column=1, row=self.countRow_svndwd).hyperlink = pathFile_NAD
            self.workSheets[0].cell(column=2, row=self.countRow_svndwd).value = report_name
            self.workSheets[0].cell(column=3, row=self.countRow_svndwd).value = largest_MBD
            self.workSheets[0].cell(column=4, row=self.countRow_svndwd).value = 'WD SELLING'
            self.workSheets[0].cell(column=5, row=self.countRow_svndwd).value = valueWD
            self.countRow_svndwd += 1
    def writeLogHidden(self, failHidden=None, pathNADFile=None, report_name = None):
        """
        second item of self.workSheets
        :param failHidden:
        :param pathNADFile:
        :param report_name:
        :param report_line:
        :return:
        """
        dirName = os.path.dirname(self.pathLogFile)
        pathFile_NAD= dirName + "/" + pathNADFile
        if self.countRow_hidden == 2:
            self.workSheets[1].cell(column=1, row=1).value = 'file NAD'
            self.workSheets[1].cell(column=2, row=1).value = "Report Name"
            self.workSheets[1].cell(column=3, row=1).value = 'MBD'
            self.workSheets[1].cell(column=4, row=1).value = 'Fact'
        for fact, hiddenMBD in failHidden["log"]:
            self.workSheets[1].cell(row=self.countRow_hidden, column=1).value = pathNADFile
            self.workSheets[1].cell(row=self.countRow_hidden, column=1).hyperlink = pathFile_NAD
            self.workSheets[1].cell(row=self.countRow_hidden, column=2).value = report_name
            self.workSheets[1].cell(row=self.countRow_hidden, column=3).value = hiddenMBD
            self.workSheets[1].cell(row=self.countRow_hidden, column=4).value = fact
            self.countRow_hidden += 1