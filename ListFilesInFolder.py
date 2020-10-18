import os
path=r"Z:/GIO/CIP_2018/2018_Data/Processed_GDBs"
for dirpath, dirnames, filenames in os.walk(path):
    for f in filenames:
        print f
print len(filenames)

#80
