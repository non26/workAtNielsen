import tkinter as tk
import queue as q
import os
import zipfile
import xlsxwriter
class AotoOpening_SFF(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.sff_path_week = r"N:\Rf3db\Rtdb\Chain\Big C\SFF\Weekly"
        self.sff_path_month = r"N:\Rf3db\Rtdb\Chain\Big C\SFF\Monthly"
        self.extract_txt_month = r"N:\Rf3db\Rtdb\Chain\Big C\SFF\ForExtract_file_monthly"
        self.extract_txt_week = r"N:\Rf3db\Rtdb\Chain\Big C\SFF\ForExtract_file_weekly"
        self.createFolder(directory=self.extract_txt_week)
        self.createFolder(directory=)
        # week
        self.weekInfo_label = tk.Label(self, text="input week", fg="black")
        self.weekInfo_label.grid(row=1, column=0, padx=(10, 0), pady=(0, 20), sticky='w')
        self.textentryweek_entry = tk.Entry(self, width=20, bg="white")
        self.textentryweek_entry.grid(row=1, column=2, padx=(10, 0), pady=(0, 20), sticky='E')
        # month
        self.monthInfo_label = tk.Label(self, text="Input month", fg="black")
        self.monthInfo_label.grid(row=2, column=0, padx=(10, 0), pady=(0, 20), sticky='w')
        self.textentrymonth_entry = tk.Entry(self, width=20, bg="white")
        self.textentrymonth_entry.grid(row=2, column=2, padx=(10, 0), pady=(0, 20), sticky='E')
        # yeear
        self.yearInfo_label = tk.Label(self, text="Input year", fg="black")
        self.yearInfo_label.grid(row=3, column=0, padx=(10, 0), pady=(0, 20), sticky='w')
        self.textentryyear_entry = tk.Entry(self, width=20, bg="white")
        self.textentryyear_entry.grid(row=3, column=2, padx=(10, 0), pady=(0, 20), sticky='E')
        # week/month button
        self.week_button = tk.Button(self, text="Weekly", width=6, command=self.click1_week)
        self.week_button.grid(row=4, column=0, padx=(5, 0), sticky='w')
        self.month_button = tk.Button(self, text="Monthly", width=6, command=click2)
        self.month_button.grid(row=4, column=2, padx=(5, 0), sticky='w')
        # entry value
        self.week_entered_text1 = self.textentryweek.get()
        self.month_entered_text2 = self.textentrymonth.get()
        self.year_entered_text3 = self.textentryyear.get()
        if self.year_entered_text2 == "1":
            self.yearchange = int(self.year_entered_text3) - 1
            self.yearchange = str(self.yearchange)
        else:
            self.yearchange = self.year_entered_text3
    @staticmethod
    def createFolder(directory):
        try:
            if os.path.exists(directory):
                os.makedirs(directory)
            else: pass
        except OSError: pass
    def click1_week(self):
        filezipname = []
        filetxtname_pass = []
        path_name = []
        i = 0
        for index, entry in enumerate(self.sff_path_week):
            if entry.name.endswith('ZIP') and entry.is_file():
                filezipname.append(str(entry.name))
                path = f"{self.sff_path_week}\\{entry.name}"
                with zipfile.ZipFile(path) as zipFileObj:
                    i += 1
                    archive = zipFileObj.infolist()
                    read_me_file = archive[-4]
                    namefiletxt = read_me_file.filename
                    modimonth = int(read_me_file.date_time[1])
                    modiyear = int(read_me_file.date_time[0])
                    if modimonth == self.month_entered_text2 and modiyear == self.year_entered_text3:
                        zipFileObj.extract(namefiletxt, self.extract_txt_week)
                        # if we don't extract zip file, can we get to the files in it ?
                        # Answer: No
                        with open(f"{self.extract_txt_week}\\{read_me_file}", "r") as inFileTxt:

                        print("Pass")
                    else:
                        print("not pass")