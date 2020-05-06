import pandas as pd
import numpy as np
# fileNAD = "BABY_SUP-RM18107.xlsx"
# df1 = pd.DataFrame(pd.read_excel(fileNAD, skiprows=[i for i in range(2)]))
# df1.rename(columns={df1.columns[0]: "MBD", df1.columns[1]: "period"}, inplace=True)
# df1["number"] = np.arange(0, len(df1))
# new_row = {col: index for index, col in enumerate(df1.columns)}
# df1 = df1.append(new_row, ignore_index=True)
# print(df1)
fileNAD = "BREK_CER-RM05830.xlsx"
sheetName = None
df1 = pd.DataFrame(pd.read_excel(fileNAD, skiprows=[i for i in range(2)]))
print(list(df1.columns))
