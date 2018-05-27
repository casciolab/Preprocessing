### This script organizes files downloaded in batch from xnat
# Michelle Failla
# Last Updated 11-21-16

# import what is needed for the operating system
import os
# import glob which in this case helps match files in directories
import glob
# import fnmatch for filename matching
import fnmatch
# import shutil for copying files
import shutil

# set up xnat directory, base directory, base subject directory
xnatdirectory = "/Users/Failla/Desktop/PIEC/Xnat/Subjs/PIEC_11-17-16/PIEC"
bDir = "/Users/Failla/Desktop/PIEC"
basesubjDir = bDir + "/Subjs"

# get list of subjects to process (all files in subject directory)
subjlist = [os.path.basename(x) for x in glob.glob(xnatdirectory + "*/*")]

# define possible anatomical runs
# in xnat they are either run 303 or 403 depending on the scan
PossibleT1_labels=['*303*','*403*']

# process by subject
for subj in subjlist:
    # define the directory for the T1 and functional runs are
    Scan_directory = xnatdirectory + "/" + subj + "/" + subj
    # define where we will be moving the T1 (anat) and functional runs (func)
    # make those directories if they don't exist
    anatdir = basesubjDir + "/" + subj + "/anat/"
    if not os.path.exists(anatdir):
        os.makedirs(anatdir)
    funcdir = basesubjDir + "/" + subj + "/func/"
    if not os.path.exists(funcdir):
        os.makedirs(funcdir)

    # now, search through the scan directory and all sub directories and filenames
    # for matches to the PossibleT1 list, to find the T1
    T1_scan = []
    for root, dirnames, filenames in os.walk(Scan_directory):
        for T1number in PossibleT1_labels:
            for filename in fnmatch.filter(filenames, T1number):
                T1_scan.append(os.path.join(root, filename))
    # define where we'd like to move the T1
    T1_scan_moved = anatdir + "T1.nii.gz"
    # get the length of the T1_scan list, if it's greater than 0 (ie. not empty
    # then we found the T1 and we can copy it and rename it
    totalT1 = len(T1_scan)
    if totalT1 > 0:
        # the T1 is listed here
        T1_scan_str = T1_scan[0]
        # copy the file and rename it
        shutil.copy(T1_scan_str, T1_scan_moved)

    # now we will do a similar search for functional runs
    # xnat downloads them into separate directories, so need to find the directories and then files
    functionalruns = []
    functionalrun_directory = []
    # this searches through the directory and all sub directories and filenames for EPI directories
    for root, dirnames, filenames in os.walk(Scan_directory):
        for dirname in fnmatch.filter(dirnames, "*EPI*"):
            functionalrun_directory.append(Scan_directory + "/" + dirname)
    # now search through all the directories for nifti files
    for directory in functionalrun_directory:
        for root, dirnames, filenames in os.walk(directory):
            for filename in fnmatch.filter(filenames, "*.nii.gz"):
                functionalruns.append(directory + "/NIFTI/" + filename)

    # getting total functional runs from length of functional run list
    totalfuncruns = len(functionalruns)
    # now loop through the functional run list and move them
    funcruncounter = 0
    for funcfile in functionalruns:
        if funcruncounter < totalfuncruns:
            run_number_section = funcfile.split('/')[11]
            run_number = run_number_section.split('-')[0]
            funcfile_moved = funcdir + run_number + ".nii.gz"
            shutil.copy(funcfile, funcfile_moved)
        funcruncounter += 1

    # this makes a list of exactly the files moved and called for each T1 and functional runs
    # just in case there is any question or issue later
    scanlist = "/Users/Failla/Desktop/PIEC/Xnat/Subjs/PIEC_11-17-16/scanlist.txt"
    with open(scanlist, "a") as newScanList:
        newScanList.write(subj + ",")
        newScanList.write(str(T1_scan))
        newScanList.write(",")
        newScanList.write(str(functionalruns))
        newScanList.write("\n")
