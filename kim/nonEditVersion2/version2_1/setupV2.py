import csv
from PyNielsen.kim.nonEditVersion2.popUp import alert_popUp
# import json
from pathlib import Path  # mix path
import os  # create folder
# import distutils.file_util
import datetime
import time
import shutil
# import zipfile
import logging
import socket

def timing(cls):
    def wrapper_time(*, day, month, year, period, folder):
        start = time.time()
        obj = cls(day=day, month=month, year=year, period=period, folder=folder)
        obj.measureTime = time.time() - start
        return obj
    return wrapper_time


class AutoCopy():
    def __init__(self, *, day, month, year, period, folder):
        name = folder.split('\\')[-1].replace(' ', '')
        self.parentStartPath = Path(r"\\BKKWINSQL02\isightengine\Databases")
        self.parentFinalPath = Path(r"G:\Shared drives\Nielsen Backup Database (Important)")
        self.childStartPath_l1 = self.parentStartPath / folder
        self.childFinalPath_l1 = self.parentFinalPath / period / folder
        self.pathStartLogCsv = self.childStartPath_l1 / f"logCopiedFiles_{name}.csv"
        self.pathFinalLogCsv = self.childFinalPath_l1 / f"logCopiedFiles_{name}.csv"
        self.pathFinalLogCsvError = self.childFinalPath_l1 / f"logCopiedFiles_{name}_error.csv"
        self.userTime = datetime.datetime(int(year), int(month), int(day))
        self.cnt_folders = 0
        self.cnt_files = 0

    def makingDirectory(self, pathDirectory):
        logging.debug(f"--making the folder: {pathDirectory}")
        try:
            os.makedirs(pathDirectory)
        except FileExistsError:
            logging.debug(f"--{pathDirectory} already exists")

    def removeFile(self, directory):
        try:
            os.remove(directory)
        except (FileExistsError, OSError): pass

    @staticmethod
    def lostInternet():
        IPaddress = socket.gethostbyname(socket.gethostname())
        if IPaddress == "127.0.0.1": #  no internet access
            return True

    def auto_copy(self, deep="--all", criteriaExtension=None, fileIterater=None):
        pathToCopy = self.childStartPath_l1
        pathToPaste = self.childFinalPath_l1
        userTime = self.userTime
        makeDirectory = self.makingDirectory # referenced function
        self.removeFile(self.pathStartLogCsv)

        file = open(self.pathStartLogCsv, 'w', newline='')
        csvWriter = csv.writer(file)
        csvWriter.writerow(["path copied", "size (bytes)", "path paste"])
        level = deep if deep != "--all" else float("inf") # start at 1 for the first level of the directory
        itFile = iter(os.listdir(pathToCopy)) if not fileIterater else fileIterater
        def throughDirectory(pathToCopy, pathToPaste, count):
            cnt_level = count
            creatingFolder = True
            for item in itFile:
                itemPathToCopy = pathToCopy / item
                itemPathToPaste = pathToPaste / item
                condition1 = os.path.isfile(itemPathToCopy) and not item.lower().endswith(".csv")
                if condition1:
                    lastModify = datetime.datetime.fromtimestamp(os.stat(itemPathToCopy).st_mtime)
                    startSize = os.path.getsize(itemPathToCopy)
                    if bool(criteriaExtension):
                        condition2 = lastModify > userTime and (item[item.rfind("."):].upper() in criteriaExtension)
                    else: condition2 = lastModify > userTime
                    if condition2:
                        self.cnt_files +=1
                        # distutils.file_util.copy_file(itemPathToCopy, pathToPaste, update=1)
                        if creatingFolder: # if there is at least 1 file in the directory then create folder
                            self.cnt_folders += 1
                            makeDirectory(itemPathToPaste)
                            creatingFolder = False
                        try:
                            shutil.copy(itemPathToCopy, pathToPaste)
                        except Exception as e: pass
                        else:
                            csvWriter.writerow([str(itemPathToCopy), startSize, str(itemPathToPaste)])
                elif cnt_level < level:
                    cnt_level += 1
                    # recursive
                    throughDirectory(itemPathToCopy, itemPathToPaste, cnt_level)
                    cnt_level -= 1
                else:
                    continue
        self.removeFile(self.pathFinalLogCsv)
        self.removeFile(self.pathFinalLogCsvError)
        throughDirectory(pathToCopy, pathToPaste, 1)
        csvWriter.writerow(["total files:", self.cnt_files, "total folder:,", self.cnt_folders-1])
        file.close()
        shutil.copyfile(self.pathStartLogCsv, self.pathFinalLogCsv)
        self.removeFile(self.pathStartLogCsv)
    @staticmethod
    def SizeCheckingFromG(wantedPath=None):
        """ this action is in the Google Shared Drive"""
        fileName = os.path.basename(wantedPath)
        nameFolder = fileName[fileName.find("_")+1:fileName.find(".")]
        errorCsv = os.path.dirname(wantedPath) +"\\"+ nameFolder
        csvErrorFile = open(errorCsv, 'w', newline="")
        csvFile = open(wantedPath, 'r')

        writer = csv.writer(csvErrorFile)
        reader = csv.reader(csvFile)
        length = len(reader)
        writer.writerow(["copied", "copied size", "pasted", 'pasted size'])
        cnt_error = 0
        for index, row in enumerate(reader):
            if index != 1 and index != length - 1:
                copiedSizeFile = row[1] # size from src
                pathItemG = row[2] # path file at Google shared drive
                sizeItemG = os.path.getsize(pathItemG)
                if copiedSizeFile == sizeItemG:
                    pass
                else:
                    writer.writerow([row[0], row[1], row[2], sizeItemG])
        csvErrorFile.close()
        csvFile.close()
        return cnt_error
                    











