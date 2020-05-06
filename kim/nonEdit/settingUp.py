import json
from pathlib import Path  # mix path
import os  # create folder
import distutils.file_util
import datetime
import time
import shutil
# import zipfile
import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s-%(message)s")
logging.disable(logging.DEBUG)

def userInput():
    path_period = input("Period[Oct'19]:")
    day = input("date[01-31]: ")
    month = input("mouth[01-12]: ")
    year = input("Year[20xx]: ")
    return path_period, day, month, year

keyWord_extension = [
    ".CHR", ".HED", ".IDX", ".INF", ".TAD"
]
class AutoCopy():
    def __init__(self, *, day, month, year, period, folder):
        self.targetFolder = folder
        self.parentStartPath = Path(r"\\BKKWINSQL02\isightengine\Databases")
        self.parentFinalPath = Path(r"G:\Shared drives\Nielsen Backup Database (Important)")
        self.pathInFullG = None
        self.pathPeriod = period
        self.day = day
        self.month = month
        self.year = year
        self.userTime = datetime.datetime(int(self.year), int(self.month), int(self.day))

    def makingDirectory(self, pathDirectory):
        logging.debug(f"--making the folder: {pathDirectory}")
        try:
            os.makedirs(pathDirectory)
        except FileExistsError:
            logging.debug(f"--{pathDirectory} already exists")

    def autoCopy_oneLevel(self):
        finalPath = self.parentFinalPath / self.pathPeriod
        logging.debug(f"--finalPath: {finalPath}")# G:\Shared drives\Nielsen Backup Database (Important)\nonTest\Oct'19
        self.makingDirectory(finalPath)
        cnt = 0
        fileSize = {}
        parentPathToCopy = self.parentStartPath / self.targetFolder
        logging.debug(f"----parentPathToCopy: {parentPathToCopy}") # \\BKKWINSQL02\isightengine\Databases\Monthly Retail Index
        parentPathToPaste = finalPath / self.targetFolder
        self.pathInFullG = parentPathToPaste
        logging.debug(f"----parentPathToPaste: {parentPathToPaste}")# G:\Shared drives\Nielsen Backup Database (Important)\nonTest\Oct'19\Monthly Retail Index
        self.makingDirectory(parentPathToPaste)
        for item in os.listdir(parentPathToCopy): # item is file name
            itemPathToCopy = parentPathToCopy / item # G:\Shared drives\Nielsen Backup Database (Important)\nonTest\Oct'19\Monthly Retail Index\fileName.CHR
            if os.path.isfile(itemPathToCopy) :
                lastModify = datetime.datetime.fromtimestamp(os.stat(itemPathToCopy).st_mtime)
                startSize = os.path.getsize(itemPathToCopy)
                logging.debug(f"--------itemPathToCopy: {itemPathToCopy}-----{startSize}----{lastModify > self.userTime}")
                if lastModify > self.userTime:
                    # shutil.copy(itemPathToCopy, parentPathToPaste)
                    logging.debug(f"--------copied {item}")
                    distutils.file_util.copy_file(itemPathToCopy, parentPathToPaste, update=1)
                    fileSize[os.path.dirname(parentPathToCopy)+"\\"+os.path.basename(parentPathToCopy) + "\\" + item] = startSize
                    cnt += 1
                else:pass
            else:pass
        pathJson = parentPathToCopy / f"copiedFileName.json"
        with open(pathJson, "w") as jsonFile:
            json.dump(fileSize, jsonFile)
        distutils.file_util.copy_file(pathJson, parentPathToPaste)

    def throughTree(self, ppathToCopy, ppathTopaste):
        fileSize = {}
        makingDirectory = self.makingDirectory
        userTime =self.userTime
        def wrapper(pathCopy, pathPaste, userTime):
            creatingFolder = True
            logging.debug(f"we're at {pathCopy}")
            for item in os.listdir(pathCopy):
                itemPathToCopy = pathCopy / item
                if os.path.isfile(itemPathToCopy):
                    lastModify = datetime.datetime.fromtimestamp(os.stat(itemPathToCopy).st_mtime)
                    startSize = os.path.getsize(itemPathToCopy)
                    logging.debug(f"--------item's name: {item}")
                    condition = lastModify > userTime and (item[item.rfind("."):].upper() in keyWord_extension)
                    logging.debug(f"--------itemPathToCopy: {itemPathToCopy}-----{startSize}----{condition}")
                    if condition:
                        if creatingFolder:
                            makingDirectory(pathPaste / item)
                            creatingFolder = False
                        # distutils.file_util.copy_file(itemPathToCopy, pathPaste, update=1)
                        shutil.copy(itemPathToCopy, pathPaste)
                        logging.debug(f"--------copied {item}")
                        fileSize[os.path.dirname(pathCopy) +"\\"+os.path.basename(pathCopy)+ "\\" + item] = startSize
                    else: continue
                else:
                    wrapper(itemPathToCopy, pathPaste / item, userTime)
        wrapper(ppathToCopy, ppathTopaste, userTime)
        logging.debug("Finished")
        pathJson = ppathToCopy / f"copiedFileName.json"
        with open(pathJson, "w") as jsonFile:
            logging.debug(f"create json file: {pathJson}")
            json.dump(fileSize, jsonFile)
        distutils.file_util.copy_file(pathJson, ppathTopaste)

    def autocopy_everyLevel(self):
        finalPath = self.parentFinalPath / self.pathPeriod
        logging.debug(f"finalPath: {finalPath}")
        # G:\Shared drives\Nielsen Backup Database (Important)\nonTest\Oct'19
        self.makingDirectory(finalPath)
        parentPathToCopy = self.parentStartPath / self.targetFolder
        logging.debug(f"parentPathToCopy: {parentPathToCopy}")
        # \\BKKWINSQL02\isightengine\Databases\Monthly Retail Index
        parentPathToPaste = finalPath / self.targetFolder
        self.pathInFullG = parentPathToPaste
        logging.debug(f"parentPathToPaste: {parentPathToPaste}")
        self.makingDirectory(parentPathToPaste)
        # G:\Shared drives\Nielsen Backup Database (Important)\nonTest\Oct'19\Monthly Retail Index
        self.throughTree(parentPathToCopy, parentPathToPaste)

    def SizeCheckingFromG(self):
        """ this action is in the Google Shared Drive"""
        print("starting checking")
        path = self.parentFinalPath / self.pathPeriod / self.targetFolder
        pathLogJson = path / "copiedFileName.json"
        log = {}
        error = {}
        errorLog = {}
        parentPathToCopy = self.parentStartPath / self.targetFolder
        with open(pathLogJson) as logJson:
            log = json.load(logJson)
        def throughTree(pathG):
            for item in os.listdir(pathG):
                itemPath = pathG / item
                if os.path.isfile(itemPath) and not item.endswith(".json"):
                    keySearch = os.path.dirname(parentPathToCopy)+"\\"+os.path.basename(parentPathToCopy) + "\\" + item
                    size = os.path.getsize(itemPath)
                    if size == log[keySearch]:pass
                    else:
                        error[keySearch] = log[keySearch]
                        error[item] = size
                        errorLog[keySearch] = error.copy()
                else:
                    if not item.endswith(".json"):
                        throughTree(itemPath)
            pathErrorFile = path / "fileError.json"
            with open(pathErrorFile, "w") as jsonError:
                json.dump(errorLog, jsonError)
            print("finish checking")
        throughTree(self.pathInFullG)
