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
