import tkinter as tk
from tkinter import TclError
import re
# from AutoNAD.DataBase.service import Service
from .DataBase.service import Service
class ServiceAutoCompleteEntry():
    # def __init__(self , master, mastervariable, x,y ): # master is An Entry where we need to get the search
    def __init__(self, master, mastervariable, parentMaster, row=None, column=None):
        """
        :param master: master is An Entry where we need to get the search
        :param mastervariable: variable of that entry
        :param parentMaster: master of the entry
        :param row:
        :param column:
        """
        self.parent = parentMaster
        self.master = master
        self.row = row
        self.column= column
        # # self.lb = tk.Listbox() # when place a ListBox here
        # # # it will get an error when you type and then delete
        self.var = mastervariable
        self.var.trace('w', self.change)
        self.master.bind("<Down>", self.down)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Right>", self.selection)
        # self.master.bind("<Return>", self.selection)
        self.lbUp = False
        self.index = 0
        self.length = 1

    def change(self, name, index, mode):
        # This version will cause the error when we delete the input from the entry
        # because self.var.ge() always return the last value before first deleting that makes
        # 'words' always have the non-empty value in it.
        # if self.var.get() == "":
        #     try:
        #         self.lb.destroy()
        #     except AttributeError:
        #         pass
        #     finally:
        #         self.lbUp = False
        # else:
        #     words, self.length = self.comparison()
        #     print(words)
        #     print(bool(words))
        #     if words:
        #         if not self.lbUp:
        #             self.lb = tk.Listbox(self.parent, width=40)
        #             self.lb.bind("<Double-Button-1>", self.selection)
        #             self.lb.bind("<Right>", self.selection)
        #             # self.lb.place(x=self.x, y=self.y)
        #             self.lbUp = True
        #             self.lb.grid(row=4, column=1, columnspan =5)
        #
        #         self.lb.delete(0, tk.END)
        #         for word in words:
        #             self.lb.insert(tk.END, word)
        #     else:
        #         if self.lbUp:
        #             self.lb.destroy()
        #             self.lbUp = False
        if self.var.get() == "":
            try:
                self.lb.destroy()
            except AttributeError:
                pass
            finally:
                self.lbUp = False
        else:
            words, self.length = self.comparison()
            if words :
                if self.lbUp: # old: , not False
                    try:
                        self.lb.destroy()
                    except AttributeError:
                        pass
                # if not self.lbUp:
                self.lb = tk.Listbox(self.parent, width=40, height=self.length+1)
                self.lb.bind("<Double-Button-1>", self.selection)
                # self.lb.bind("<Right>", self.selection)
                # self.lb.place(x=100, y=100)
                self.lbUp = True
                self.lb.grid(row=self.row, column=self.column, columnspan=5)
                # print(self.master.winfo_rootx(), self.master.winfo_rooty()-self.master.winfo_height())
                # self.lb.place(x=self.master.winfo_rootx(), y=self.master.winfo_rooty()-self.master.winfo_height())
                # self.parent.update_idletasks()
                try:
                    self.lb.delete(0, tk.END)
                    for word in words:
                        self.lb.insert(tk.END, word)
                except TclError : pass
            else:
                if self.lbUp:
                    self.lb.destroy()
                    self.lbUp = False

    def selection(self, event):
        if self.lbUp:
            self.var.set(self.lb.get(tk.ACTIVE))# this line will trigger the trace method as well
            self.lb.destroy()
            self.master.icursor(tk.END)
            # self.lbUp = True # if we change it to False we need to add more condition in change()
            self.lbUp = False

    def down(self, event):
        # print("down",self.lb.curselection())
        # if self.lbUp:
        #     if self.lb.curselection() == ():
        #         pass
        #     else:
        #         self.index = self.lb.curselection()[0]
        #     print(self.index)
        #     if self.index != self.length-1:
        #         self.lb.select_clear(first=self.index)
        #         self.index += 1
        #         self.lb.select_set(first=self.index)
        #         self.lb.activate(self.index)
        if self.lbUp:
            if self.lb.curselection() == ():
                self.index=0
            if self.index <= self.length-1:
                self.lb.select_clear(first=self.index-1)
                self.lb.select_set(first=self.index)
                self.lb.activate(self.index)
                self.index += 1  # last value is self.length
    def up(self, event):
        if self.lbUp:
            if self.index == self.length - 1:
                pass
            elif self.lb.curselection() == ():
                self.index = self.length
            else:
                self.index = self.lb.curselection()[0]
            if self.index != 0:
                self.lb.select_clear(first=self.index)
                self.index -= 1
                self.lb.select_set(first=self.index)
                self.lb.activate(self.index)
    def comparison(self):
            words = Service.Service().reading_service()['service']
            pattern = re.compile(f".*{re.escape(self.var.get())}.*")
            result =[word for word in words if re.match(pattern, str(word))]
            return result, len(result)
















