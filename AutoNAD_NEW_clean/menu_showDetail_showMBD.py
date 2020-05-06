import tkinter as tk
import tkinter.font
from tkinter import ttk
# from workAtNielsen.AutoNAD_NEW_editting.DataBase.MBD.hidden import connDataBaseHiddenDB as cdb
from .DataBase.MBD.hidden import connDataBaseHiddenDB as cdb
from tkinter import filedialog
class SubMenuShowView:
    def __init__(self, master):
        self.tree_column = ("MBDCode", "DESCRIPTION", "Hide MBD", "Show Hide")
        self.master = master
        # # LabelFrame
        self.tree_labelFrame = tk.LabelFrame(self.master, text="MBD", width=900, height=600)
        self.tree_labelFrame.grid(row=0, rowspan=3, column=1, columnspan=4)
        self.tree_labelFrame.grid_propagate(0)
        # # tree
        self.tree = ttk.Treeview(master=self.tree_labelFrame, columns=self.tree_column
                                 , show="headings", height=25)
        self.tree_vsb = ttk.Scrollbar(master=self.tree_labelFrame, orient="vertical", command=self.tree.yview)
        self.tree_hsb = ttk.Scrollbar(master=self.tree_labelFrame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.tree_vsb.set, xscrollcommand=self.tree_hsb.set)
        self.tree.grid(row=0, rowspan=4, column=0, columnspan=4, stick="NSEW")
        self.tree_vsb.grid(row=0, rowspan=4, column=4, sticky="NS")
        self.tree_hsb.grid(row=4, column=0, columnspan=4, sticky="EW")
        self._build_tree()

    def connDataBase(self):
        data = cdb.ConnDataBaseHiddenDB()
        row = data.sql_queryingAllData()
        for item in row:
            yield item

    def _build_tree(self):
        data2Fill = self.connDataBase()
        for col in self.tree_column:
            self.tree.heading(column=col, text=col)
            self.tree.column(column=col, width=tkinter.font.Font().measure(col))
        for child in data2Fill:
            self.tree.insert("", tk.END, values=child)
            for index, value in enumerate(child):
                valueLen = tkinter.font.Font().measure(value)
                if self.tree.column(self.tree_column[index], width=None) < valueLen:
                    self.tree.column(self.tree_column[index], width=valueLen)

