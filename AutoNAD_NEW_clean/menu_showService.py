import tkinter as tk
from tkinter import ttk
from tkinter import font
import json
from .DataBase.service import connDatabaseService as cdbs
from .DataBase.service import *
from .DataBase.service import update_matchingFileWithDBName as mf
# from  tkinter import TclError
class ShowMatchedDBName():
    def __init__(self, master,  embedObj, chosenService):
        """
        :param master: self.master. This is result_labelFrame from SubMenuShowView class
        # :param rows:
        :param embedObj: here, is the ListBox from the SubMenuShowView class
        :param selectedmbd:
        """
        # try:
        #     self.tree.destroy()
        #     print("destroy")
        # except Exception:
        #     pass
        self.chosenService = chosenService
        self.master = master
        self.embedObj = embedObj
        self.tree_column=[]
        self.tree = None
        self.showDBNameAndFile()
        self._build_tree()
    def showDBNameAndFile(self):
            self.tree_column = ("DBName", "File")
            self.tree = ttk.Treeview(master=self.master, columns=self.tree_column
                                     , show="headings", height=25)
            tree_vsb = ttk.Scrollbar(master=self.master, orient="vertical", command=self.tree.yview)
            tree_hsb = ttk.Scrollbar(master=self.master, orient="horizontal", command=self.tree.xview)
            self.tree.configure(yscrollcommand=tree_vsb.set, xscrollcommand=tree_hsb.set)
            self.tree.grid(row=0, column=1, rowspan=30)
            tree_vsb.grid(row=0, column=2, rowspan=30, sticky="NS")
            tree_hsb.grid(row=30, column=1, sticky="EW")
    def _build_tree(self):
        conn = cdbs.ConnDatabaseService()
        tree_data = conn.sql_DBNameAndFileQuery(serviceName=self.chosenService)
        # if self.chosenService.lower().find("monthly") != -1:
        for col in self.tree_column:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=font.Font().measure(col))
        for child in tree_data:
            self.tree.insert("", tk.END, values=child)
            for index, value in enumerate(child):
                # ilen = font.Font().measure(value)
                # if self.tree.column(self.tree_column[index], width=None) < ilen:
                self.tree.column(self.tree_column[index], width=200)
            # self.tree.column(width=200)
class SubMenuShowView():
    def __init__(self, master, embedObj = None):
        """
        This class is called at ShowService Class with
        :param master: self.master
        # :param rows: self.allService
        :param embedObj: self
        """
        self.master = master
        self.rootObj = embedObj
        self.chooseService = None
        rows = self.readService()
        # Frame
        self.result_labelFrame = tk.LabelFrame(self.rootObj, text="View", width=900
                                               , height=600, borderwidth=1)
        self.result_labelFrame.grid(row=0, column=1)
        self.result_labelFrame.grid_propagate(0)
        # ListBox
        self.service_listBox = tk.Listbox(self.result_labelFrame, width=50, height=30, exportselection=tk.FALSE)
        self.service_listBox.grid(row=0, column=0, padx=10, rowspan=30)
        service = sorted(rows["service"], key=lambda x: str(x))
        [self.service_listBox.insert("end", f"{item}") for item in service if str(item) != "nan"]
        self.service_listBox.bind("<Double-Button-1>", self.getMatching)
        # self.service_listBox.bind("<Button-1>", self.getMatching)
        # self.service_listBox.bind("<<Listboxselection>>", self.getMatching)
        # service = self.service_listBox.get(tk.ACTIVE)

    def readService(self):
        path = pathService
        with open(path+"\\"+"service.json") as file:
            service = json.load(file)
        return service

    def _scroll(self,*arg):
        self.service_listBox.yview(*arg)

    def getMatching(self, event):
        if self.chooseService.__class__.__base__.__name__ == "Widget":
            self.chooseService.destroy()
        # print(self.service_listBox.curselection())
        service = self.service_listBox.get(tk.ACTIVE)
        # service = self.service_listBox.get(self.service_listBox.curselection())
        # print("Service: ", service)
        x=ShowMatchedDBName(master=self.result_labelFrame
                          , embedObj=self.rootObj
                          , chosenService=service)
        self.chooseService = x.tree

