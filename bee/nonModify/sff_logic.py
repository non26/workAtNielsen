import re
import zipfile
import distutils.dir_util
import distutils.file_util
import os
import xlsxwriter
import time
import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s-%(message)s")
class ParentSFF():
    month_dict = {1: "JAN", 2: "FEB", 3: "MAR", 4: "APR", 5: "MAY", 6: "JUNE", 7: "JULY", 8: "AUG", 9: "SEP", 10: "OCT",
                  11: "NOV", 12: "DEC"}
    def __init__(self, flag, pathZipFile=None, pathtxtFile=None, userMonth=None, userWeek=None, userYear=None):
        """
        1.This class will copy
        N:\Rf3db\Rtdb\Chain\Big C\SFF\Weekly for week
        N:\Rf3db\Rtdb\Chain\Big C\SFF\Monthly for month
        that stay on the 'shared drive' to the 'Local' of users where this script located
        , after copying to Local and check the pattern in the txt files
        , all files in the local will be removed.
        2.methods that prefix with the single underscore mean that for internal use.

        :param flag: can either 'week' or 'month'
        :param pathZipFile: path of zip files at the shared drive
        :param pathtxtFile: path of extracted txt files at the shared drive
        :param userMonth:
        :param userWeek:
        :param userYear:
        """
        self.flag = flag
        self.pathSharedDriveFolderZipFileSFF = pathZipFile
        self.pathSharedDriveFolderTxtFile = pathtxtFile
        # os.path.abspath(__file__) this code tells us that keep the copied to where this file located.
        self.pathLocalFolderSFF = os.path.dirname(os.path.abspath(__file__)) + "\\" + f"sim2localZipFile{flag.upper()}"
        self.pathLocalFolderForTxt = os.path.dirname(os.path.abspath(__file__)) + "\\" + f"ForExtract_file_{flag.lower()}ly"
        self.month = userMonth # string object
        self.week = userWeek # string object
        self.year = userYear.rstrip() # string object
        if userMonth == "1":
            self.yearChange = str(int(userYear) - 1)
        else:
            self.yearChange = userYear.rstrip()
        self.worksheet = None
        self.workbook = None
        # *****
        if self.flag.lower() == "week": # check that flag is week or not
            self.txt_pattern = r"LAST_PERIOD[\s:]+WEEKLY[\s-]*(W[0-9]*)"
            if len(self.week) == 1:
                self.user_pattern = f"W0{self.week}{self.yearChange[-2:]}"
            else:
                self.user_pattern = f"W{self.week}{self.yearChange[-2:]}"
        else: # else, it's month
            if self.month == '1':
                checked_month = ParentSFF.month_dict[12]
            else:
                checked_month = ParentSFF.month_dict[int(self.month)-1]
            self.user_pattern = f"{checked_month}{self.yearChange[-2:]}"
            self.txt_pattern = r"LAST_PERIOD[\s:]+MONTH[\s-]*([a-zA-Z0-9]*)"
        # *****
        self._conn2Excel(flag=self.flag)
        # create folder for the extracted txt files at Shared Drive
        ParentSFF._createFolder(self.pathSharedDriveFolderTxtFile)
        # create the folder at Local for the copied SFF from Shared Drive
        ParentSFF._createFolder(self.pathLocalFolderSFF)
        # create folder for the extracted txt files
        ParentSFF._createFolder(self.pathLocalFolderForTxt)

    def _conn2Excel(self, flag):
        month = ParentSFF.month_dict[int(self.month)]
        logging.debug(f"connecting to file SFF_Summary_month_{month}_{flag.upper()}LY.xlsx")
        self.workbook = xlsxwriter.Workbook(
            os.path.dirname(self.pathSharedDriveFolderZipFileSFF) +
            "\\" + f"SFF_Summary_month_{month}_{flag.upper()}LY.xlsx"
        )
        logging.debug(f"connecting to the SUMMARY_SFF_File({flag.lower()}ly) worksheet")
        self.worksheet = self.workbook.add_worksheet(f'SUMMARY_SFF_File({flag.lower()}ly)')
        cell_format = self.workbook.add_format()
        cell_format.set_pattern(1)  # This is optional when using a solid fill.
        cell_format.set_bg_color('pink')
        # set cell width
        self.worksheet.set_column(1, 1, 10)
        self.worksheet.set_column(2, 3, 40)
        self.worksheet.write('A1', 'Status', cell_format)
        self.worksheet.write('B1', 'FileName', cell_format)
        self.worksheet.write('C1', 'Path', cell_format)
        self.worksheet.write('D1', "folder", cell_format)
        self.worksheet.write('E1', "No. file", cell_format)
        self.worksheet.write('F1', "txt period", cell_format)

    @staticmethod
    def _createFolder(path_directory):
        logging.debug(f"creating {path_directory} folder")
        try:
            if not os.path.exists(path_directory):

                os.makedirs(path_directory)
            else:
                distutils.dir_util.remove_tree(path_directory)
                os.makedirs(path_directory)
        except OSError: pass # # waiting for update
        logging.debug("finished creating folder")

    def _copyZipFileToLocal(self):
        logging.debug("copying SFF files from shared drive to local")
        distutils.dir_util.copy_tree(self.pathSharedDriveFolderZipFileSFF, self.pathLocalFolderSFF)
        logging.debug("finished copying to local")

    @staticmethod
    def _removeFolder(path_directory):
        logging.debug(f"removing {path_directory} folder")
        try:
            if os.path.exists(path_directory):
                distutils.dir_util.remove_tree(path_directory)
            else: pass
        except Exception: pass # # waiting for update
        logging.debug("finished removing folder")
    def _write2Excel(self, rowExcel, **kwargs):
        self.worksheet.write(rowExcel, 0, kwargs["status"])
        self.worksheet.write(rowExcel, 1, kwargs["filetxtName"])
        # hyperlink
        self.worksheet.write_url(f"C{rowExcel+1}", kwargs["pathHyper"],
                                 string="check here")
        self.worksheet.write(rowExcel, 3, kwargs["zipFileName"])
        self.worksheet.write(rowExcel, 4, kwargs["cnt"])
        self.worksheet.write(rowExcel, 5, kwargs["txtPattern"])


    def getFile(self):
        start = time.time()
        self._copyZipFileToLocal()
        filetxt = None # a txt file object
        row_excel = 1 # row_excel
        logging.debug(f"we're at local:{self.pathLocalFolderSFF}")
        # os.scandir() return all objects in the directory
        for index, entry in enumerate(os.scandir(self.pathLocalFolderSFF)):
            # check that which object is the zip file.
            if entry.name.endswith('ZIP') and entry.is_file():
                logging.debug(f"{' '*10}Zip file's name {entry.name}")
                zipFileName = entry.name # zip file's name
                pathForUnzip = f"{self.pathLocalFolderSFF}\\{zipFileName}" # path of that zip file
                logging.debug(f"{' '*10}Zip file's path {pathForUnzip}")
                with zipfile.ZipFile(pathForUnzip) as zfiles: # open that zip file by creating zip file object "zfiles"
                    logging.debug(f"{' ' * 15} into Zip file's path ")
                    # get all files of open zip file by "ZipObject.infolist()"
                    for file in zfiles.infolist():
                        if file.filename.endswith(".txt"):
                            logging.debug(f"{' ' * 20} txt member: {file.filename}")
                            filetxt = file # assign fileTxt to file object
                            break
                    cnt = len(zfiles.infolist()) # number of files in file object
                    filetxtName = filetxt.filename # file's name in string
                    txtModi_month = str(filetxt.date_time[1]) # last modified for month
                    txtModi_year = str(filetxt.date_time[0]) # last modified for week
                    logging.debug(f"{' ' * 15} modi-month:{txtModi_month}, mod-year:{txtModi_year}")
                    logging.debug(f"{' ' * 15} user-month:{self.month}, user-year:{self.year}")
                    # check that user's input and last modified of txt file is matched or not
                    if txtModi_month == self.month and txtModi_year == self.year:
                        logging.debug(f"{' '*20} extracting txt to {self.pathLocalFolderForTxt}")
                        # extract that txt file of that zip file to self.pathLocalFolderForTxt located in local
                        zfiles.extract(filetxtName, self.pathLocalFolderForTxt)
                        # create a path of that txt file located in self.pathLocalFolderForTxt
                        pathLocalTxtFile = self.pathLocalFolderForTxt + "\\" + filetxtName
                        logging.debug(f"{' '*20} path file txt at local {pathLocalTxtFile}")
                        status = "" # checking status, pass or fail
                        with open(pathLocalTxtFile) as txtFile:
                            # make all the texts in the file into one long string without space
                            stringContent = "".join("".join(txtFile.readlines()).split("\n"))
                            compileObj = re.compile(self.txt_pattern)
                            searchObj = compileObj.search(stringContent)
                            try:
                                # fetch that pattern out of the Txt file
                                txtPattern = searchObj.group(1)
                                logging.debug(f"{' '*25} need to check: {txtPattern}")
                            except Exception: pass # # waiting for update
                            # check that the Txt pattern is matched with user pattern
                            if txtPattern == self.user_pattern:
                                status = "Pass"
                            elif txtPattern.endswith(f"{self.year[-2:]}"):
                                status = "Fail"
                            # copy that txt file to the shared drive
                            distutils.file_util.copy_file(pathLocalTxtFile, self.pathSharedDriveFolderTxtFile)
                            pathHyper = self.pathSharedDriveFolderTxtFile + "\\" + filetxtName
                            self._write2Excel(row_excel
                                              , status=status
                                              , filetxtName=filetxtName
                                              , pathHyper=pathHyper
                                              , zipFileName=zipFileName
                                              , cnt=cnt
                                              , txtPattern=txtPattern
                                              )
                            row_excel += 1
                    # # waiting for update
                    else: pass # means it doesn't match then pass
        self.workbook.close()
        # remove all folders that's generating on Local
        ParentSFF._removeFolder(self.pathLocalFolderForTxt)
        ParentSFF._removeFolder(self.pathLocalFolderSFF)
        print(f"{self.flag}:",time.time()-start)



