class SubMenuAdding:
    def __init__(self, master):
        self.conn = cdb.ConnDataBaseHiddenDB()
        self.master = master
        self.fillMBDCode_var = tk.StringVar()
        self.fillDescription_var = tk.StringVar()
        self.fillHideMBD_var = tk.StringVar()
        self.fillShowHide_var = tk.StringVar()
        # # labelFrame
        self.add_labelFrame = tk.LabelFrame(self.master, text="ADD", width=900, height=600)
        self.add_labelFrame.grid(row=0, rowspan=3, column=1, columnspan=4)
        self.add_labelFrame.grid_propagate(0)
        # # label
        self.add_label = tk.Label(self.add_labelFrame, text="Fill the following details: ")
        self.add_label.grid(row=0, column=0, columnspan=3)
        # # Fill-MBDCode
        self.fillMBDCode_label = tk.Label(self.add_labelFrame, text="MBDCode")
        self.fillMBDCode_label.grid(row=1, column=0, columnspan=3)
        self.fillMBDCode_entry = tk.Entry(self.add_labelFrame, textvariable = self.fillMBDCode_var, width=20)
        self.fillMBDCode_entry.grid(row=1, column=3, columnspan=3)
        # # Fill-Description
        self.fillDescription_label = tk.Label(self.add_labelFrame, text="Description")
        self.fillDescription_label.grid(row=2, column=0, columnspan=3)
        self.fillDescription_entry = tk.Entry(self.add_labelFrame, textvariable=self.fillDescription_var, width=20)
        self.fillDescription_entry.grid(row=2, column=3, columnspan=3)
        # # Fill-Hide MBD
        self.fillHideMBD_label = tk.Label(self.add_labelFrame, text="Hide MBD")
        self.fillHideMBD_label.grid(row=3, column=0, columnspan=3)
        self.fillHideMBD_entry = tk.Entry(self.add_labelFrame, textvariable=self.fillHideMBD_var, width=20)
        self.fillHideMBD_entry.grid(row=3, column=3, columnspan=3)
        instruction = tk.Label(self.add_labelFrame, text="if there is, input 'x', if not let it empty")
        instruction.grid(row=3, column=6)
        # # Fill-Show Hide
        self.fillShowHide_label = tk.Label(self.add_labelFrame, text="Show MBD")
        self.fillShowHide_label.grid(row=4, column=0, columnspan=3)
        self.fillShowHide_entry = tk.Entry(self.add_labelFrame, textvariable=self.fillShowHide_var, width=20)
        self.fillShowHide_entry.grid(row=4, column=3, columnspan=3)
        instruction = tk.Label(self.add_labelFrame, text="if there is, input 'x', if not let it empty")
        instruction.grid(row=4, column=6)
        # button
        self.add_button = tk.Button(self.add_labelFrame, text="ADD", command=self.update2DataBase_byAdding)
        self.add_button.bind("<Return>", self.update2DataBase_byAdding)
        self.add_button.grid(row=5, column=3, columnspan=3, sticky="EW")
        # # input file to update
        tk.Label(self.add_labelFrame, text="Input file for the hidden MBD").grid(row=6, column=0, columnspan=3)
        self.file2Update_button = tk.Button(self.add_labelFrame, text="Input File", command=self.openFile)
        self.file2Update_button.grid(row=7, column=3, columnspan=3, sticky="EW")

    def update2DataBase_byAdding(self, event=None):
        iteration = [var.get() for var in (self.fillMBDCode_var, self.fillDescription_var
                                           , self.fillHideMBD_var, self.fillShowHide_var)
                     ]
        [self.conn.sql_insert(row) for row in iteration]
        self.conn.sql_closeConn()

    def openFile(self):
        file = filedialog.askopenfilename(initialdir="C:", title = "select CheckList")
        try:
            self.conn.sql_createTable()
        except Exception as e: pass
        finally:
            self.conn.sql_excel2DataBase(pathExcel=file)

class ShowMBDCode:
    def __init__(self, master):

        self.master=master
        self.master.title("Show MBDCode")
        self.master.geometry("1100x800") #WxH
        self.optionVar = tk.StringVar()
        self.optionVar.set(value=0)
        self.choose_frame = None
        # # LabelFrame
        self.frame1_labelFrame = tk.LabelFrame(self.master,  text="MBDCode",width=100, height=600, borderwidth=1)
        self.frame1_labelFrame.grid(row=0, rowspan=3, column=0, padx=25, pady=25, sticky="NSEW")
        self.frame1_labelFrame.grid_propagate(0)
        self.frame1 = tk.Frame(self.frame1_labelFrame, borderwidth=1)
        self.frame1.grid(row=0, rowspan=3, column=0,  sticky="NSEW")
        # # Radio Button
        # view Radio Button
        self.view_radioButton = tk.Radiobutton(self.frame1, text="View"
                                               , variable=self.optionVar, value="View", anchor="w")
        self.view_radioButton.grid(row=0, column=0, padx=10, sticky="nw")
        # add Radio Button
        self.add_radioButton = tk.Radiobutton(self.frame1, text="Add"
                                              , variable=self.optionVar, value="Add", anchor='n')
        self.add_radioButton.grid(row=1, column=0, padx=10, sticky="nw")
        self.view_radioButton["command"] = self.mbd_showView
        self.add_radioButton["command"] = self.mbd_adding

    def mbd_showView(self):
        # if self.choose_frame:
        #     self.choose_frame.tree_labelFrame.destroy()
        #     self.choose_frame=SubMenuShowView(master=self.master)
        # else:
        #     self.choose_frame=SubMenuShowView(master=self.master)
        self.choose_frame=SubMenuShowView(master=self.master)

    def mbd_adding(self):
        # if self.choose_frame:
        #     self.choose_frame.add_labelFrame.destroy()
        #     self.choose_frame=SubMenuAdding(master=self.master)
        # else:
        #     self.choose_frame=SubMenuAdding(master=self.master)
        self.choose_frame=SubMenuAdding(master=self.master)
