import tkinter as tk
import threading
# import os
from workAtNielsen.projectAtNielsen.bee.nonModify import sff_logic as sff, popUp_taskWithoutRootWD as popUp


# for Nielsen's CP
# from PyNielsen.fromGithub.bee.SFF.nonModify import sff_logic as sff
# from PyNielsen.fromGithub.bee.SFF.nonModify import popUp_taskWithoutRootWD as popUp
# class AutoOpening_SFF(tk.Tk): 1
class AutoOpening_SFF():
    def __init__(self, master):
        # tk.Tk.__init__(self) 1
        self.master = master
        self.master.geometry("300x200")
        self.week = tk.StringVar()
        self.month = tk.StringVar()
        self.year = tk.StringVar()
        self.thread1 = None
        #
        self.sff_path_week = r"N:\Rf3db\Rtdb\Chain\Big C\SFF\Weekly"
        self.sff_path_month = r"N:\Rf3db\Rtdb\Chain\Big C\SFF\Monthly"
        self.extracted_txt_month = r"N:\Rf3db\Rtdb\Chain\Big C\SFF\ForExtract_file_monthly"
        self.extracted_txt_week = r"N:\Rf3db\Rtdb\Chain\Big C\SFF\ForExtract_file_weekly"
        # week
        self.weekInfo_label = tk.Label(self.master, text="input week", fg="black")
        self.weekInfo_label.grid(row=1, column=0, padx=(10, 0), pady=(0, 20), sticky='w')
        self.textentryweek_entry = tk.Entry(self.master, width=20, bg="white", textvariable=self.week)
        self.textentryweek_entry.grid(row=1, column=2, padx=(10, 0), pady=(0, 20), sticky='E')
        tk.Label(self.master, text="EX week: 9").grid(row=1, column=3)
        # month
        self.monthInfo_label = tk.Label(self.master, text="Input month", fg="black")
        self.monthInfo_label.grid(row=2, column=0, padx=(10, 0), pady=(0, 20), sticky='w')
        self.textentrymonth_entry = tk.Entry(self.master, width=20, bg="white", textvariable=self.month)
        self.textentrymonth_entry.grid(row=2, column=2, padx=(10, 0), pady=(0, 20), sticky='E')
        tk.Label(self.master, text="EX month: 3").grid(row=2, column=3)
        # year
        self.yearInfo_label = tk.Label(self.master, text="Input year", fg="black")
        self.yearInfo_label.grid(row=3, column=0, padx=(10, 0), pady=(0, 20), sticky='w')
        self.textentryyear_entry = tk.Entry(self.master, width=20, bg="white", textvariable=self.year)
        self.textentryyear_entry.grid(row=3, column=2, padx=(10, 0), pady=(0, 20), sticky='E')
        tk.Label(self.master, text="EX year: 2020").grid(row=3, column=3)
        # week/month button
        self.week_button = tk.Button(self.master, text="Weekly", width=6, command=self.click_week)
        self.week_button.grid(row=4, column=0, padx=(5, 0), sticky='w')
        self.month_button = tk.Button(self.master, text="Monthly", width=6, command=self.click_month)
        self.month_button.grid(row=4, column=2, padx=(5, 0), sticky='w')

    def click_week(self):
        # entry value
        w = sff.ParentSFF(flag='week', pathZipFile=self.sff_path_week, pathtxtFile=self.extracted_txt_week
                      , userMonth=self.month.get(), userWeek=self.week.get()
                      , userYear=self.year.get())
        self.thread1 = threading.Thread(target=w.getFile)
        self.thread1.start()
        self._showCompletionTask()
        # w.getFile()

    def click_month(self):
        # entry value
        m = sff.ParentSFF(flag="month", pathZipFile=self.sff_path_month, pathtxtFile=self.extracted_txt_month
                      , userWeek=self.week.get(), userMonth=self.month.get()
                      , userYear=self.year.get())
        self.thread1 = threading.Thread(target=m.getFile)
        self.thread1.start()
        self._showCompletionTask()
        # m.getFile()

    def _showCompletionTask(self):
        if self.thread1.is_alive():
            self.master.after(1000, self._showCompletionTask)
        else:
            popUp.alert_popUp("SFF", "Finished!")

if __name__ == "__main__":
    master = tk.Tk()
    test = AutoOpening_SFF(master)
    master.mainloop()