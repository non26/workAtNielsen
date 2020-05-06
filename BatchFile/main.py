from . import IClass as ic
from .IClass import IFile
from .IClass import IZipFile
from .IClass import IToLog
import math
import os

# file type input
INFACT = "infact"
INFACT_PASSWORD = "infact password"
SFF = "sff"
SFF_RENAME = "sff rename"
SFF_PASSWORD = "sff password"

class MoveFile:
    def __init__(self, dataDict: dict):
        # # Arrange data from dictionary
        # it's the same dbname, so it'll have the same  file type
        self.file_type = dataDict[ic.FILE_TYPE][0]
        # dbname, there's only one dbname
        self.dbName = dataDict[ic.DB_NAME][0]
        # it's the same dbname, so it'll have the same file extension
        self.extension_String = dataDict[ic.FILE_EXTENSION][0]
        # it's the same dbname, so it'll have the same source path
        self.source_path = dataDict[ic.SOURCE_PATH][0]
        # it's the same dbname, so it'll have the same  mediator path
        self.mediator_path = dataDict[ic.MEDIATOR_PATH][0]
        # destination path, it's the same dbname, so it'll have the same source path
        self.destination_path = dataDict[ic.DESTINATION_PATH][0]
        # status of zipping of each destination
        self.has_to_zip_list = dataDict[ic.HAS_ZIP]
        # rename status of each destination, it'll be the same amount of destination path
        self.has_to_rename_list = dataDict[ic.HAS_RENAME]
        # rename to what ?
        self.rename_to_list = dataDict[ic.RENAME_TO]
        # password status of each destination, it'll be the same amount of destination path
        self.has_to_password_list = dataDict[ic.HAS_PASSWORD]
        # set password to what?
        self.password_to_list = dataDict[ic.PASSWORD_TO]

        # # Arrange new data from above data
        # create list of extension
        self.extensionList = IFile.splitExtension(ExtensionString=self.extension_String)
        # find files that's corresponding to condition
        self.filePathList_source, self.fileNameList_source = IFile.findFile(self.source_path, self.dbName, self.extensionList)
        # find file's size in the 'source'
        self.fileSizeList_source = [IFile.getFileSize(filePath) for filePath in self.filePathList_source]
        # file's date at the 'source path'
        self.fileDateList_source = [IFile.getFileDate(filePath) for filePath in self.filePathList_source]
        # file path at 'mediator path'
        self.filePathList_mediator = list(map(lambda x: self.mediator_path + "\\" + x, self.fileNameList_source))

        # attribute for writing log
        self.toLog = {
            ic.L_MOVED:True
            , ic.L_DB_NAME:""
            , ic.L_SIZE:""
            , ic.L_SIZE_CHANGE:""
            , ic.L_RENAME:""
            , ic.L_DATE_STATUS:False
            , ic.L_DATE:""
            , ic.L_ZIPPED:False
            , ic.L_SUMMARY:False
        }
    @staticmethod
    def fileSizeChangeAverage(filePathList_source, filePathList_destination):
        sizeChangeList = []
        for index, fileSize_source in enumerate(filePathList_source):
            fileSize_destination = filePathList_destination[index]
            ratio = (fileSize_destination-fileSize_source)/fileSize_source
            percent = ratio*100
            sizeChangeList.append(percent)
        length = len(sizeChangeList)
        avg = sum(sizeChangeList)/length
        return avg

    @staticmethod
    def combinePath(dirPath, base):
        path = dirPath + "\\" + base
        return path

    @staticmethod
    def isEqual(list1, list2):
        """
        this method checks that each item in the same position is equal or not
        EX: list1 = [1,2,3,4], list2 = [1,2,3,4] isEqual => [True, True, True, True]
        :param list1:
        :param list2:
        :return: if all item in the same position is equal, so it'll return the list of boolean
        that each item in True or False corresponding to that each position is equal or not
        """
        sizeStatus = []
        for index, item1 in enumerate(list1):
            result = False
            item2 = list2[index]
            if item1 == item2:
                result = True
                sizeStatus.append(result)
            else:
                sizeStatus.append(result)
        return sizeStatus

    @staticmethod
    def allElementIsTrue(list1):
        """
        this method checks all elements in the list is true or not
        EX: list1 = [True, True, True] allElementIsTrue() => True
            list1 = [False, True, True] allElementIsTrue() => False
        :param list1:
        :return: True or False
        """
        result = True
        for item in list1:
            result = result and item
        return result

    def copyFromSourceToMediatorPath(self):
        # copy files from "source path" to "mediator path"
        result = True
        for filePath in self.filePathList_source:
            result = IFile.copyWithMetaData(filePath, self.mediator_path)
            result = result and result
            if result:
                pass
            else:
                return result
        return result

    def copyFromMediatorToDestinationPath(self):
        # copy files from "mediator path" to "destination path"
        result = True
        for index1, destinationPath in enumerate(self.destination_path):
            result = IFile.copyWithMetaData(self.filePathList_mediator[0], destinationPath)
            result = result and result
            if result:
                pass
            else:
                return result
        return result

