### This script will take all the filtered func data from first level and register them into MNI through SPM
# It will loop through all subjects and runs
# Michelle Failla
# created 8-29-2018 with new High Pass Filter of 300, Cue Modeling, Axial T1s, and SPM Registration

# import what is needed for the operating system
import os
# import glob which in this case helps match files in directories
import glob
import glob2
# import shutil for copying files
import shutil

# set up base directory and base subject directory
bDir = "/Users/Failla/Desktop/PIEC"
# this is where you have saved the warps from xnat, usually in an xnat download file structure
warp_folder = bDir + "/Xnat/Warps/PIEC"
# this is the first level folder where you have run the first part of the first level, up to stats
axial_folder = bDir + "/300HPF/Axial/FirstLevel_SPMReg"
# this folder has the anatomical T1 in subject space (and is axial)
subj_folder = bDir + "/Subjs/"
# this folder is where you will save the SPM registrations
reg_directory = "/Users/Failla/Desktop/PIEC/300HPF/SPM_Reg/SPM_Reg"

# get list of all first levels you need to register to MNI
subject_files = [os.path.basename(x) for x in glob.glob(axial_folder + "*/*")]

# loop through first level files
for subj in subject_files:
    subj_run = subj.split('.')
    new_dir = reg_directory + "/" + subj_run[0]
    # check to make sure the directory of your registration doesn't exist
    # set up so that you can rerun script if you get new subjects, but if one fails in the middle
    # may need to rerun manually
    if not os.path.exists(new_dir):
        # make directory
        os.makedirs((new_dir))
        print new_dir
        # find filtered func from first level pre-stats folder
        filtered_func_old = axial_folder + "/" + subj + "/filtered_func_data.nii.gz"
        # set new path for filtered func
        filtered_to_process = new_dir + "/filtered_func_data.nii.gz"
        # copy filtered func
        shutil.copy(filtered_func_old, filtered_to_process)
        print "Copied Filtered Func"
        subj_num = subj_run[0].split('_')
        subj_number = subj_num[0]
        # set path for warp and mat file
        # will need both for SPM registration
        warp_file = glob2.glob(warp_folder + "/" + subj_number + "/**/y_csrc_sn.nii.gz")
        mat_file = glob2.glob(warp_folder + "/" + subj_number + "/**/initial_coreg_mat.txt")
        # also need anatomical to register it in SPM
        anatomical = subj_folder + subj_number + "/anat/T1_axial.nii.gz"
        # set new paths for matrix, warp, and T1
        new_mat = new_dir + "/initial_coreg_mat.txt"
        new_T1 = new_dir + "/T1_axial.nii.gz"
        new_warp = new_dir + "/y_csrc_sn.nii.gz"
        # if the mat file exists
        # then copy mat file, warp file
        # sometimes they dont exist in xnat so this prevents the script from failing
        if mat_file:
            shutil.copy(mat_file[0], new_mat)
            shutil.copy(warp_file[0], new_warp)
            print "Copied mat and warp file"
        shutil.copy(anatomical, new_T1)
        print "Copied T1"
