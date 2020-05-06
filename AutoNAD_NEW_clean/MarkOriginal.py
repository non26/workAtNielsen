import openpyxl
from openpyxl.styles.fills import PatternFill
import os
import datetime
from .ConWorkBook import ConnWorkBook

class MarkOriginal(ConnWorkBook):
    def __init__(self, pathNADFile=None, sheetName="Sheet1"):
        """
        :param pathNADFile:
        :param sheetName:
        """
        self.pathFileNAD = pathNADFile
        ConnWorkBook.__init__(self, pathFile=pathNADFile)
        self.selectWorkSheet(sheetName)
        self.markColor = PatternFill(start_color='F0FF00'
                                     , end_color='F0FF00', fill_type='solid')

    def markSVNDWD(self, skipRow=0
                   , markSV=True, markND=True, markWD=True
                   , col_sv=None, col_nd=None, col_wd=None): pass
    def markHidden(self, failHidden): pass