class Infact(MoveFile):
    def __init__(self, dataDict : dict):
        super(Infact, self).__init__(dataDict=dataDict)

    def infact(self):
        result = self.copyFromSourceToMediatorPath()
        move_status = self.copyFromMediatorToDestinationPath()
        for index, destination in enumerate(self.destination_path):
            # # check that each destination needs "rename", "zip" or "password"
            hasToRename = IFile.parseToBoolean(self.has_to_rename_list[index])
            hasToZip = IFile.parseToBoolean(self.has_to_zip_list[index])
            hasToPassword = IFile.parseToBoolean(self.has_to_password_list[index])
            # # get the path of copied file at "destination path"
            filePathList_destination = [MoveFile.combinePath(destination, file) for file in self.fileNameList_source]
            # # get "file's size average"
            # # and check that each copied file has the same size as "source path" at "destination path"
            fileSizeList_destination = [IFile.getFileSize(filePath=filePath) for filePath in filePathList_destination]
            # check that each file at "source path" equals to "destination path"
            fileSizeList_isEqual = MoveFile.isEqual(self.fileSizeList_source, fileSizeList_destination)
            # check that all element is "true" means that all files are the same size as "source path"
            fileSize_status = MoveFile.allElementIsTrue(fileSizeList_isEqual)
            # get the file's size average
            fileSizeChangeAverage_status = MoveFile.fileSizeChangeAverage(self.fileSizeList_source, fileSizeList_destination)
            # # check that file's date is the same as "source path"
            fileDateList_destination = [IFile.getFileDate(filePath) for filePath in filePathList_destination]
            fileDateList_isEqual = MoveFile.isEqual(self.fileDateList_source, fileDateList_destination)
            fileDate_status = MoveFile.allElementIsTrue(fileDateList_isEqual)
            # # zip section
            if hasToZip:
                password = None
                if hasToPassword:
                    password = self.password_to_list[index]
                zip_status = IZipFile.toZipFile(self.dbName, filePathList_destination, password)
            else:
                zip_status = False
            # # rename section
            rename_status = False
            summary = move_status and fileSize_status and fileDate_status
            # # prepare date for writing to log
            self.toLog = {
                ic.L_MOVED: move_status
                , ic.L_DB_NAME: self.dbName
                , ic.L_SIZE: fileSize_status
                , ic.L_SIZE_CHANGE: fileSizeChangeAverage_status
                , ic.L_RENAME: "Done" if rename_status else "N/A"
                , ic.L_DATE_STATUS: "pass" if fileDate_status else "fail"
                , ic.L_DATE: fileDateList_isEqual[0]
                , ic.L_ZIPPED: "Done" if zip_status else "N/A"
                , ic.L_SUMMARY: "pass" if summary else "fail"
            }
            yield self.toLog

class InfactPassword(MoveFile):
    def __init__(self, dataDict: dict):
        super(InfactPassword, self).__init__(dataDict=dataDict)
    def infactPassword(self): pass

class Sff(MoveFile):
    def __init__(self, dataDict : dict):
        super(Sff, self).__init__(dataDict=dataDict)
    def sff(self): pass

class SffPassword(MoveFile):
    def __init__(self, dataDict: dict):
        super(SffPassword, self).__init__(dataDict=dataDict)
    def sffPassword(self): pass

class SffRename(MoveFile):
    def __init__(self, dataDict: dict):
        super(SffRename, self).__init__(dataDict=dataDict)
    def sffRename(self): pass

def main(pathExcel):
    # iterator
    # content = ic.IFile.readUserInputFile(pathExcel=pathExcel)
    for groupedByDbName in ic.IFile.readUserInputFile(pathExcel=pathExcel):
        fileType = groupedByDbName[ic.FILE_TYPE][0].lower()
        if fileType == INFACT:
           infact_test = Infact(groupedByDbName)

        elif fileType == INFACT_PASSWORD:
            infactPassword()
        elif fileType == SFF:
            sff()
        elif fileType == SFF_RENAME:
            sffRename()
        elif fileType == SFF_PASSWORD:
            sffPassword()
        else:
            pass



