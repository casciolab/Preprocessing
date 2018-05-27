### This script takes the anatomical T1s
# and runs fsl_anat on them
# It will loop through all subjects
# Michelle Failla
# Updated 06-15-17

# import what is needed for the operating system
import os
# import glob which in this case helps match files in directories
import glob
# for copying files
import shutil

# set up base directory, base subject directory, and base anatomical directory
bDir = "/Users/Failla/Desktop/PIEC"
basesubjDir = bDir + "/Subjs"
baseanatDir = bDir + "/AnatLevel"

# get list of subjects to process (all files in subject directory)
subjlist = [os.path.basename(x) for x in glob.glob(basesubjDir + "*/*")]

# define subjects to rerun list if you only want to run specific subjects
adultrerun = open("/Users/Failla/Desktop/PIEC/Scripts/anat_recover_4-30-18b").read()

# process by subject
for subj in subjlist:
    if subj in adultrerun:
        # define folder where the functional images are found, organized by run
        # subjfolder = basesubjDir + "/" + subj + "/func"

        # define anatomical directory for the subject, fsl will import proper anatomical image
        anatomical = basesubjDir + "/" + subj + "/anat/T1.nii.gz"

        # define anatomical output directory
        output = bDir + "/AnatLevel/" + subj

        # run fsl_anat
        os.system("fsl_anat -i " + anatomical + " -o " + output + " --nosubcortseg")

        # copy and move new file for use in first level processing
        new_biascorr_T1 = output + ".anat/T1_biascorr_brain.nii.gz"
        anatomical_moved = basesubjDir + "/" + subj + "/anat/T1_2MNI_brain.nii.gz"
        shutil.copy(new_biascorr_T1, anatomical_moved)
