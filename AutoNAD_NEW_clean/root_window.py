import tkinter as tk
from .FrontEnd_Monthly.monthlyWindow import  MonthWindow\
    , Menu_ShowDetail_ShowMBD as SubMenuShowMBD
from .FrontEnd_Weekly.weeklyWindow import WeekWindow
from . import menu_setting as ms
from . import menu_showService as mss
# import os
class mainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Automate NAD")
        self.geometry("1000x600") #WxH
    # # LabelFrame
        self.week = tk.LabelFrame(self, width=450, height=500, text="weekly")
        self.week.grid(row=0, column=0, rowspan=5, padx=(10, 5))
        self.week.grid_propagate(0)
        self.month = tk.LabelFrame(self, width=450, height=500, text="monthly")
        self.month.grid(row=0, column=1, rowspan=5, padx=(5, 10))
        self.month.grid_propagate(0)
    # # Menu
        self.menu = tk.Menu(self, bg="black", fg="white")

        # setting Menu
        setting = tk.Menu(self.menu, tearoff=0, bg="white", fg="black")
        self.menu.add_cascade(label="Setting", menu=setting)
        # setting Menu---set up default
        setting.add_command(label="Set Up Default", command=self.setUp_file)

        # MBD Menu
        mbd = tk.Menu(self.menu, tearoff=0, bg="white", fg="black")
        self.menu.add_cascade(label="MBD", menu=mbd)
        # MBD Menu---show MBD code
        mbd.add_command(label="Show hidden MBD", command=self.show_MBDCode)

        # Service Menu
        service = tk.Menu(self.menu, tearoff=0, bg="white", fg="black")
        # Service Menu---show service
        service.add_command(label="Show Service", command=self.show_service)
        self.menu.add_cascade(label="Service", menu=service)

        # all menus config
        self.config(menu=self.menu)

    # # Monthly side
        self.monthlySide = MonthWindow(master=self.month)
    # # Weekly side
        self.weeklySide = WeekWindow(master=self.week)
    def onClosingConfigurationWindow(self, widget):
        widget.destroy()
        self.monthlySide.setMonthlyDetail()
        self.weeklySide.setWeeklyDetail()
    def showHidden(self): pass

    def show_MBDCode(self):
        """
        Menu MBD
        :return:
        """
        root2 = tk.Toplevel(self)
        root2.transient(self)
        SubMenuShowMBD(root2)
    def show_service(self):
        """
        menu Service
        :return:
        """
        mss.ShowService(master=self)
    def setUp_file(self):
        """
        set the configuration, Menu Setting
        :return:
        """
        root2 = tk.Toplevel(self)
        root2.transient(self)
        # thread1 = threading.Thread(target=ms.Setting, args=(root2,))
        # thread1.start()
        ms.Setting(root2)
        root2.protocol("WM_DELETE_WINDOW", lambda w=root2: self.onClosingConfigurationWindow(widget=w))
