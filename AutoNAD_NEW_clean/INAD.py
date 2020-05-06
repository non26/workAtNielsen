
class INAD:
    def _readConfiguration(self, path): pass
    def _readNADFile(self, pathFileNAD=None, sheetName=None): pass
    @staticmethod
    def _check_SALEVALUE(sv_trend, sv_nad):
        """checking SALE VALUE FROM TrendCheck File and NAD File"""
        sv_trend = abs(sv_trend)
        sv_nad = abs(sv_nad)
        if sv_trend == sv_nad:
            return True, 0
        else:
            return False, sv_trend - sv_nad
    @staticmethod
    def _check_ND(nd):
        """Checking ND selling"""
        if nd == 'nan':
            return False, 'NA'
        elif float(nd) >= 101:
            return False, 'EXCESS 100'
        else:
            return True, None
    @staticmethod
    def _check_WD(wd):
        """Checking WD selling"""
        if wd == 'nan':
            return False, 'NA'
        elif float(wd) >= 101:
            return False, 'EXCESS 100'
        else:
            return True, None
    @staticmethod
    def _roundDigitToWhole(number):
        str_number = str(number)
        digit = len(str_number[str_number.find(".") + 1:])
        for d in range(1, digit + 1):
            number = round(number, digit - d)
        return number
    def mainCompare(self): pass