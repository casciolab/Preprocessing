# import what is needed for the operating system
import os
# import glob which in this case helps match files in directories
import glob
# set up base directory, base subject directory, and base anatomical directory
bDir="/Users/Failla/Desktop/PIEC"
basesubjDir=bDir + "/Subjs"
baseanatDir=bDir + "/Anat_Level"

# get list of subjects to process (all files in subject directory)
subjlist=[os.path.basename(x) for x in glob.glob(basesubjDir + "*/2*")]

# process by subject
for subj in subjlist:

    subjfolder = bDir + "/Preprocessing/"
    # generate run list for this subject based on all func images *.nii.gz
    runlist = glob.glob(subjfolder + str(subj) + "*.feat")

    runnumberlist = []
    for run in runlist:
        if not os.path.isdir(run + "/stats"):
            print "%s does not have a stats directory." % run
        else:
            print "%s has been processed." % run
