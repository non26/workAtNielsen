from tkinter import *

from tkinter import filedialog
from tkinter import *
import time
import os
import zipfile
import xlsxwriter
from zipfile import ZipFile
import re


window = Tk()
window.title("Auto open SFF file")
window.geometry("300x150")


def click():
	entered_text1 = textentryweek.get()
	entered_text2 = textentrymonth.get()
	entered_text3 = textentryyear.get()
	passedText_file, Path2,passedText_file_monthly, Path2_monthly = GetFile(entered_text2,entered_text3)
	createFolder('./ForExtract_file/')
	status, file_name,status_monthly, file_name_monthly = detect_week_num(passedText_file,entered_text1,entered_text2,entered_text3,Path2,passedText_file_monthly, Path2_monthly)
	excel_summary(entered_text2,status,file_name,Path2,status_monthly, file_name_monthly,Path2_monthly)
	window.destroy()
	exit()

Label(window,text = "input week", fg = "black" ).grid(row =1 ,column = 0,padx = (10,0),pady = (0,20),sticky = 'w' )
textentryweek = Entry(window,width = 20, bg = "white")
textentryweek.grid(row = 1, column = 2 ,padx = (10,0),pady = (0,20), sticky ='E')

Label(window,text = "Input month", fg = "black" ).grid(row =2 ,column = 0,padx = (10,0),pady = (0,20),sticky = 'w' )
textentrymonth = Entry(window ,width = 20, bg = "white")
textentrymonth.grid(row = 2, column = 2 ,padx = (10,0),pady = (0,20), sticky ='E')

Label(window,text = "Input year", fg = "black" ).grid(row =3 ,column = 0,padx = (10,0),pady = (0,20),sticky = 'w' )
textentryyear = Entry(window ,width = 20, bg = "white")
textentryyear.grid(row = 3, column = 2 ,padx = (10,0),pady = (0,20), sticky ='E')

Button(window, text = "OK",width = 6, command = click).grid(row =4 , column =0 ,padx = (5,0), sticky = 'w')
________________________________________________________________________________________________________
#
# def open_SFF():
# 	url = 'C:\\Users\\TeNi9001\\Desktop\\Bee\\SFF-Test\\weekly'
# 	web.open(url)
# 	#time.sleep(2)
# 	#pg.move(100,300)
# 	open("01")
#_______________________________________________________________________________________________________________

def GetFile(monthpass,yearpass):
	#filezipname = ["SFF_Bsicuit_yummy.zip","SFF_Baby_Sup_wk.zip","SFF_CON_MiLK_WK_PERRY.zip" ]
	month = int(monthpass)
	obj = os.scandir(path ='N:\\Rf3db\\Rtdb\\Chain\\Big C\\SFF\\Weekly')
	year = int(yearpass)
	filezipname = []
	filetxtname_pass = []
	path_name =[]
	i=0	
	for index,entry in enumerate(obj) :
		if entry.name.endswith('ZIP') and entry.is_file():
			filezipname.append(str(entry.name))
			with zipfile.ZipFile(f"N:\\Rf3db\\Rtdb\\Chain\\Big C\\SFF\\Weekly\\{filezipname[i]}") as file:
				path = f"N:\\Rf3db\\Rtdb\\Chain\\Big C\\SFF\\Weekly\\{filezipname[i]}"
				i += 1
				archive = file.infolist()
				read_me_file = archive[-4]
				namefiletxt = format(read_me_file.filename)
				modimonth = int(format(read_me_file.date_time[1]))
				modiyear = int(format(read_me_file.date_time[0]))
				if modimonth == month and modiyear == year:
					filetxtname_pass.append(namefiletxt)
					path_name.append(path)
					print("Pass")
				else:
					print("not pass")

	#start detect monthly_________________________________________________________________________
	obj2 = os.scandir(path ='N:\\Rf3db\\Rtdb\\Chain\\Big C\\SFF\\Monthly') 
	filezipname_monthly = []
	filetxtname_pass_monthly = []
	path_name_monthly =[]
	km=0	
	for index,entry2 in enumerate(obj2) :
		if entry2.name.endswith('ZIP') and entry2.is_file():
			filezipname_monthly.append(str(entry2.name))
			with zipfile.ZipFile(f"N:\\Rf3db\\Rtdb\\Chain\\Big C\\SFF\\Monthly\\{filezipname_monthly[km]}") as file2:
				path_monthly = f"N:\\Rf3db\\Rtdb\\Chain\\Big C\\SFF\\Monthly\\{filezipname_monthly[km]}"
				km += 1
				archive_monthly = file2.infolist()
				read_me_file_monthly = archive_monthly[-4]
				namefiletxt_monthly = format(read_me_file_monthly.filename)
				modimonth2 = int(format(read_me_file_monthly.date_time[1]))
				modiyear2 = int(format(read_me_file_monthly.date_time[0]))
				if modimonth2 == month and modiyear2 == year:
					filetxtname_pass_monthly.append(namefiletxt_monthly)
					path_name_monthly.append(path_monthly)
					print("PassMonth")
				else:
					print("not PassMonth")

	return filetxtname_pass,path_name,filetxtname_pass_monthly,path_name_monthly

