def GetFilemonth(monthpass,yearpass):
	month = int(monthpass)
	year = int(yearpass)
	obj2 = os.scandir(path ='N:\\Rf3db\\Rtdb\\Chain\\Big C\\SFF\\Monthly')
	filezipname_monthly = []
	filetxtname_pass_monthly = []
	path_name_monthly =[]

	km=0
	for index,entry2 in enumerate(obj2) :
		if entry2.name.endswith('ZIP') and entry2.is_file():
			filezipname_monthly.append(str(entry2.name))
			#stayedpath = os.path.commonpath(['c:/Users/TeNi9001', name])
			#filename = entry.name
			with zipfile.ZipFile(f"N:\\Rf3db\\Rtdb\\Chain\\Big C\\SFF\\Monthly\\{filezipname_monthly[km]}") as file2:
				path_monthly = f"N:\\Rf3db\\Rtdb\\Chain\\Big C\\SFF\\Monthly\\{filezipname_monthly[km]}"
				km += 1
				# 'infolist()' is the object of 'ZipFile' class
				# 'infolist()' returns a list containing all the folders and files of the zip -> 'ZipInfo' objects
				# assigning last element of the list to a variable to Tests all the methods of 'ZipInfo'
				archive_monthly = file2.infolist()
				read_me_file_monthly = archive_monthly[-4]
				#print("read_me_file=",read_me_file)
				# 'ZipInfo' methods
				# ZipInfo_object.filename returns the name of the file
				namefiletxt_monthly = format(read_me_file_monthly.filename)
				# ZipInfo_object.file_size returns the size of the file
				#print("Size of the file:- {}".format(read_me_file.file_size))
				# ZipInfo_object.is_dir() returns True if it's directory otherwise False
				# ZipInfo_object.date_time() returns the created date & time of file
				modimonth2 = int(format(read_me_file_monthly.date_time[1]))
				modiyear2 = int(format(read_me_file_monthly.date_time[0]))
				if modimonth2 == month and modiyear2 == year:
					filetxtname_pass_monthly.append(namefiletxt_monthly)
					path_name_monthly.append(path_monthly)
					print("PassMonth")
				else:
					print("not PassMonth")
	return filetxtname_pass_monthly,path_name_monthly
def createFolder(directory):
		try:
			if not os.path.exists(directory):
				os.makedirs(directory)
		except OSError: print('Error: Creating directory. ' +  directory)
def detect_month_num(week_real,month_real,yaer_real,passedText_monthly,pathma_monthly):
	monthy = int(month_real)
	yeary = yaer_real
	passfile_list_monthly = passedText_monthly
	path_file_monthly = pathma_monthly
	month_dict = { 1:"JAN" , 2 : "FEB", 3:"MAR", 4:"APR", 5 : "MAY", 6 :"JUNE", 7 :"JULY", 8 : "AUG" , 9:"SEP", 10:"OCT" , 11:"NOV" ,12:"DEC"}
	if monthy == 1:
		checked_month = month_dict.get(12)
	else:
		checked_month = month_dict.get(monthy-1)
	pass_status_monthly = []
	for k2 in range(len(passfile_list_monthly)):
		with zipfile.ZipFile(f"{path_file_monthly[k2]}") as zipjo:
			listOfFileNames_monthly = zipjo.namelist()
			for m2 in range(len(listOfFileNames_monthly)):
				if listOfFileNames_monthly[m2].endswith('.txt'):
					zipjo.extract(listOfFileNames_monthly[m2],"N:\\Rf3db\\Rtdb\\Chain\\Big C\\SFF\\ForExtract_file_monthly")
		f22 = open(f"N:\\Rf3db\\Rtdb\\Chain\\Big C\\SFF\\ForExtract_file_monthly\\{passfile_list_monthly[k2]}", "r")
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
	return pass_status_monthly,passfile_list_monthly
def excel_summary_month(filenamemonth,status_new_monthly,passnamefile_monthly,path_sff_monthly):
	status_monthly = status_new_monthly
	nameFile_to_excel_monthly = passnamefile_monthly
	path_monthly = path_sff_monthly
	name_M = int(filenamemonth)
	month_dict = { 1:"JAN" , 2 : "FEB", 3:"MAR", 4:"APR", 5 : "MAY", 6 :"JUNE", 7 :"JULY", 8 : "AUG" , 9:"SEP", 10:"OCT" , 11:"NOV" ,12:"DEC"}
	workbook = xlsxwriter.Workbook(f'N:\\Rf3db\\Rtdb\\Chain\\Big C\\SFF\\SFF_Summary_month_{month_dict.get(name_M)}_MONTHLY.xlsx')
	worksheet2 = workbook.add_worksheet('SUMMARY_SFF_File(monthly)')
	cell_format = workbook.add_format()
	cell_format.set_pattern(1)  # This is optional when using a solid fill.
	cell_format.set_bg_color('pink')
	worksheet2.write('A1', 'Status', cell_format)
	worksheet2.write('B1', 'FileName', cell_format)
	worksheet2.write('C1', 'Path', cell_format)
	worksheet2.write('D1', 'Month_data', cell_format)
	row = 1
	col = 0
	status_des_monthly = []
	for po in range(len(status_monthly)):
		if status_monthly[po] == 1:
			status_des_monthly.append("Pass")
		elif status_monthly[po] == 0:
			status_des_monthly.append("Fail")
	row2 = 1
	for ch in range(len(status_monthly)):
		worksheet2.write(row2, 0, status_des_monthly[ch])
		worksheet2.write(row2, 1, nameFile_to_excel_monthly[ch])
		#worksheet2.write(row2, 2, path_monthly[ch])
		worksheet2.write_url(f'C{row2+1}', f'N:\\Rf3db\\Rtdb\\Chain\\Big C\\SFF\\ForExtract_file_monthly\\{nameFile_to_excel_monthly[ch]}',string='check here')
		worksheet2.write(row2, 3, month_dict.get(name_M-1))
		row2 += 1
	workbook.close()