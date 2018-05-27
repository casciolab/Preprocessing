# import what is needed for the operating system
import os
# import glob which in this case helps match files in directories
import glob
# for copying files
import shutil


# set up base directory, base subject directory, and base anatomical directory
bDir="/Users/Failla/Desktop/PIEC"
basesubjDir=bDir + "/Subjs"

# get list of subjects to process (all files in subject directory)
subjlist=[os.path.basename(x) for x in glob.glob(basesubjDir + "*/*")]

# process by subject
for subj in subjlist:

    anatomical = basesubjDir + "/" + subj + "/anat/T1.nii.gz"

    farb_move_anat = bDir + "/Anatomicals_ToFarb/" + subj + "_T1.nii.gz"

    print anatomical
    print farb_move_anat

    # copy and move new file for use in first level processing
    if os.path.isfile(anatomical):
        shutil.copy(anatomical, farb_move_anat)
    else:
        print "%s does not have an anatomical scan." % subj