class SubMenuAdding():
    def __init__(self, master, embedObj):
        self.master = master
        self.rootObj = embedObj # self of the ShowService
        self.service = tk.StringVar()
        self.adding_labelFrame = tk.LabelFrame(self.rootObj, text="Adding service"
                                               ,width=900, height=600, borderwidth=1)
        self.adding_labelFrame.grid(row=0, column=1)
        self.adding_labelFrame.grid_propagate(0)
        self.adding_frame = tk.Frame(self.adding_labelFrame
                                     , width=400, height=600, borderwidth=1)
        self.adding_frame.grid(row=0, column=1)
        # adding Service
        self.service_label = tk.Label(self.adding_frame, text="specify service:")
        self.service_label.grid(row=0, column=0, padx=10, sticky="w")
        self.service_entry = tk.Entry(self.adding_frame, width=50, textvariable=self.service)
        self.service_entry.grid(row=0, column=1, sticky="w")
        # update Button
        self.update_button = tk.Button(self.adding_frame, text='Update', command=self.start_adding)
        self.update_button.grid(row=2, column=1, sticky='e')

    def start_adding(self):
        added_service = [x.strip() for x in self.service.get().split(',')]
        self.rootObj.allService["service"].extend(added_service)
        self.rootObj.service.writing_service(value=self.rootObj.allService["service"])

class ShowService(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.master = master
        self.choose_viewButton = None
        # self.master.title("Show MBDCode")
        # self.master.geometry("1100x800")  # WxH
        self.title("Show Service")
        self.geometry("1100x800")  # WxH
        self.option = tk.StringVar()
        self.option.set(value=0)
        self.frame1_labelFrame = tk.LabelFrame(self, text="Option", width=100, height=600, borderwidth=1)
        self.frame1_labelFrame.grid(row=0, column=0, padx=25, pady=25, sticky="NSEW")
        self.frame1_labelFrame.grid_propagate(0)
        self.frame1 = tk.Frame(self.frame1_labelFrame, borderwidth=1)
        self.frame1.grid(row=0, column=0, sticky="NSEW")

        # # Radio Button
        # view Radio Button
        self.view_radioButton = tk.Radiobutton(self.frame1, text="View"
                                               , variable=self.option, value="View", anchor="w")
        self.view_radioButton.grid(row=0, column=0, padx=10, sticky="nw")
        # add Radio Button
        self.add_radioButton = tk.Radiobutton(self.frame1, text="Add"
                                              , variable=self.option, value="Add", anchor='n')
        self.add_radioButton.grid(row=1, column=0, padx=10, sticky="nw")
        # # add command
        self.view_radioButton["command"] = self.mbd_showView
        self.add_radioButton["command"] = self.mbd_adding
        # # button
        # update DBName and File
        self.update_button = tk.Button(self.frame1, text="Update"
                                       , command=self.updateData)
        self.update_button.grid(row=2, column=0)

    def updateData(self):
        print("start updating the service")
        matching = mf.MatchingFile()
        x = matching.getServiceName() # service name
        y = matching.getSetting()  # get path config from the Setting menu
        # y["checkList"] means, getting check list path
        # z is the group object by "Service"
        z = matching.matchDBName(y["checkList"])
        matching.getCorrespondingFile(serviceName=x, pathConfig=y, df_DBName=z)
        matching.conn.sql_closeConn()
        print("finish updating")

    def mbd_showView(self):
        self.choose_viewButton = SubMenuShowView(master=self.master, embedObj=self)

    def mbd_adding(self):
        self.choose_viewButton = SubMenuAdding(self.master, self)
