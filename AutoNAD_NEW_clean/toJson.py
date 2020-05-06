import json
from json.decoder import JSONDecodeError
import pandas as pd
import numpy as np
import os


class MBDToJson():
    """This class is used for extract data for monthly with two columns
    -first: MBD
    -second: MBDCode
    """

    def __init__(self, pathJson=None):
        self.jsonFile = pathJson
        self.read_json()

    @property
    def pathJson(self):
        return self.jsonFile

    @pathJson.setter
    def pathJson(self, another):
        self.jsonFile = another

    @pathJson.deleter
    def pathJson(self):
        del self.jsonFile

    def read_json(self):
        self.dict_mbd = {}  # a pair of key:value , that is MBD:MBDCode
        with open(self.jsonFile, "r") as outfile:
            try:
                self.dict_mbd = json.load(outfile)
            except JSONDecodeError:  # check whether that Json's content is empty or not.
                pass

    def updateFromExcel(self, pathFile=None):
        """

        :param pathFile:
        :return:
        """
        df = pd.DataFrame(pd.read_excel(pathFile))
        with open(self.jsonFile, "w") as infile:
            for index in range(len(df)):
                self.dict_mbd[df.iloc[index, 0]] = df.iloc[index, 1]
            json.dump(self.dict_mbd, infile)

    def update(self):
        with open(self.jsonFile, "w") as infile:
            json.dump(self.dict_mbd, infile)

    def set_MBD(self, MBD=None, MBDCode=None):
        """

        :param MBD: Tuple of MBDs
        :param MBDCode: Tuple of the corresponding MBDCode
        :param delete: for specify that there's element need to be deleted
        :return:
        """
        for index, mbd in enumerate(MBD):
            self.dict_mbd[mbd] = MBDCode[index]
        self.update()

    def delete(self, MBD_delete=None):
        """

        :param MBD_delete:
        :return:
        """
        MBD = tuple(self.dict_mbd.keys())
        for item in MBD_delete:
            if item not in MBD:
                pass
            else:
                del self.dict_mbd[item]
        self.update()

    def showHidden(self):
        if not self.dict_mbd:
            print("pass")
        else:
            mbd = list(self.dict_mbd.keys())
            fact= list(self.dict_mbd.values())
            for index, keyMBD in enumerate(mbd):
                print(keyMBD.ljust(50), fact[index].ljust(20))
if __name__=="__main__":
    jsonObj = MBDToJson(pathJson=r"C:\Users\EiCh9001\PycharmProjects\PyNielsen\AutomateNAD\AutoNAD\MBD.json")
    jsonObj.showHidden()
    jsonObj.delete(("N", "T"))
    jsonObj.showHidden()
    jsonObj.delete(["Non"])
