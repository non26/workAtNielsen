import distutils.dir_util
import time
start = time.time()
distutils.dir_util.copy_tree(r"N:\Rf3db\Rtdb\Chain\Big C\SFF\Weekly", r"C:\Users\EiCh9001\PycharmProjects\PyNielsen\bee\nonModify\test_distutils\keep")
print("elapsed time:", time.time()-start)