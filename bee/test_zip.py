import zipfile
with zipfile.ZipFile(r"C:\Users\EiCh9001\PycharmProjects\PyNielsen\AutoNAD_NEW-20200106T025337Z-001.zip") as myzip:
        [print(item) for item in myzip.infolist()]
        [print(item.filename) for item in myzip.infolist()]