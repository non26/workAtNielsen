import tkinter as tk
from tkinter import ttk
# import distutils.file_util
# import pickle
# from tkinter import messagebox
from tkinter import filedialog
from PyNielsen.kim.nonEditVersion2 import setupV2 as settingUp

folders = [
    r"Monthly Retail Index"
    , r"Monthly Retailer"
    , r"Weekly Retailer"
    , r"Weekly Database\e-Commerce\Manufacturer"
    , r"Weekly Database\Manufact"
    , r"Weekly Database\Causal"
    , r"DDP\Watsons"
    , r"Weekly Database\ScanTrack Family Mart"
    , r"Weekly Database\ScanTrack Big C"
    , r"Weekly Database\ScanTrack Makro"
    , r"Weekly Database\ScanTrack Tesco"
    , r"Weekly Database\ScanTrack The Mall"
    , r"Weekly Database\ScanTrack Tops"
]
keyWord_extension = [
    ".CHR", ".HED", ".IDX", ".INF", ".TAD"
]

class UIForAutoCopy(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.period = tk.StringVar()
        self.date = tk.StringVar()
        self.month = tk.StringVar()
        self.year = tk.StringVar()
        self.autoCopyObject = []
        self.autoCp = None
        self.title("Auto Copy")
        self.geometry("800x350") #WxH
        # initiate noteBook
        noteBook = ttk.Notebook(self)
        input_info_tab = tk.Frame(noteBook)
        checking_file_tab = tk.Frame(noteBook)
        noteBook.add(input_info_tab, text="Input Tab")
        noteBook.add(checking_file_tab, text="Checking Tab")
        noteBook.pack(fill=tk.BOTH, expand=1)
        # # input tab
        # input_LabelFrame
        input_frame = tk.LabelFrame(input_info_tab, width=450, height=140, text="Input Date")
        input_frame.grid(row=0, column=0, rowspan=5, columnspan=5, padx=25, pady=5, sticky="SN")
        input_frame.grid_propagate(0)
        # input_Label
        label = ["Period: ", "Date: ", "Month: ", "Year: "]
        for index, name in enumerate(label):
            period_label = tk.Label(input_frame, text=name)
            period_label.grid(row=index, column=0)
        # input_Entry
        period_entry = tk.Entry(input_frame, textvariable=self.period)
        period_entry.grid(row=0, column=1, columnspan=2)
        date_entry = tk.Entry(input_frame, textvariable=self.date)
        date_entry.grid(row=1, column=1, columnspan=2)
        month_entry = tk.Entry(input_frame, textvariable=self.month)
        month_entry.grid(row=2, column=1, columnspan=2)
        year_entry = tk.Entry(input_frame, textvariable=self.year)
        year_entry.grid(row=3, column=1, columnspan=2)
        # label instruction
        instruction = ["FEB'19 (19 is year)", "1-31", "1-12", "2020(20xx)"]
        for index, ins in enumerate(instruction):
            tk.Label(input_frame, text=ins).grid(row=index, column=3, sticky="W", padx=5)
        # copy Button
        copy_button = tk.Button(input_frame, text="start copying", command=self.copy)
        copy_button.grid(row=4, column=1, columnspan=2, pady=10, sticky="E")
        # # check folder
        # check labelFrame
        checking_labelFrame = tk.LabelFrame(input_info_tab, width=450, height=200, text="select folder")
        checking_labelFrame.grid(row=0, rowspan=5, column=5, columnspan=3, sticky="NS")
        checking_labelFrame.grid_propagate(0)
        # check folder button
        self.checking_vars = []
        for index, folder in enumerate(folders):
            var = tk.BooleanVar()
            checking_button = ttk.Checkbutton(checking_labelFrame, onvalue=True, offvalue=False ,text=folder, variable=var)
            checking_button.pack(side=tk.TOP, anchor=tk.W, expand=tk.YES)
            self.checking_vars.append(var)
        # checking all
        self.checking_all = tk.IntVar()
        checking_all_button = ttk.Checkbutton(checking_labelFrame, onvalue=1, offvalue=0
                                                   , text="All", variable=self.checking_all
                                                   , command=self.checkedAll)
        checking_all_button.pack(side=tk.TOP, anchor=tk.W, expand=tk.YES)
        
        # # checking tab
        # label checking
        self.checking_varEntry = tk.StringVar()
        checking_label = tk.Label(checking_file_tab, text="Checking")
        checking_label.grid(row=0, column=0)
        # entry checking
        checking_entry = tk.Entry(checking_file_tab, textvariable=self.checking_varEntry, width=35)
        checking_entry.grid(row=1, column=0, columnspan=5, sticky="EW", padx=10)
        # button checking
        browse_button = tk.Button(checking_file_tab, text="select file",command=self.findFile)
        browse_button.grid(row=1, column=5, sticky="EW")
        # checking_button
        checking_button = tk.Button(checking_file_tab, text="check size", command=self.checkSize)
        checking_button.grid(row=1, column=6, sticky="WE", padx=5)
        # label checking
        self.cnt_checkingVar = tk.StringVar()
        cnt_label = tk.Label(checking_file_tab, text="Files error")
        cnt_label.grid(row=2, column=0)
        cnt = tk.Entry(checking_file_tab, textvariable=self.cnt_checkingVar, state="readonly")
        cnt.grid(row=2, column=1)
    def checkedAll(self):
        for item in self.checking_vars:
            if self.checking_all.get() == 1:
                item.set(1)
            else:
                item.set(0)
    def copy(self):
        selected_folder = [ folders[index] for index, item in enumerate(self.checking_vars) if item.get() ]
        d = self.date.get()
        m = self.month.get()
        y = self.year.get()
        p = self.period.get()
        # f = self.folder_combobox.get()
        for f in selected_folder:
            if bool(self.autoCopyObject):
                self.autoCopyObject = []
            if type(self.autoCp) is not None:
                self.autoCp = None
            if f.find("\\") != -1:
                check = "".join(f[f.find("\\") + 1:].split(" ")).lower()
            else:
                check = "".join(f.split(" "))
            self.autoCp = settingUp.AutoCopy(day=d, month=m, year=y, period=p, folder=f)
            self.checking_varEntry.set(self.autoCp.childFinalPath_l1 / "logCopiedFiles.csv")
            self.autoCopyObject.append(self.autoCp)
            if check.find("scantrack") == -1:
                self.autoCp.auto_copy(deep=1)
            else:
                self.autoCp.auto_copy(deep="--all", criteriaExtension=keyWord_extension)

    def findFile(self):
        selectedFile = filedialog.askopenfilename(initialdir="C:", title = "select file to check")
        self.checking_varEntry.set(selectedFile)

    def checkSize(self):
        for obj in self.autoCopyObject:
            if self.autoCp is None:
                pass
            else:
                errors = self.autoCp.SizeCheckingFromG()
                self.cnt_checkingVar.set(errors)

if __name__ == "__main__":
    autoCopy = UIForAutoCopy()
    autoCopy.mainloop()
