import pandas as pd

def skipRowNotNull(pathNadFile, checkColumn = 1 ,startRow=0):
    nadContent = pd.read_excel(pathNadFile
                               , sheet_name="WSP_Sheet1"
                               , skiprows=[i for i in range(startRow)])
    for row in range(len(nadContent)):
        null = nadContent.iloc[:, checkColumn].at[row]
        if str(null) != "nan":
            startRow += 1
        else:
            break
    return startRow

def skipRowNull(pathNadFile, checkColumn=1, startRow=0):
    nadContent = pd.read_excel(pathNadFile
                               , sheet_name="WSP_Sheet1"
                               , skiprows=[i for i in range(startRow)])
    for row in range(len(nadContent)):
        null = nadContent.iloc[:, checkColumn].at[row]
        if str(null) == "nan":
            startRow += 1
        else:
            break
    return startRow
# pathNadFile = r"C:\nonContent\workAtNielsen\paralle\Koi\Weekly\KAD Tops\BEER-ST06700.xlsx"
pathNadFile = r"C:/nonContent/workAtNielsen/paralle/Koi/Weekly/KAD Tops\LIQ_MILK-ST00410.xlsx"
skipRow = 1
skipRow = skipRowNull(pathNadFile, 2, skipRow) + 1 # +1 is meant for header
skipRow = skipRowNotNull(pathNadFile, 2, skipRow)
skipRow = skipRowNull(pathNadFile, 2, skipRow) + 1 # +1 is meant for header
nadContent = pd.read_excel(pathNadFile
                           , sheet_name="WSP_Sheet1"
                           , skiprows=[i for i in range(skipRow)])
nadContent.rename(columns={nadContent.columns[0]: "MBD", nadContent.columns[1]: "period"}, inplace=True)
nadContent.iloc[0:15, 0] = nadContent.iloc[:, 0].fillna(method="ffill")
print(nadContent)