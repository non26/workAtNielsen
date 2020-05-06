import csv
# from PyNielsen.kim.nonEditVersion2.popUp import alert_popUp
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
    def __init__(self, *, day=None, month=None, year=None, period=None, folder=None):
        name = folder.split('\\')[-1].replace(' ', '')
        self.parentStartPath = Path(r"\\BKKWINSQL02\isightengine\Databases")
        self.parentFinalPath = Path(r"G:\Shared drives\Nielsen Backup Database (Important)")
        self.childStartPath_l1 = self.parentStartPath / folder
        self.childFinalPath_l1 = self.parentFinalPath / period / folder
        self.pathStartLogCsv = self.childStartPath_l1 / f"logCopiedFiles_{name}.csv"
        self.pathFinalLogCsv = self.childFinalPath_l1 / f"logCopiedFiles_{name}.csv"
        self.pathFinalLogCsvError = self.childFinalPath_l1 / f"logCopiedFiles_{name}_error.csv"
        self.userTime = datetime.datetime(int(year), int(month), int(day))
        self._makingDirectory(self.childFinalPath_l1)

    @staticmethod
    def _makingDirectory(pathDirectory):
        logging.debug(f"--making the folder: {pathDirectory}")
        try:
            os.makedirs(pathDirectory)
        except FileExistsError:
            logging.debug(f"--{pathDirectory} already exists")

    @staticmethod
    def _copyingFilesNoMetaData(thisDirectory, targetDirectory):
        """
        Copy the contents (no metadata)
        of the file named src to a file named dst
        and return dst in the most efficient way possible
        """
        try:
            shutil.copyfile(thisDirectory, targetDirectory)
        except FileNotFoundError: pass

    @staticmethod
    def _copyingFilesMetaData(thisDirectory, targetDirectory):
        """
        copy() copies the file data and the file’s permission mode (see os.chmod()). Other metadata
        , like the file’s creation and modification times, is not preserved.
        :param thisDirectory:
        :param targetDirectory:
        :return:
        """
        try:
            shutil.copy2(thisDirectory, targetDirectory)
        except FileNotFoundError: pass

    @staticmethod
    def _removeFile(directory):
        try:
            os.remove(directory)
        except (FileExistsError, OSError): pass

    @staticmethod
    def _lostInternet():
        IPaddress = socket.gethostbyname(socket.gethostname())
        if IPaddress == "127.0.0.1": # no internet access
            return True

    def auto_copy(self, deep="--all", criteriaExtension=None, fileIterater=None, createSubFolders=False):
        # make the instance attributes become local to this method
        pathToCopy = self.childStartPath_l1
        pathToPaste = self.childFinalPath_l1
        userTime = self.userTime
        copyingFilesMetaData = self._copyingFilesMetaData # referenced function
        makeDirectory = self._makingDirectory # referenced function
        self._removeFile(self.pathStartLogCsv)
        creatingFolder = createSubFolders
        countFolders = 0
        countFiles = 0

        file = open(self.pathStartLogCsv, 'w', newline='')
        csvWriter = csv.writer(file)
        csvWriter.writerow(["path copied", "size (bytes)", "path paste"]) # write header
        level = deep if deep != "--all" else float("inf") # start at 1 for the first level of the directory
        # iterFile = iter(os.listdir(pathToCopy)) if not fileIterater else fileIterater
        def throughDirectory(pathToCopy, pathToPaste, count):
            """
            this function is to iterate through the directory every levels or just
            deep as specified by user, this can be simulated by os.walk()
            """
            nonlocal creatingFolder, countFiles, countFolders
            cnt_level = count # count the deep of directory level
            for item in os.listdir(pathToCopy):
                itemPathToCopy = pathToCopy / item
                itemPathToPaste = pathToPaste / item
                condition1 = os.path.isfile(itemPathToCopy) and not item.lower().endswith(".csv")
                if condition1: # check that it is a file or not
                    lastModify = datetime.datetime.fromtimestamp(os.stat(itemPathToCopy).st_mtime)
                    startSize = os.path.getsize(itemPathToCopy)
                    if bool(criteriaExtension):
                        condition2 = lastModify > userTime and (item[item.rfind("."):].upper() in criteriaExtension)
                    else: condition2 = lastModify > userTime
                    if condition2: # last modified file needs to be more than user input.
                        # self.cnt_files += 1
                        countFiles += 1
                        # distutils.file_util.copy_file(itemPathToCopy, pathToPaste, update=1)
                        if creatingFolder: # if there is at least 1 file in the directory then create folder
                            # self.cnt_folders += 1
                            countFolders += 1
                            makeDirectory(itemPathToPaste)
                            creatingFolder = False
                        try:
                            # shutil.copy(itemPathToCopy, pathToPaste)
                            copyingFilesMetaData(itemPathToCopy, pathToPaste)
                        except Exception as e: pass
                        else:
                            csvWriter.writerow([str(itemPathToCopy), startSize, str(itemPathToPaste)])
                elif cnt_level < level:
                    cnt_level += 1
                    # recursive
                    creatingFolder = True
                    throughDirectory(itemPathToCopy, itemPathToPaste, cnt_level) # caller2 for recursive.
                    cnt_level -= 1
                else:
                    continue
        # remove the csv files at destination path if exist
        self._removeFile(self.pathFinalLogCsv)
        self._removeFile(self.pathFinalLogCsvError)
        # caller1
        throughDirectory(pathToCopy, pathToPaste, 1)
        # write the number of total files and total folders to the csv
        csvWriter.writerow(["","total files:"])
        csvWriter.writerow(["", countFiles])
        csvWriter.writerow(["", "total folder:"])
        csvWriter.writerow(["", countFolders])
        file.close()
        # shutil.copyfile(self.pathStartLogCsv, self.pathFinalLogCsv)
        self._copyingFilesNoMetaData(self.pathStartLogCsv, self.pathFinalLogCsv)
        # remove log file at the start path
        self._removeFile(self.pathStartLogCsv)

    @staticmethod
    def SizeCheckingFromG(wantedPath):
        """ this action is in the Google Shared Drive"""
        fileName = os.path.basename(wantedPath)
        # nameFolder can be find by this pattern
        nameFolder = fileName[fileName.find("_")+1:fileName.find(".")]
        errorCsv = os.path.dirname(wantedPath) +"\\"+ f"logCopiedFiles_{nameFolder}_error.csv"
        csvErrorFile = open(errorCsv, 'w', newline="")
        csvFile = open(wantedPath, 'r')

        writer = csv.writer(csvErrorFile)
        reader = csv.reader(csvFile)
        writer.writerow(["copied", "copied size", "pasted", 'pasted size'])
        cnt_error = 0
        for index, row in enumerate(reader):
            if index != 0:
                copiedSizeFile = row[1] # size from the source
                try:
                    pathItemG = row[2] # path file at Google shared drive
                    sizeItemG = os.path.getsize(pathItemG)
                except Exception:
                    writer.writerow(row)
                else:
                    if copiedSizeFile == sizeItemG:
                        writer.writerow(row)
                    else:
                        # writer.writerow([row[0], row[1], row[2], sizeItemG])
                        row.extend([sizeItemG])
                        writer.writerow(row)
        csvErrorFile.close()
        csvFile.close()

        return cnt_error # the number of error path