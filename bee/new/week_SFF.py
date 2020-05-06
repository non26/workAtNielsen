# monthpass is the month that user input
# yearpass is the year that user input
def GetFileweek(monthpass, yearpass):
    # filezipname = ["SFF_Bsicuit_yummy.zip","SFF_Baby_Sup_wk.zip","SFF_CON_MiLK_WK_PERRY.zip" ]
    month = int(monthpass)
    year = int(yearpass)

    obj = os.scandir(path='N:\\Rf3db\\Rtdb\\Chain\\Big C\\SFF\\Weekly')
    filezipname = []
    filetxtname_pass = []
    path_name = []

    i = 0
    for index, entry in enumerate(obj):
        if entry.name.endswith('ZIP') and entry.is_file():
            filezipname.append(str(entry.name))
            # stayedpath = os.path.commonpath(['c:/Users/TeNi9001', name])
            # filename = entry.name
            with zipfile.ZipFile(f"N:\\Rf3db\\Rtdb\\Chain\\Big C\\SFF\\Weekly\\{filezipname[i]}") as file:
                path = f"N:\\Rf3db\\Rtdb\\Chain\\Big C\\SFF\\Weekly\\{filezipname[i]}"
                i += 1
                # 'infolist()' is the object of 'ZipFile' class
                # 'infolist()' returns a list containing all the folders and files of the zip -> 'ZipInfo' objects
                # assigning last element of the list to a variable to Tests all the methods of 'ZipInfo'
                archive = file.infolist()
                read_me_file = archive[-4]
                # 'ZipInfo' methods
                # ZipInfo_object.filename returns the name of the file
                namefiletxt = format(read_me_file.filename)
                # ZipInfo_object.file_size returns the size of the file
                # ZipInfo_object.is_dir() returns True if it's directory otherwise False
                # ZipInfo_object.date_time() returns the created date & time of file
                modimonth = int(format(read_me_file.date_time[1]))
                modiyear = int(format(read_me_file.date_time[0]))

                if modimonth == month and modiyear == year:
                    filetxtname_pass.append(namefiletxt)
                    path_name.append(path)
                    print("Pass")
                else:
                    print("not pass")
    return filetxtname_pass, path_namec
def createFolder(directory):
	try:
		if not os.path.exists(directory):
			os.makedirs(directory)
	except OSError: print('Error: Creating directory. ' +  directory)
def detect_week_num(passedText,week_real,month_real,yaer_real,pathMa):

	passfile_list = passedText
	weeky = week_real
	monthy = int(month_real)
	yeary = yaer_real
	path_file = pathMa

	month_dict = { 1:"JAN" , 2 : "FEB", 3:"MAR", 4:"APR", 5 : "MAY", 6 :"JUNE", 7 :"JULY", 8 : "AUG" , 9:"SEP", 10:"OCT" , 11:"NOV" ,12:"DEC"}

	pass_status = []
	for k in range(len(passfile_list)):
		with zipfile.ZipFile(f"{path_file[k]}") as zip:
			listOfFileNames = zip.namelist()
			for m in range(len(listOfFileNames)):
				if listOfFileNames[m].endswith('.txt'):
					zip.extract(listOfFileNames[m],"N:\\Rf3db\\Rtdb\\Chain\\Big C\\SFF\\ForExtract_file_weekly")
		f = open(f"N:\\Rf3db\\Rtdb\\Chain\\Big C\\SFF\\ForExtract_file_weekly\\{passfile_list[k]}", "r")
		for x in f:
			detect = re.split(r'\s', x)
			for j in range(len(detect)):
				if detect[j] == f"W{weeky}{yeary.rstrip()[-2:]}":
					pass_status.append(1)
					break
				elif detect[j] != f"W{weeky}{yeary.rstrip()[-2:]}" and detect[j].endswith(f"{yeary.rstrip()[-2:]}") :
					pass_status.append(0)
					break
			else: continue
			break
	return pass_status,passfile_list

def excel_summary_week(filenamemonth, status_new, passnamefile, path_sff):
	status = status_new
	nameFile_to_excel = passnamefile
	path = path_sff
	name_M = int(filenamemonth)
	month_dict = { 1:"JAN" , 2 : "FEB", 3:"MAR", 4:"APR", 5 : "MAY", 6 :"JUNE", 7 :"JULY", 8 : "AUG" , 9:"SEP", 10:"OCT" , 11:"NOV" ,12:"DEC"}
	workbook = xlsxwriter.Workbook(f'N:\\Rf3db\\Rtdb\\Chain\\Big C\\SFF\\SFF_Summary_month_{month_dict.get(name_M)}_WEEKLY.xlsx')
	worksheet1 = workbook.add_worksheet('SUMMARY_SFF_File(weekly)')
	cell_format = workbook.add_format()
	cell_format.set_pattern(1)  # This is optional when using a solid fill.
	cell_format.set_bg_color('pink')
	worksheet1.write('A1', 'Status', cell_format)
	worksheet1.write('B1', 'FileName', cell_format)
	worksheet1.write('C1', 'Path', cell_format)
	row = 1
	col = 0
	status_des = []
	for r in range(len(status)):
		if status[r] == 1:
			status_des.append("Pass")
		elif status[r] == 0:
			status_des.append("Fail")
	# Iterate over the data and write it out row by row.
	for jd in range(len(status)):
		worksheet1.write(row, 0, status_des[jd])
		worksheet1.write(row, 1, nameFile_to_excel[jd])
		worksheet1.write_url(f'C{row+1}', f'N:\\Rf3db\\Rtdb\\Chain\\Big C\\SFF\\ForExtract_file_weekly\\{nameFile_to_excel[jd]}',string='check here')
		row += 1
	workbook.close()
