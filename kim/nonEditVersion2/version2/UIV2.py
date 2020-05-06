import tkinter as tk
from tkinter import ttk
# from workAtNielsen.kim.nonEdit import settingUp
from PyNielsen.kim.nonEditVersion2 import setupV2 as settingUp
import pickle
import distutils.file_util
from tkinter import ttk

class UIForAutoCopy(tk.Tk):
    folder = [
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
    def __init__(self):
        tk.Tk.__init__(self)
        self.period = tk.StringVar()
        self.date = tk.StringVar()
        self.month = tk.StringVar()
        self.year = tk.StringVar()
        self.autoCp = None
        self.title("Auto Copy")
        self.geometry("500x300") #WxH
        # input_LabelFrame
        self.input_frame = tk.LabelFrame(self, width = 450, height=140, text="Input Date")
        self.input_frame.grid(row=0, column=0, columnspan=5, padx=25, pady=5)
        self.input_frame.grid_propagate(0)
        # input_Label
        self.period_label = tk.Label(self.input_frame, text="Period: ")
        self.period_label.grid(row=0, column=0)
        self.date_label = tk.Label(self.input_frame, text="Date: ")
        self.date_label.grid(row=1, column=0)
        self.month_label = tk.Label(self.input_frame, text="Month: ")
        self.month_label.grid(row=2, column=0)
        self.year_label = tk.Label(self.input_frame, text="Year: ")
        self.year_label.grid(row=3, column=0)
        # input_Entry
        self.period_entry = tk.Entry(self.input_frame, textvariable=self.period)
        self.period_entry.grid(row=0, column=1, columnspan=2)
        self.date_entry = tk.Entry(self.input_frame, textvariable=self.date)
        self.date_entry.grid(row=1, column=1, columnspan=2)
        self.month_entry = tk.Entry(self.input_frame, textvariable=self.month)
        self.month_entry.grid(row=2, column=1, columnspan=2)
        self.year_entry = tk.Entry(self.input_frame, textvariable=self.year)
        self.year_entry.grid(row=3, column=1, columnspan=2)

        # inputFolder_LabelFrame
        self.folder_labelFrame = tk.LabelFrame(self, width=450, height=140, text="Input Folder")
        self.folder_labelFrame.grid(row=1, column=0, columnspan=5, padx=25, pady=5)
        self.folder_labelFrame.grid_propagate(0)
        # inputFolder_label
        self.instruction_label = tk.Label(self.folder_labelFrame, text=r"Root Directory is: X:\Databases")
        self.instruction_label.grid(row=0, column=0)
        self.folder_label = tk.Label(self.folder_labelFrame, text="Choose Folder:")
        self.folder_label.grid(row=1, column=0)
        # inputFolder_combobox
        self.folder_combobox = ttk.Combobox(self.folder_labelFrame, values=sorted(self.folder), width=40)
        self.folder_combobox.grid(row=1, column=1, columnspan=3)
        self.folder_combobox.current(0)

        # copy Button
        self.copy_button = tk.Button(self.folder_labelFrame, text="start copying", command=self.copy)
        self.copy_button.grid(row=2, column=3, pady=10, sticky="WE")

        # # checking Label
        # self.checking_label = tk.Label(self.folder_labelFrame, text="check the upload first at Shared Drive:")
        # self.checking_label.grid(row=3, column=0, sticky="w")
        # checking_button
        self.checking_button = tk.Button(self.folder_labelFrame, text="check size", command=self.checkSize)
        self.checking_button.grid(row=3, column=3, sticky="WE")

    def copy(self):
        d = self.date.get()
        m = self.month.get()
        y = self.year.get()
        p = self.period.get()
        f = self.folder_combobox.get()
        if type(self.autoCp) is not None:
            self.autoCp = None
        try:
            check = "".join(f[f.find("\\")+1:].split(" ")).lower()
        except Exception :
            check = "".join(f.split(" "))
        self.autoCp = settingUp.AutoCopy(day=d, month=m, year=y, period=p, folder=f)
        if check.find("scantrack") != -1:
            self.autoCp.auto_copy()
        else:
            self.autoCp.auto_copy()
        pickleStartPathName = self.autoCp.childStartPath_l1 / "pickle"
        pickleEndPathName = self.autoCp.childFinalPath_l1 / "pickle"
        pickle_autoCpFile = open(pickleStartPathName, 'wb')
        pickle.dump(self.autoCp, pickle_autoCpFile)
        pickle_autoCpFile.close()
        distutils.file_util.copy_file(pickleStartPathName, pickleEndPathName)

    def checkSize(self):
        pickle_autoCpFile = open(self.autoCp.childFinalPath_l1 / "pickle")
        autoCpObj = pickle.load(pickle_autoCpFile)
        autoCpObj.


if __name__ == "__main__":
    autoCopy = UIForAutoCopy()
    autoCopy.mainloop()