if __name__ == "__main__":
    def timing(func):
        def wrapper():
            start = time.perf_counter()
            func()
            print(f"time on {func.__name__}: {time.perf_counter() - start}")
        return wrapper

    @timing
    def main_oneLevel():
        test = AutoCopy(day=31, month=1, year=2020, period="FEB'20", folder="Monthly Retailer")
        test.autoCopy_oneLevel()

    @timing
    def main_everyLevel():
        test = AutoCopy(day=1, month=12, year=2019, period="FEB'20", folder=r"Weekly Database\ScanTrack Makro")
        # folder = Weekly Database\ScanTrack Makro
        test.autocopy_everyLevel()
    main_everyLevel()
    main_oneLevel()
    pathForOneLevel = [
            r"X:\Databases\Monthly Retail Index"
            , r"X:\Databases\Monthly Retailer"
            , r"X:\Databases\Weekly Retailer"
            , r"X:\Databases\Weekly Database\e-Commerce\Manufacturer"
            , r"X:\Databases\Weekly Database\Manufact"
            , r"X:\Databases\Weekly Database\Causal"
            , r"X:\Databases\DDP\Watsons"
    ]
    pathForEveryLevel = [
        r"X:\Databases\Weekly Database\ScanTrack Family Mart"
        , r"X:\Databases\Weekly Database\ScanTrack Big C"
        , r"X:\Databases\Weekly Database\ScanTrack Makro"
        , r"X:\Databases\Weekly Database\ScanTrack Tesco"
        , r"X:\Databases\Weekly Database\ScanTrack The Mall"
        , r"X:\Databases\Weekly Database\ScanTrack Tops"
    ]
    keyWord_extension =[
        "CHR", "HED", "IDX", "INF", "TAD"
    ]
    keyWord_name = {
            "ScanTrack Family Mart":{"keywprd":["FM"]}
            , "ScanTrack Big C":{"keyword":["SB"]}
            , "ScanTrack Makro":{"keyword":["MK"]}
            , "ScanTrack Tesco":{"keyword":["SL"]}
            , "ScanTrack The Mall": {"keyword": ["TM"]}
            , "ScanTrack Tops": {"keyword": ["ST", "DT"]}
    }














