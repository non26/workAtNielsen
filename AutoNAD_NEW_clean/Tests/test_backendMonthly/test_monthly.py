# from ...BackEnd_Monthly import monthly_class_revamped
from workAtNielsen.projectAtNielsen.AutoNAD_NEW_clean.BackEnd_Monthly import monthly_class_revamped
import unittest

class Test_Monthly(unittest.TestCase):
    def test_classMonthly__getReportName(self):
        # Arrange
        # fake file name
        fileNADName1 = "RTDTEA_HABU-TCCCRTTH.xlsx"
        fileNADName2 = "SNA_SEAW-RM93800.xlsx"
        fileNADName3 = "SAUCE-RM00810.xlsx"
        expected1 = "TCCCRTTH"
        expected2 = "RM93800"
        expected3 = "RM00810"
        test = monthly_class_revamped.Monthly()
        # Act
        actual1 = test._getReportName(fileNADName1)
        actual2 = test._getReportName(fileNADName2)
        actual3 = test._getReportName(fileNADName3)
        # Assert
        self.assertEqual(expected1, actual1)
        self.assertEqual(expected2, actual2)
        self.assertEqual(expected3, actual3)

    def test_classMonthly__findFactWithStockWord(self):
        # Arrange
        columns = [
                    "Sales Volume(Tsd.Units)"
                    , "Sales Volume(KG)"
                    , "Sales Value(Tsd.Baht)"
                    , "Price Per Pack"
                    , "Purchase (Tsd.Units)"
                    , "Purchase (KG)"
                    , "Forward Stock (Tsd.Units)"
                    , "Forward Stock (KG)"
                    , "Reserved Stock (Tsd.Units)"
                    , "Reserved Stock (KG)"
                    , "ND In - Stock"
                    , "WD In- Stock"
                    , "ND Out -Stock"
                    , "WD Out-Stock"
                    , "ND Selling"
                    , "WD Selling"
        ]
        expected = [
              "ND In - Stock"
            , "WD In- Stock"
            , "ND Out -Stock"
            , "WD Out-Stock"
        ]
        expected.sort()
        # Act
        actual = []
        actual_iterator = monthly_class_revamped.Monthly._findFactWithStockWord(columns)
        for column in actual_iterator:
            actual.append(column)
        actual.sort()
        # Assert
        self.assertEqual(expected, actual)

    def test_classMonthly__findMBDCode(self):
        # Arrange
        mbdCode1 = "M00AAA1"
        mbdCode2 = "AD111"
        mbdCode3 = "M00AA1"
        expected1 = "AAA1"
        expected2 = "AD111"
        expected3 = 'AA1'
        # Act
        actual1 = monthly_class_revamped.Monthly._findMBDCode(mbdCode1)
        actual2 = monthly_class_revamped.Monthly._findMBDCode(mbdCode2)
        actual3 = monthly_class_revamped.Monthly._findMBDCode(mbdCode3)
        # Assert
        self.assertEqual(expected1, actual1)
        self.assertEqual(expected2, actual2)
        self.assertEqual(expected3, actual3)

    def test_classMonthly__findHiddenFact(self):
        # Arrange
        expected = [
             "Purchase (Tsd.Units)"
            , "Purchase (KG)"
            , "Forward Stock (Tsd.Units)"
            , "Forward Stock (KG)"
            , "Reserved Stock (Tsd.Units)"
            , "Reserved Stock (KG)"
        ]
        expected.sort()
        # fileNAD = "BREK_CER-RM05830.xlsx"
        columnsName =[
                    "Sales Volume(Tsd.Units)"
                    , "Sales Volume(KG)"
                    , "Sales Value(Tsd.Baht)"
                    , "Price Per Pack"
                    , "Purchase (Tsd.Units)"
                    , "Purchase (KG)"
                    , "Forward Stock (Tsd.Units)"
                    , "Forward Stock (KG)"
                    , "Reserved Stock (Tsd.Units)"
                    , "Reserved Stock (KG)"
                    , "ND In-Stock"
                    , "WD In-Stock"
                    , "ND Out-Stock"
                    , "WD Out-Stock"
                    , "ND Selling"
                    , "WD Selling"
        ]
        test = monthly_class_revamped.Monthly()
        # Act
        actual_iterator = test._findHiddenFact(colName=columnsName)
        actual = []
        for item in actual_iterator:
            actual.append(item)
        actual.sort()
        # Assert
        self.assertEqual(expected, actual)

    def test_classMonthly__skipRowNull(self):
        # Arrange
        # fileNAD = "BREK_CER-RM05830.xlsx"
        fileNAD = r"C:\nonContent\workAtNielsen\projectAtNielsen\formatNAD_afterLeave1\CANDY-RM04400.xlsx"
        expected = 3
        test = monthly_class_revamped.Monthly()
        # Act
        actual = test._skipRowNull(fileNAD)
        # Assert
        self.assertEqual(expected, actual)

    def test_classMonthly__findHiddenMBD(self):
        # Arrange
        expected = [
                 "Total Thailand+MTSR"
                , "Greater Bangkok+MTSR"
                , "Central+MTSR"
                , "North+MTSR"
                , "Northeast+MTSR"
                , "South+MTSR"
                , "Super/Hypermarket+MTSR"
                , "Super/Hypermarket (Gbkk.)+MTSR"
                , "Super/Hypermarket (Upc.)+MTSR"
                , "Super/Hypermarket Chain"
                , "Local Supermarket + MTSR"
                , "Convenience"
                , "Convenience (Gbkk.)"
                , "Convenience  (Upc.)"
                , "Modern Trade+MTSR"
                , "Modern Trade (GBKK)+MTSR"
                , "Modern Trade (UPC)+MTSR"
        ]
        mbd = [
            "Total Thailand+MTSR"
            , "Greater Bangkok+MTSR"
            , "Central+MTSR"
            , "North+MTSR"
            , "Northeast+MTSR"
            , "South+MTSR"
            , "Super/Hypermarket+MTSR"
            , "Super/Hypermarket (Gbkk.)+MTSR"
            , "Super/Hypermarket (Upc.)+MTSR"
            , "Super/Hypermarket Chain"
            , "Local Supermarket + MTSR"
            , "Convenience"
            , "Convenience (Gbkk.)"
            , "Convenience  (Upc.)"
            , "Open Trade"
            , "Open Trade (Urban)"
            , "Open Trade (Rural)"
            , "Licensed Pharmacy"
            , "Modern Trade+MTSR"
            , "Modern Trade (GBKK)+MTSR"
            , "Modern Trade (UPC)+MTSR"
            , "Traditional Trade"
        ]
        mbdCode = [
             "M00AAA1"
            , "M00ABA1"
            , "M00ABB1"
            , "M00ABC1"
            , "M00ABD1"
            , "M00ABE1"
            , "M00AGA1"
            , "M00AGB1"
            , "M00AGG1"
            , "M00GC0"
            , "M00AGD0"
            , "M00HA1"
            , "M00HB1"
            , "M00HG1"
            , "M00IA1"
            , "M00IH1"
            , "M00II1"
            , "M00JA1"
            , "M00AMA1"
            , "M00AMB1"
            , "M00AMG1"
            , "M00NA1"
        ]
        test = monthly_class_revamped.Monthly()
        expected.sort()
        # Act
        actual_iterator = test._findHiddenMBD(mbd=mbd, mbdCode=mbdCode)
        actual = []
        for item in actual_iterator:
            actual.append(item)
        actual.sort()
        # Assert
        self.assertEqual(expected, actual)

    def test_classMonthly__readNADFile(self):
        # Arrange
        fileNAD = r"C:\nonContent\workAtNielsen\projectAtNielsen\formatNAD_afterLeave1\CANDY-RM04400.xlsx"
        expected_largeMBD = "Total Thailand"
        expected_largeMBDCode = "M00AA1"
        expected_value = {
            expected_largeMBD: {
                "Sales Value (Tsd.Baht)": 41458
                , "ND Selling": 92
                , "WD Selling": 100
            }
            , "row": 0
            , "column":{
                "Sales Value (Tsd.Baht)": 4
                , "ND Selling": 16
                , "WD Selling": 17
            }
        }
        test = monthly_class_revamped.Monthly()
        # Act
        actual_value, actual_largeMBD, actual_largeMBDCode = test._readNADFile(fileNAD=fileNAD)
        # Assert
        self.assertEqual(expected_value, actual_value)
        self.assertEqual(expected_largeMBD, actual_largeMBD)
        self.assertEqual(expected_largeMBDCode, actual_largeMBDCode)

    def test_classMonthly__readTrendFileAA1_AAA1_at_AAA1(self):
        # Arrange
        mbdCode = "M00AAA1"
        fileNADName = r"C:\nonContent\workAtNielsen\AutoNAD_NEW_clean\Tests\test_backendMonthly\BREK_CER-RM05830.xlsx"
        fileTrendPath = "TrendCheck W01-04_20 _Jan_20.xlsx"
        test = monthly_class_revamped.Monthly()
        test.pathFileTrend = fileTrendPath
        expected = {
            'SALESVALUE':[
                256876
            ]
        }
        # Act
        actual = test._readTrendFileAA1_AAA1(fileNAD=fileNADName, MBDCode=mbdCode)
        # Assert
        self.assertEqual(expected, actual)

    def test_classMonthly__checkingSALESVALUEAA1_AAA1_at_AAA1(self):
        # Arrange
        svFromNAD1 = 123456
        svFromNAD2 = -123456
        svFromNAD3 = 214365
        svFromNAD4 = 56467
        svfromTrend1 = {'SALESVALUE':[1234567, 34567, 43226, -123456]}
        svfromTrend2 = {'SALESVALUE':[1234567, 34567, 43226, -123456]}
        svfromTrend3 = {'SALESVALUE':[1234567, 34567, 214365, -1234562]}
        svfromTrend4 = {'SALESVALUE':[1234567, 34567, 214365, -1234562]}
        test = monthly_class_revamped.Monthly()
        # Act
        actual1 = test._checkingSALESVALUEAA1_AAA1(svFromNAD1, svfromTrend1)
        actual2 = test._checkingSALESVALUEAA1_AAA1(svFromNAD2, svfromTrend2)
        actual3 = test._checkingSALESVALUEAA1_AAA1(svFromNAD3, svfromTrend3)
        actual4 = test._checkingSALESVALUEAA1_AAA1(svFromNAD4, svfromTrend4)
        # Assert
        self.assertTrue(actual1)
        self.assertTrue(actual2)
        self.assertTrue(actual3)
        self.assertFalse(actual4)

    def test_classMonthly__checkingHiddenMBD_noLog(self):
        # Arrange
        fileNAD = "BREK_CER-RM05830.xlsx"
        test = monthly_class_revamped.Monthly()
        test._readNADFile(fileNAD=fileNAD)
        expected = {
            "log":[]
            , "mark":[]
            , "rowth":test.skipRow
        }
        # Act
        actual = test._checkingHiddenMBDAndFACT(pathFileNAD=fileNAD)
        # Assert
        self.assertEqual(expected, actual)

    def test_classMonthly__checkingHiddenMBD_withLog(self): pass
    def test_classMonthly__readConfiguration(self): pass
    def test_classMonthly__readTrendFileAA1_AAA1_at_AA1(self): pass
    def test_classMonthly__readTrendFileAll(self): pass
    def test_classMonthly__checkingSALESVALUEAA1_AAA1_at_AA1(self): pass
    def test_classMonthly_mainCompare(self): pass

def runTest_Test_Monthly():
    unittest.main(__name__)
if __name__ == "__main__":
    unittest.main()
