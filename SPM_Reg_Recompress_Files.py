### This script will recompress any nii files used in SPM
# It will loop through all subjects and runs
# Michelle Failla
# created 8-29-2018 with new High Pass Filter of 300, Cue Modeling, Axial T1s, and SPM Registration

# import what is needed for the operating system
import os
# import glob which in this case helps match files in directories
import glob2
# find all files to compress
files_compress = glob2.glob('/Users/Failla/Desktop/PIEC/300HPF/SPM_Reg/SPM_Reg/' + '**/*.nii')
# loop through all these files
for file in files_compress:
    subj_run = file.split('/')[8]
    real_dir = "/Users/Failla/Desktop/PIEC/300HPF/SPM_Reg/SPM_Reg/" + subj_run
    print real_dir
    noNANs_file = real_dir + "/filtered_func_data_warped_noNANs.nii.gz"
    # only compress files if the noNANs file exists
    if os.path.exists(noNANs_file):
        print noNANs_file
        # change directory
        os.chdir(real_dir)
        # compress all nii in the directory to nii.gz
        os.system("gzip *.nii")

