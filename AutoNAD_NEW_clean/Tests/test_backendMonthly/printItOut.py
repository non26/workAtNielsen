import pandas as pd
fileNAD = r"C:\nonContent\workAtNielsen\projectAtNielsen\formatNAD_afterLeave1\CANDY-RM04400.xlsx"
skipRow = 3
sheetName = "WSP_Sheet1"
if sheetName:
    df1 = pd.DataFrame(pd.read_excel(fileNAD, skiprows=[i for i in range(skipRow)], sheet_name=sheetName))
else:
    df1 = pd.DataFrame(pd.read_excel(fileNAD, skiprows=[i for i in range(skipRow)]))
# df1.rename(columns={df1.columns[0]:"MBD", df1.columns[1]:"MBDCode", df1.columns[2]:"period"}, inplace=True)
df1.rename(columns={df1.columns[0]: "MBD", df1.columns[1]: "MBDCode"}, inplace=True)
print(df1)
print(df1["MBD"].to_list())
print(df1["MBDCode"].to_list())
l1 = [x for x in df1["MBDCode"].to_list() if str(x) != "nan"]
length = len(l1)
print(df1["MBD"].to_list()[:length])
print(l1)
