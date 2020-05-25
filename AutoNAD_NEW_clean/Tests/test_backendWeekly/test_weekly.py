import unittest
# from ...BackEnd_Weekly import weekly_class_revamped
from workAtNielsen.projectAtNielsen.AutoNAD_NEW_clean.BackEnd_Weekly import weekly_class_revamped
# from BackEnd_Weekly import weekly_class_revamped
import  pandas as pd
class Test_Weekly(unittest.TestCase):
    # pathFileTrend = r"C:\nonContent\workAtNielsen\paralle\TrendCheck W05-09_20 _Feb_20 .xlsx"
    pathFileTrend = r"C:\nonContent\workAtNielsen\paralle\TrendCheck W13-17_20 _Feb_20 .xlsx"
    fileNAD = "BIRD_NET-ST04900.xlsx"

    def test_findWeek(self):
        # Arrange
        # pathFileTrend = r"TrendCheck W05-09_20 _Feb_20 .xlsx"
        expected = "05-09-2020"
        # Act
        actual = weekly_class_revamped.findWeek(fileTrendPath=Test_Weekly.pathFileTrend)
        # Assert
        self.assertEqual(expected, actual)

    def test_formatWeek(self):
        # Arrange
        weekth = "05-09-2020"
        expexted = ["W0520", "W0620", "W0720", "W0820", "W0920"]
        # Act
        actual = weekly_class_revamped.formatWeek(weekth)
        # Assert
        self.assertEqual(expexted, actual)

    def test_weekClass_skipRowNull(self):
        # Arrange
        # fileNAD = "BIRD_NET-ST04900.xlsx"
        expected = 3
        # Act
        actual = weekly_class_revamped.Weekly._skipRowNull(
            pathNadFile=Test_Weekly.fileNAD, checkColumn=2)
        # Assert
        self.assertEqual(expected, actual)

    def test_weekClass_skipRowNotNull(self):
        # Arrange
        # fileNAD = "BIRD_NET-ST04900.xlsx"
        expected = 31
        # Act
        rowNull = weekly_class_revamped.Weekly._skipRowNull(
            pathNadFile=Test_Weekly.fileNAD, checkColumn=2)
        actual = weekly_class_revamped.Weekly._skipRowNotNull(
            pathNadFile=Test_Weekly.fileNAD, checkColumn=2, startRow=rowNull)
        # Assert
        self.assertEqual(expected, actual)

    def test_weekClass_rowToWantedTable(self):
        # Arrange
        # fileNAD = "BIRD_NET-ST04900.xlsx"
        expected = 35
        # Act
        actual = weekly_class_revamped.Weekly._rowToWantedTable(pathFileNAD=Test_Weekly.fileNAD)
        # Assert
        self.assertEqual(expected, actual)

    def test_weekClass_readConfiguration(self): pass

    def test_weekClass_readNADFile(self):
        # Arrange
        # fileNAD = "BIRD_NET-ST04900.xlsx"
        expected_large_mbd = "Tops Total"
        expected_need2Check = {"Tops Total":{
            "W1320":{
                "Sales Value (Baht)":1194337,
                "ND Selling":10357,
                "WD Selling":12893
            },
            "W1420":{
                "Sales Value (Baht)":3606895,
                "ND Selling":2301,
                "WD Selling":1751
            },
            "W1520": {
                "Sales Value (Baht)": 3637297,
                "ND Selling": 18680,
                "WD Selling": 2767
            },
            "W1620": {
                "Sales Value (Baht)": 1591954,
                "ND Selling": 13056,
                "WD Selling": 8211
            },
            "W1720": {
                "Sales Value (Baht)": 2498801,
                "ND Selling": 2970,
                "WD Selling": 12071
            },
        },
        "column":{
            "Sales Value (Baht)":4,
            "ND Selling": 5,
            "WD Selling": 6
        },
        "row":{
            "W1320":5,
            "W1420":6,
            "W1520":7,
            "W1620":8,
            "W1720":9
        }
    }
        # pathFileTrend = r"C:\nonContent\workAtNielsen\paralle\TrendCheck W05-09_20 _Feb_20.xlsx"
        weekth = weekly_class_revamped.findWeek(fileTrendPath=Test_Weekly.pathFileTrend)
        # Act
        test = weekly_class_revamped.Weekly(selectedService=None, conclude=None, weekth=weekth)
        actual_need2Check, actual_large_mbd = test._readNADFile(pathFileNAD=Test_Weekly.fileNAD)
        # Assert
        self.assertEqual(expected_need2Check, actual_need2Check)
        self.assertEqual(expected_large_mbd, actual_large_mbd)

    def test_weekClass_readTrendFile(self):
        # Arrange
        # pathFileTrend = r"TrendCheck W05-09_20 _Feb_20 .xlsx"
        sheetName = "KAD Tops"
        expected_dataFrame = pd.DataFrame(pd.read_excel(("test_trendcheck_KADTops.xlsx")))
        weekly = "05-09-2020"
        test_actual = weekly_class_revamped.Weekly(selectedService=None, conclude=None, weekth=weekly)
        test_actual.pathFileTrend = Test_Weekly.pathFileTrend
        # Act
        actual_dataFrame = test_actual._readTrendFile(sheetName=sheetName)
        actual_equal = expected_dataFrame.equals(actual_dataFrame)
        # Assert
        self.assertTrue(actual_equal)

    def test_weekClass_valueFromFileTrend(self):
        # Arrange
        dbName = "ST04900"
        sheetName = "KAD Tops"
        # pathFileTrend = r"TrendCheck W05-09_20 _Feb_20 .xlsx"
        weekly = "05-09-2020"
        expected = {
            "ST04900":{
                "W0520": 4785330.863751509,
                "W0620": 3973853.921604303,
                "W0720": 3744036.7575683827,
                "W0820": 3933200.402389045,
                "W0920": 4084410.3660577363
            }
        }
        test_actual = weekly_class_revamped.Weekly(selectedService=None, conclude=None, weekth=weekly)
        test_actual.pathFileTrend = Test_Weekly.pathFileTrend
        # Act
        actual = test_actual._valueFromFileTrend(sheet=sheetName, dbName=dbName)
        # Assert
        self.assertEqual(expected, actual)

def runtest_TestWeekly():
    unittest.main(module=__name__)
if __name__ == "__main__":
    unittest.main()








