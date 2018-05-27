# import what is needed for the operating system
import os
# import glob which in this case helps match files in directories
import glob
import shutil


# set up base directory and base subject directory
bDir = "/Users/Failla/Desktop/PIEC"
subjfolder = bDir + "/Preprocessing/"

# get list of subject files (all files in subject directory)
subject_files = [os.path(x) for x in glob.glob(subjfolder + "*/2*")]

names_delete = open("/Users/Failla/Desktop/PIEC/Scripts/namelist").read()

for name in glob.glob(subjfolder + "/2*"):
    if name in names_delete:
        confound = name + "/confoundevs.txt"
        if os.path.exists(confound):
            print confound
            os.remove(confound)