#________________________________________________________________________________________________________________

#weekdefReal,monthReal,yearReal = click()
#passedText_file = GetFile(monthReal,yearReal)
#detect_week_num(passedText_file,weekdefReal,monthReal,yearpass)

#________________________________________________________________________________________________________________

def detect_week_num(passedText,week_real,month_real,yaer_real,pathMa,passedText_monthly,pathma_monthly):

	passfile_list = passedText
	weeky = week_real
	monthy = int(month_real)
	yeary = yaer_real
	path_file = pathMa
	passfile_list_monthly = passedText_monthly
	path_file_monthly = pathma_monthly

	month_dict = { 1:"JAN" , 2 : "FEB", 3:"MAR", 4:"APR", 5 : "MAY", 6 :"JUNE", 7 :"JULY", 8 : "AUG" , 9:"SEP", 10:"OCT" , 11:"NOV" ,12:"DEC"}
	checked_month = month_dict.get(monthy-1)
	pass_status = []
	for k in range(len(passfile_list)):
		with zipfile.ZipFile(f"{path_file[k]}") as zip:
			listOfFileNames = zip.namelist()
			for m in range(len(listOfFileNames)):
				if listOfFileNames[m].endswith('.txt'):
					zip.extract(listOfFileNames[m],"N:\\Rf3db\\Rtdb\\Chain\\Big C\\SFF\\ForExtract_file")

		f = open(f"N:\\Rf3db\\Rtdb\\Chain\\Big C\\SFF\\ForExtract_file\\{passfile_list[k]}", "r")
		for x in f:
			detect = re.split(r'\s', x)
			for j in range(len(detect)):
				if detect[j] == f"W{weeky}{yeary.rstrip()[-2:]}":
					pass_status.append(1)
					break
				elif detect[j] != f"W{weeky}{yeary.rstrip()[-2:]}" and detect[j].endswith(f"{yeary.rstrip()[-2:]}"):
					pass_status.append(0)
					break

			else: continue
			break

	#start monthly section_____________________________________________________________________________
	
	pass_status_monthly = []
	for k2 in range(len(passfile_list_monthly)):
		with zipfile.ZipFile(f"{path_file_monthly[k2]}") as zipjo:
			listOfFileNames_monthly = zipjo.namelist()
			for m2 in range(len(listOfFileNames_monthly)):
				if listOfFileNames_monthly[m2].endswith('.txt'):
					zipjo.extract(listOfFileNames_monthly[m2],"N:\\Rf3db\\Rtdb\\Chain\\Big C\\SFF\\ForExtract_file")

		f22 = open(f"N:\\Rf3db\\Rtdb\\Chain\\Big C\\SFF\\ForExtract_file\\{passfile_list_monthly[k2]}", "r")
		for x2 in f22:
			detect2 = re.split(r'\s', x2)
			for j2 in range(len(detect2)):
				if detect2[j2] == f"{checked_month}{yeary.rstrip()[-2:]}":
					pass_status_monthly.append(1)
					break
				elif detect2[j2] != f"{checked_month}{yeary.rstrip()[-2:]}" and detect2[j2].endswith(f"{yeary.rstrip()[-2:]}") :
					pass_status_monthly.append(0)
					break
			else: continue
			break
	return pass_status,passfile_list,pass_status_monthly,passfile_list_monthly
		
