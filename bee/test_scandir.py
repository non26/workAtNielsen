import os
path = r"C:\Users\EiCh9001\PycharmProjects\PyNielsen\Chapter8_GUI"
with os.scandir(path) as it:
    for entry in it:
        if not entry.name.startswith('.') and entry.is_file():
            print(entry)
            print(format("{0}"))