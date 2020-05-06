from PyNielsen.bee.nonModify import sff_logic as sff
import time
class test_sff(sff.ParentSFF):
    def __init__(self, flag, pathSFF_sd, pathTxt_sd, month, week, year):
        sff.ParentSFF.__init__(self, flag, pathZipFile=pathSFF_sd, pathtxtFile=pathTxt_sd
                               , userMonth=month, userWeek=week, userYear=year)

if __name__ == "__main__":
    w = test_sff("week"
                 , pathSFF_sd=r"N:\Rf3db\Rtdb\Chain\Big C\SFF\Weekly"
                 , pathTxt_sd=r"N:\Rf3db\Rtdb\Chain\Big C\SFF\ForExtract_file_weekly"
                 , month="1", week="52", year="2020")
    sum_time_week = []
    for _ in range(5):
        start = time.time()
        w.getFile()
        elapsed = time.time()-start
        print("week:", elapsed)
        sum_time_week.append(elapsed)
    print("avg week", sum(sum_time_week)/5)
    m = test_sff("month"
                 , pathSFF_sd=r"N:\Rf3db\Rtdb\Chain\Big C\SFF\Monthly"
                 , pathTxt_sd=r"N:\Rf3db\Rtdb\Chain\Big C\SFF\ForExtract_file_monthly"
                 , month="1", week="52", year="2020")
    sum_time_month = []
    for _ in range(5):
        start = time.time()
        w.getFile()
        elapsed = time.time() - start
        print("month:", elapsed)
        sum_time_month.append(elapsed)
    print("avg month", sum(sum_time_month) / 5)








