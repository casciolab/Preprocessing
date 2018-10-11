### This script will take all masks from your SPM registrations
# put them all into a FSL timeseries
# should allow you to check if any are way out of registration
# Michelle Failla
# created 10-1-18

# for working with system
import os
# for finding files
import glob2
# for copying files
import shutil

first_level_dir = "/Users/Failla/Desktop/PIEC/300HPF/SPM_Reg/SecondLevel"
mask_files = glob2.glob(first_level_dir + '/*feat/mask.nii.gz')
QA_dir = "/Users/Failla/Desktop/PIEC/300HPF/SPM_Reg/QA/SecondLevelMasks/"


for mask in mask_files:
    subj_run = mask.split("/")[8]
    subj_run_only = subj_run.split(".")[0]
    new_mask_loc = QA_dir + subj_run_only + "_mask.nii.gz"
    shutil.copy(mask,new_mask_loc)


os.chdir(QA_dir)

os.system("fslmerge -t secondlevelmasks.nii.gz *mask.nii.gz")

