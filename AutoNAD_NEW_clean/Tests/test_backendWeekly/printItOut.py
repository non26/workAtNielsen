from workAtNielsen.projectAtNielsen.AutoNAD_NEW_clean.Tests.test_backendWeekly import test_weekly

# import pandas as pd
# nadContent = pd.DataFrame(pd.read_excel("BIRD_NET-ST04900.xlsx"
#                                    , sheet_name="WSP_Sheet1"
#                                    , skiprows=[i for i in range(35)]))
                                   # , header = None)
# checkColumn = 2
# startRow = 0
# for row in range(len(nadContent)):
#     null = nadContent.iloc[:, checkColumn].at[row]
#     if str(null) == "nan":
#         startRow += 1
#     else:
#         break
# checkColumn = 2
# startRow = 0
# for row in range(len(nadContent)):
#     null = nadContent.iloc[:, checkColumn].at[row]
#     if str(null) != "nan":
#         startRow += 1
#     else:
#         break
# print(nadContent)
# print(startRow)
print(test_weekly.__name__)