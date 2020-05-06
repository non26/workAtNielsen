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

def readSource(path):
    df1 = pd.read_excel(path)
    for i in range(len(df1)):
        yield df1.iloc[i, 0]

def has(string, lookFor):
    if string.lower().find(lookFor.lower()) == -1:
        return False
    else:
        return True
def getFileSize(pathFile):
    try:
        size = os.path.getsize(pathFile)
    except (FileNotFoundError, Exception) as e:
        return None
    else:
        return size

def withExtension(superPath):
    fiveSize = 0
    nonFiveSize = 0
    for dbName in readSource("infactDatabase.xlsx"):
        print(f"dbName: {dbName}")
        for root, folders, files in os.walk(superPath):
            if not has(root, "\\sff"): # this means it's not sff
                for file in files:
                    current_path = root + "\\" + file
                    try:
                        t = os.path.getmtime(current_path)
                    except (FileNotFoundError, Exception):
                        continue
                    modified_date = datetime.datetime.fromtimestamp(t)
                    modified_date = str(modified_date)
                    if has(file, dbName) and has(modified_date, "2020/04"):
                        extension = file[file.find("."):]
                        # size = os.path.getsize(current_path)
                        size = getFileSize(current_path)
                        if size is not None:
                            size = size
                        else:
                            continue
                        if extension.upper() in dataBaseExtension:
                            fiveSize += size
                        else:
                            nonFiveSize += size
                    else: continue
            else: continue
        yield dbName, fiveSize, nonFiveSize
        fiveSize = 0
        nonFiveSize = 0

def sff(superPath):
    for sffName in readSource("sff.xlsx"):
        print(f"sff name: {sffName}")
        for root, folders, files in os.walk(superPath):
            if has(root, "\\sff"):
                for file in files:
                    if has(file, sffName):
                        current_path = root + "\\" + file
                        name = file[:file.find(".")]
                        # size = os.path.getsize(current_path)
                        size = getFileSize(current_path)
                        if size is not None:
                            size = size
                        else:
                            continue
                        yield name, size
                    else: continue
            else: continue

def main():
    fiveExtensionExcecl = ToExcel("FiveExtension.xlsx")
    fiveExtensionExcecl.activeWorksheet()
    allExtensionExcel = ToExcel("AllExtension.xlsx")
    allExtensionExcel.activeWorksheet()
    sffFileExcel = ToExcel("sff.xlsx")
    sffFileExcel.activeWorksheet()
    superPath = r"\\HKGWINFSVINS02\Share_N\RF35\Infact\PROD"
    for dbName, fiveFilesSize, nonFiveFilesSize in withExtension(superPath):
        fiveExtensionExcecl.writeValue(dbName, fiveFilesSize)
        allExtensionExcel.writeValue(dbName, fiveFilesSize+nonFiveFilesSize)
    print("*"*100)
    fiveExtensionExcecl.saveWorkBook()
    allExtensionExcel.saveWorkBook()
    for sffName, size in sff(superPath):
        print(f"sff name: {sffName}")
        sffFileExcel.writeValue(sffName, size)
    print("-" * 100)
    sffFileExcel.saveWorkBook()
main()