''''		
		for x in f:
			if x.startswith('LAST_PERIOD'):
				#print(x[-7:])
				print(x.rstrip()[-7:])
				x=x.rstrip()
				#if x == "Weekly - W4319": 
				if x[-7:] == f"W{weeky}{yeary.rstrip()[-2:]} ;":
					print("pass ja")
'''
		
	#print("line_num: ",k)

#_________________________________________________________________________________________________________________________
def createFolder(directory):
		try:
			if not os.path.exists(directory):
				os.makedirs(directory)
		except OSError:
			print ('Error: Creating directory. ' +  directory)

#____________________________________________________________________________________________________________________________

def excel_summary(filenamemonth,status_new,passnamefile,path_sff,status_new_monthly,passnamefile_monthly,path_sff_monthly):
	status = status_new
	nameFile_to_excel = passnamefile
	path = path_sff

	status_monthly = status_new_monthly
	nameFile_to_excel_monthly = passnamefile_monthly
	path_monthly = path_sff_monthly

	name_M = int(filenamemonth)

	month_dict = { 1:"JAN" , 2 : "FEB", 3:"MAR", 4:"APR", 5 : "MAY", 6 :"JUNE", 7 :"JULY", 8 : "AUG" , 9:"SEP", 10:"OCT" , 11:"NOV" ,12:"DEC"}
	workbook = xlsxwriter.Workbook(f'N:\\Rf3db\\Rtdb\\Chain\\Big C\\SFF\\SFF_Summary_month_{month_dict.get(name_M)}.xlsx')
	worksheet1 = workbook.add_worksheet('SUMMARY_SFF_File(weekly)')
	worksheet2 = workbook.add_worksheet('SUMMARY_SFF_File(monthly)')
	

	cell_format = workbook.add_format()
	cell_format.set_pattern(1)  # This is optional when using a solid fill.
	cell_format.set_bg_color('pink')

	worksheet1.write('A1', 'Status', cell_format)
	worksheet1.write('B1', 'FileName', cell_format)
	worksheet1.write('C1', 'Path_Name', cell_format)

	worksheet2.write('A1', 'Status', cell_format)
	worksheet2.write('B1', 'FileName', cell_format)
	worksheet2.write('C1', 'Path_Name', cell_format)
	worksheet2.write('D1', 'Month_data', cell_format)

	row = 1
	col = 0
	status_des = []
	status_des_monthly = []

	for r in range(len(status)):
		if status[r] == 1:
			status_des.append("Pass")

		elif status[r] == 0:
			status_des.append("Fail")

	for po in range(len(status_monthly)):
		if status_monthly[po] == 1:
			status_des_monthly.append("Pass")

		elif status_monthly[po] == 0:
			status_des_monthly.append("Fail")
# Iterate over the data and write it out row by row. 
	for jd in range(len(status)): 
		worksheet1.write(row, 0, status_des[jd]) 
		worksheet1.write(row, 1, nameFile_to_excel[jd]) 
		worksheet1.write(row, 2, path[jd])
		row += 1

	row2 = 1
	for ch in range(len(status_monthly)): 
		worksheet2.write(row2, 0, status_des_monthly[ch]) 
		worksheet2.write(row2, 1, nameFile_to_excel_monthly[ch]) 
		worksheet2.write(row2, 2, path_monthly[ch])
		worksheet2.write(row2, 3, month_dict.get(name_M-1))
		row2 += 1

	workbook.close()


window.mainloop()
