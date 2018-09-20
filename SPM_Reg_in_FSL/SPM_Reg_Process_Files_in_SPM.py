### This script will recompress any nii files used in SPM
# It will loop through all subjects and runs
# Michelle Failla
# created 8-29-2018 with new High Pass Filter of 300, Cue Modeling, Axial T1s, and SPM Registration

# for working with system
import os
# for finding files
import glob2
# for running matlab through python
import matlab.engine

# this is the folder where you are storing registrations through SPM
reg_directory = "/Users/Failla/Desktop/PIEC/300HPF/SPM_Reg/SPM_Reg"
# find all warp files available in registrations folder
spm_reg_dirs = glob2.glob(reg_directory + '/**/y_csrc_sn.nii*')

#loop through list of viable warp files/parent directories
for reg_dir in spm_reg_dirs:
    just_dir = reg_dir.split("y")
    real_dir = just_dir[0]
    noNANs_file = real_dir + "filtered_func_data_warped_noNANs.nii.gz"
    # change directory, it makes Matlab run better
    os.chdir(real_dir)
    # only run registration if there is no finished registration file (noNANS_file)
    if not os.path.exists(noNANs_file):
        print "No NAN file detected, beginning prep for SPM"
        # split filtered func in time
        os.system("fslsplit filtered_func_data func")
        print real_dir
        # unzip all volumes for SPM
        os.system("gunzip *gz")
        func_file_0 = real_dir + "func0000.nii"
        # if split and unzip was successful, run Matlab registration (see MatLab script for comments)
        if os.path.exists(func_file_0):
            print "File Split"
            print "Directory Unzipped"
            print "Running MatLab Registration and Normalization (SPM_xnat_registration_normalization)"
            eng = matlab.engine.start_matlab()
            eng.SPM_xnat_registration_normalization(real_dir,nargout=0)
            wcfunc_file_134 = real_dir + "wcfunc0134.nii"
            # if the wcfunc files exist, then SPM was likely successful, so then move on
            if os.path.exists(wcfunc_file_134):
                print "SPM Finished"
                # merge the wcfunc files back into a 4D volume
                os.system("fslmerge -tr filtered_func_data_warped.nii.gz wcfunc* 2")
                warped_data_file = real_dir + "filtered_func_data_warped.nii.gz"
                # if merge works, then move forward
                if os.path.exists(warped_data_file):
                    print "Warped Images Merged"
                    # SPM puts in NANs in the image, which FSL will not accept
                    # run command to change NANs to 0s
                    os.system("fslmaths filtered_func_data_warped.nii.gz -nan filtered_func_data_warped_noNANs.nii.gz")
                    # if successful, noNANs image exists, move forward
                    if os.path.exists(noNANs_file):
                        print "The NoNANs image was created"
                        # find unzipped files that we dont need anymore
                        unzipped_images_to_delete = glob2.glob(real_dir + '*func0*')
                        # loop through and delete these images - otherwise they will up your disk FAST
                        for image in unzipped_images_to_delete:
                            os.remove(image)
                        unzipped_images_remaining = glob2.glob(real_dir + '*func0*')
                        # check to make sure all of them are gone
                        if not unzipped_images_remaining:
                            print "Images Deleted"


