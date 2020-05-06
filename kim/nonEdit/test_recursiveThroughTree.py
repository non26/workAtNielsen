import os
def treeStructure(path, deep, space):
    deepLocal = deep
    deepNonLocal = deep
    spaceLocal = space
    spaceNonlocal = space
    for item in os.listdir(path):
        if os.path.isfile(path+"\\"+item):
            print(" "*spaceLocal+"|"+"-"*deepLocal, item)
        else:
            print(" "*spaceLocal+"|" + "-"*deepLocal, item)
            deepNonLocal += 2
            spaceNonlocal += 2
            treeStructure(path+"\\"+item, deepNonLocal, spaceNonlocal)
            deepNonLocal = deepLocal
            spaceNonlocal = spaceLocal


# print(os.listdir(r"C:\Users\EiCh9001\PycharmProjects\PyNielsen\WorkingOn\ProjectEuler"))
# r"X:\Databases\Monthly Retail Index"
treeStructure(r"C:\Users\EiCh9001\PycharmProjects\PyNielsen\AutoNAD_NEW_editting", 0, 0)
# l1 = list(range(10))
# for i in l1:
#     if i == 9:
#         l1.extend([10,11])
#     print(i)
