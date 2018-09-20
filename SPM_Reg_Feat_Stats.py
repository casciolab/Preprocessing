### This script will run any files that have been registered in SPM
# Files now need to run through first level stats
# It will loop through all subjects and runs
# Michelle Failla
# created 8-29-2018 with new High Pass Filter of 300, Cue Modeling, Axial T1s, and SPM Registration

# import what is needed for the operating system
import os
# import glob which in this case helps match files in directories
import glob2
# import time for adding to rerun templates
import time
# import csv for reading subject run list
import csv
# for copying files
import shutil

# set up base directory and base subject directory
bDir = "/Users/Failla/Desktop/PIEC"
# this is needed to find FD DVARS confound files
basesubjDir = bDir + "/Subjs"
# where your first levels are
axial_folder = bDir + "/300HPF/Axial/FirstLevel_SPMReg/"
# where your old anatomicals are
# NOTE - I'm not sure we need this, but I left it in b/c thats how my old analysis was
anat_axial_folder = bDir + "/Axial_Anat/"
# where you stored your SPM registrations
reg_directory = "/Users/Failla/Desktop/PIEC/300HPF/SPM_Reg/SPM_Reg"

# define subjects and their runs that warrant processing (to exclude certain runs)
# this code creates a dictionary that we can look up what each run number is for each subject
Subjects_RunNumbers = {}
with open ('/Volumes/psr/Failla/PIEC/DesktopBackup/subjectsandruns_confound_7-1-18.csv', 'rU') as subject_run_file:
    subject_run_data = csv.reader(subject_run_file, delimiter=',')
    next(subject_run_data, None)  # Skip header
    for row in subject_run_data:
        Subjects_RunNumbers[row[0]] = {}
        Subjects_RunNumbers[row[0]]['Run1'] = row[1]
        Subjects_RunNumbers[row[0]]['Run2'] = row[2]
        Subjects_RunNumbers[row[0]]['Run3'] = row[3]
        Subjects_RunNumbers[row[0]]['Run4'] = row[4]

# this is all the folders that have viable filtered and registered data in your SPM folder
spm_reg_dirs = glob2.glob(reg_directory + '/**/filtered_func_data_warped_noNANs.nii.gz')
# loop through files
for reg_dir in spm_reg_dirs:
    print "Checking %r" % reg_dir
    # check that the directory exists
    if os.path.exists(reg_dir):
        subj_run = reg_dir.split("/")[8]
        subj = subj_run.split("_")[0]
        run = subj_run.split("_")[1]
        print subj_run
        print "File exists: Filtered Func Data Warped with no NANs"
        # will need to replace the new filtered func data from our registration with the old one in the first level feat
        axial_first_level = axial_folder + subj_run + ".feat/filtered_func_data.nii.gz"
        # check for a stats log - only want to run first level feats that need new stats
        stats_log_file = axial_folder +subj_run + ".feat/stats/logfile"
        print "Checking for Stats Log"
        if not os.path.exists(stats_log_file):
            print "No Stats Log found in feat directory, running Stats"
            # copy new filtered and registered func data over to feat directory
            shutil.copy(reg_dir,axial_first_level)
            mean_func = axial_folder + subj_run + ".feat/mean_func.nii.gz"
            mask = axial_folder + subj_run + ".feat/mask"
            mask_mask = axial_folder + subj_run + ".feat/mask_mask.nii.gz"
            # need to make new mean_func images and masks off of the new filtered func data
            os.system("fslmaths " + axial_first_level + " -Tmean " + mean_func)
            os.system("bet2 " + mean_func + " " + mask + " -f 0.3 -n -m; immv " + mask_mask + " " + mask)
            # define if the subject has long or short design based on what their subject number is
            # subj is a string, converting to integer for math statement
            subjnum = int(subj)
            if subjnum < 130269:
                runtype = "Short"
                template = "/Users/Failla/Desktop/PIEC/300HPF/Templates/1stLevelTemplate_Stats_135vols_Cue.fsf"
                number_confound_lines = 135
            else:
                if subjnum < 212000:
                    runtype = "Long"
                    template = "/Users/Failla/Desktop/PIEC/300HPF/Templates/1stLevelTemplate_Stats_180vols_Cue.fsf"
                    number_confound_lines = 180

                else:
                    runtype = "Short"
                    template = "/Users/Failla/Desktop/PIEC/300HPF/Templates/1stLevelTemplate_Stats_135vols_Cue.fsf"
                    number_confound_lines = 135

            templateContent = open(template).read()

            # define anatomical directory for the subject, fsl will import old anatomical image
            anatomical = anat_axial_folder + subj + ".anat/T1_biascorr_brain"

            # process by run
            runnumber = Subjects_RunNumbers[str(subj)].keys()[Subjects_RunNumbers[str(subj)].values().index(str(run))]
            run_order_num = runnumber.split('Run')[1]
            heart_timingfile = bDir + "/TimingFiles/NewModel/" + runtype + "/run" + run_order_num + "heart.txt"
            visual_timingfile = bDir + "/TimingFiles/NewModel/" + runtype + "/run" + run_order_num + "visual.txt"
            print heart_timingfile
            print visual_timingfile
            print anatomical
            funcfile = bDir + "/300HPF/Axial/FirstLevel_SPMReg/" + subj + "_" + str(run) + ".feat"
            print funcfile

            confoundfilenew = basesubjDir + "/" + subj + "/func/" + str(
                    runnumber) + "/" + "FD_DVARS_MotionOutliers/FD_DVARS_common_outliers.txt"

            if not os.path.isfile(confoundfilenew):
                confoundfilenew = ""
            output = bDir + "/300HPF/Axial/FirstLevel_SPMReg/" + subj + "_" + str(run) + ".feat"
            print output
            print template

            # Copy template and append new data to it
            date = time.strftime("%m%d%Y")
            newTemplateFile = "/Users/Failla/Desktop/PIEC/300HPF/Templates/1stLevelSubj/Stats/" + subj + "_" + str(
                    run) + "_" + date + ".fsf"

            with open(newTemplateFile, "a") as newTemplate:
                newTemplate.write(templateContent)
                newTemplate.write("set fmri(outputdir) " + '"' + output + '"' + "\n")
                newTemplate.write("set feat_files(1) " + '"' + funcfile + '"' + "\n")
                newTemplate.write("set highres_files(1) " + '"' + anatomical + '"' + "\n")
                newTemplate.write("set confoundev_files(1) " + '"' + confoundfilenew + '"' + "\n")
                newTemplate.write("set fmri(custom1) " + '"' + heart_timingfile + '"' + "\n")
                newTemplate.write("set fmri(custom2) " + '"' + visual_timingfile + '"' + "\n")

            os.system("feat " + newTemplateFile)