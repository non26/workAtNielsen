import tkinter as tk
from tkinter import ttk
# import distutils.file_util
# import pickle
# from tkinter import messagebox
from tkinter import filedialog
# from PyNielsen.kim.AutoCopy.nonEditVersion2.version2_2 import setupV2 as settingUp
# from workAtNielsen.kim.nonEditVersion2.version2_2 import setupV2 as settingUp
from PyNielsen.fromGithub.kim.AutoCopy.nonEditVersion2.version2_2 import setupV2 as settingUp
import threading
from PyNielsen.fromGithub.kim.AutoCopy.nonEditVersion2.version2_2.popUp_taskWithoutRootWD import alert_popUp as popUp
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
class InputTab():
    def __init__(self, root):
        self.period = tk.StringVar()
        self.date = tk.StringVar()
        self.month = tk.StringVar()
        self.year = tk.StringVar()
        input_info_tab = root
        # # input tab
        # input_LabelFrame
        input_frame = tk.LabelFrame(input_info_tab, width=450, height=250, text="Input Date")
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
        self.copy_button = tk.Button(input_frame, text="start copying")
        self.copy_button.grid(row=4, column=1, columnspan=2, pady=10, sticky="E")
        # # check folder
        # check labelFrame
        checking_labelFrame = tk.LabelFrame(input_info_tab, width=450, height=250, text="select folder")
        checking_labelFrame.grid(row=0, rowspan=5, column=5, columnspan=3, sticky="NS")
        checking_labelFrame.grid_propagate(0)
        # check folder button
        self.checking_vars = []
        for index, folder in enumerate(folders):
            var = tk.BooleanVar()
            checking_button = ttk.Checkbutton(checking_labelFrame, onvalue=True, offvalue=False, text=folder,
                                              variable=var)
            checking_button.pack(side=tk.TOP, anchor=tk.W, expand=tk.YES)
            self.checking_vars.append(var)
        # checking all
        self.checking_all = tk.IntVar()
        self.checking_all_button = ttk.Checkbutton(checking_labelFrame, onvalue=1, offvalue=0
                                              , text="All", variable=self.checking_all)
        self.checking_all_button.pack(side=tk.TOP, anchor=tk.W, expand=tk.YES)
class CheckingTab():
    def __init__(self, root):
        checking_file_tab = root
        # # checking tab
        # LabelFrame left
        left_labelFrame = tk.LabelFrame(checking_file_tab, width=300,
                                             height=250, text="from input")
        left_labelFrame.grid(row=0, column=0, rowspan=6, columnspan=6, padx=5, pady=5)
        left_labelFrame.grid_propagate(0)
        # ListBox
        xscroll = tk.Scrollbar(left_labelFrame, orient=tk.HORIZONTAL)
        yscroll = tk.Scrollbar(left_labelFrame, orient=tk.VERTICAL)
        self.listBox_csv = tk.Listbox(left_labelFrame
                                      , width=40
                                      , xscrollcommand=xscroll.set
                                      , yscrollcommand=yscroll.set)
        self.listBox_csv.grid(row=0, column=0, rowspan=5, columnspan=5)
        xscroll.grid(row=5, column=0, columnspan=5, sticky="WE")
        yscroll.grid(row=0, column=5, rowspan=5, sticky="SN")
        self.leftButton_checking = tk.Button(left_labelFrame, text="Check File")
        self.leftButton_checking.grid(row=6, column=4, sticky="NSEW")
        # LabelFrame right
        self.rightEntry_var = tk.StringVar()
        right_labelFrame = tk.LabelFrame(checking_file_tab, width=450
                                         , height=250, text="specify file to check")
        right_labelFrame.grid(row=0, column=6, rowspan=6, columnspan=6)
        right_labelFrame.grid_propagate(0)
        self.pathFile_entry = tk.Entry(right_labelFrame, width=50, textvariable=self.rightEntry_var)
        self.pathFile_entry.grid(row=0, column=0, columnspan=5, padx=5, pady=5)
        self.browse_rightButton = tk.Button(right_labelFrame, text="select file")
        self.browse_rightButton.grid(row=1, column=3, padx=5, pady=5, sticky="WE")
        self.rightButton_checking = tk.Button(right_labelFrame, text="Check File")
        self.rightButton_checking.grid(row=1, column=4, pady=5, sticky="WE")
        xscroll.config(command = self.listBox_csv.xview)
        yscroll.config(command = self.listBox_csv.yview)

