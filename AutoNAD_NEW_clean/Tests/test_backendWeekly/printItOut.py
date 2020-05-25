import pandas as pd
import numpy as np
fileNAD = "BIRD_NET-ST04900.xlsx"
sheetName="WSP_Sheet1"
df1 = pd.DataFrame(pd.read_excel(fileNAD, skiprows=[i for i in range(3)], sheet_name=sheetName))
df1.rename(columns={df1.columns[0]: "MBD", df1.columns[1]: "period"}, inplace=True)
df1.iloc[0:15, 0] = df1.iloc[:, 0].fillna(method="ffill")
df1["number"] = np.arange(0, len(df1))
print(df1)