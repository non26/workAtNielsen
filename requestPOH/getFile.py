import os
import pandas as pd
import datetime
import openpyxl
dataBaseExtension = ('.CHR', '.HED', '.IDX', '.INF', '.TAD')
class ToExcel:
    def __init__(self, workBookName):
        self.workBookName = workBookName
        self.workSheet = None
        self.workBook = openpyxl.workbook.Workbook()
        self.row = 1

    def activeWorksheet(self, sheetName = "Sheet1"):
        try:
            self.workSheet = self.workBook[sheetName]
        except Exception:  # If work sheet does't exist then create it.
            self.workSheet = self.workBook.create_sheet(title=sheetName)

    def writeValue(self, dbName, size):
        self.workSheet[f"A{self.row}"] = dbName
        self.workSheet[f"B{self.row}"] = size
        self.row += 1

    def saveWorkBook(self):
        self.workBook.save(self.workBookName)
def has(string, lookFor):
    if string.lower().find(lookFor.lower()) == -1:
        return False
    else:
        return True
def meetDate(path, date="2020/04"):
    try:
        t = os.path.getmtime(path)
    except (FileNotFoundError, Exception):
        return False
    modified_date = datetime.datetime.fromtimestamp(t)
    modified_date = str(modified_date)
    if has(modified_date, date):
        return True
    else:
        return False
def getFileSize(pathFile):
    try:
        size = os.path.getsize(pathFile)
    except (FileNotFoundError, Exception) as e:
        return None
    else:
        return size
def getFile(path):
    for root, folders, files in os.walk(path):
        print(root, end=" ")
        for file in files:
            current_file = root + "\\" + file
            if meetDate(current_file):
                if not has(root, "\\sff"): # means it's not sff
                    dot = file[file.find("."):]
                    if dot in dataBaseExtension:
                        yield "f", current_file
                    else:
                        yield "n", current_file
                else: # it's sff
                    yield "s", current_file
            else:
                continue
def main():
    nonFiveFile = ToExcel("nonSFF.xlsx")
    sffFile = ToExcel("SFF.xlsx")
    fiveFile = ToExcel("fiveFile.xlsx")
    fiveFile.activeWorksheet()
    nonFiveFile.activeWorksheet()
    sffFile.activeWorksheet()
    superPath = r"\\HKGWINFSVINS02\Share_N\RF35\Infact\PROD"
    for flag, path in getFile(superPath):
        size = getFileSize(path)
        print(size)
        if flag == "n":
            nonFiveFile.writeValue(path, size)
        elif flag == "f":
            fiveFile.writeValue(path, size)
        else:
            sffFile.writeValue(path, size)
    nonFiveFile.saveWorkBook()
    sffFile.saveWorkBook()
    fiveFile.saveWorkBook()