class UIForAutoCopy(tk.Tk, InputTab, CheckingTab):
    def __init__(self):
        tk.Tk.__init__(self)
        self.pathLogCSV = []
        self.autoCp = None
        self.title("Auto Copy")
        self.geometry("800x350")  # WxH
        self.thread1 = None
        # initiate noteBook
        noteBook = ttk.Notebook(self)
        input_info_tab = tk.Frame(noteBook)
        checking_file_tab = tk.Frame(noteBook)
        noteBook.add(input_info_tab, text="Input Tab")
        noteBook.add(checking_file_tab, text="Checking Tab")
        noteBook.pack(fill=tk.BOTH, expand=1)
        InputTab.__init__(self, input_info_tab)
        self.copy_button["command"] = self.copy
        self.checking_all_button["command"] = self.checkedAll
        CheckingTab.__init__(self, checking_file_tab)
        self.leftButton_checking["command"] = self.checkSize_listBox
        self.rightButton_checking["command"] = self.checkSize_specific
        self.browse_rightButton["command"] = self.findFile

    def checkedAll(self):
        for item in self.checking_vars:
            if self.checking_all.get() == 1:
                item.set(1) # select
            else:
                item.set(0) # deselect

    def findFile(self):
        selectedFile = filedialog.askopenfilename(initialdir="C:", title="select file to check")
        self.rightEntry_var.set(selectedFile)

    def copy(self):
        selected_folder = [folders[index] for index, item in enumerate(self.checking_vars) if item.get()]
        d = self.date.get()
        m = self.month.get()
        y = self.year.get()
        p = self.period.get()
        for f in selected_folder:
            if bool(self.pathLogCSV):
                self.autoCopyObject = []
            if type(self.autoCp) is not None:
                self.autoCp = None
            if f.find("\\") != -1:
                check = "".join(f[f.find("\\") + 1:].split(" ")).lower()
            else:
                check = "".join(f.split(" "))
            self.autoCp = settingUp.AutoCopy(day=d, month=m, year=y, period=p, folder=f)
            self.pathLogCSV.append(self.autoCp.pathFinalLogCsv)
            if check.find("scantrack") == -1:
                self.thread1 = threading.Thread(target=self.autoCp.auto_copy, args=(1,))
            else:
                self.thread1 = threading.Thread(target=self.autoCp.auto_copy, args=("--all", keyWord_extension, None, True))
            self.thread1.start()
            self._showCompletionTask()

    def checkSize_listBox(self):
        for index, obj in enumerate(self.pathLogCSV):
            if self.autoCp is None:
                pass
            else:
                errors = self.autoCp.SizeCheckingFromG(obj)
                if errors != 0:
                    self.listBox_csv.itemconfig(index, fg="red") # if there is an unequal size checking, item'll be red
            self.autoCp.removeFile(self.autoCp.pathFinalLogCsv)
        popUp("Checking files", "Checking files are completed")

    def checkSize_specific(self):
        errors = settingUp.AutoCopy.SizeCheckingFromG(self.rightEntry_var.get())
        if errors != 0:
            self.pathFile_entry["fg"] = "red"

    def _showCompletionTask(self):
        if self.thread1.is_alive():
            self.after(1000, self._showCompletionTask)
        else:
            popUp(title="Copy files", message="copied files are completed. Please check the drive for upload")
            for item in self.pathLogCSV:
                self.listBox_csv.insert(tk.END, item)


if __name__ == "__main__":
    autoCopy = UIForAutoCopy()
    autoCopy.mainloop()
