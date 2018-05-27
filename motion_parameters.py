### This script creates takes the created confound files (FD and DVARS)
### and matches the spikes that are found in both files
### It will loop through all subjects and runs that are valid
### Michelle Failla
### Last Updated 06-16-17

# import what is needed for the operating system
import os
# import glob which in this case helps match files in directories
import glob
#import csv for reading subject run list
import csv
import pandas as pd

# set up base directory, base subject directory, and base anatomical directory
bDir = "/Users/Failla/Desktop/PIEC"
basesubjDir = bDir + "/Subjs"
subjfolder = "/Users/Failla/Desktop/PIEC/300HPF/FirstLevel/"

# get list of subject files (all files in subject directory)
subject_files = [os.path.basename(x) for x in glob.glob(basesubjDir + "*/*")]
# get list to compare to - only subjects that have valid runs (to exclude certain subjects)
subjects_to_process = open("/Users/Failla/Desktop/PIEC/Scripts/300hpf_rerun_stats_5-7-18").read()

# define subjects and their runs that warrant processing (to exclude certain runs)
# this code creates a dictionary that we can look up what each run number is for each subject
Subjects_RunNumbers = {}
with open ('/Volumes/psr/Failla/PIEC/DesktopBackup/subjectsandruns_confound_4-28-18.csv', 'rU') as subject_run_file:
    subject_run_data = csv.reader(subject_run_file, delimiter=',')
    next(subject_run_data, None)  # Skip header
    for row in subject_run_data:
        Subjects_RunNumbers[row[0]] = {}
        Subjects_RunNumbers[row[0]]['Run1'] = row[1]
        Subjects_RunNumbers[row[0]]['Run2'] = row[2]
        Subjects_RunNumbers[row[0]]['Run3'] = row[3]
        Subjects_RunNumbers[row[0]]['Run4'] = row[4]

motion_param_dict = {}
# process by subject and run
for subj in subject_files:
    if subj in subjects_to_process:
        # call the definitions from the dictionary
        run1 = Subjects_RunNumbers[str(subj)]['Run1']
        run2 = Subjects_RunNumbers[str(subj)]['Run2']
        run3 = Subjects_RunNumbers[str(subj)]['Run3']
        run4 = Subjects_RunNumbers[str(subj)]['Run4']
        # build a run list to loop through
        runlist = [run1,run2,run3,run4]
        # process by valid runs
        for runnumber in runlist:
            subj_run = subj + "_" + runnumber
            motion_file = subjfolder + subj_run + ".feat/mc/prefiltered_func_data_mcf.par"
            if os.path.isfile(motion_file):
                motion_param_dict[subj_run] = {}
                # define files to pull out data
                run_rot_x_list =[]
                run_rot_y_list =[]
                run_rot_z_list =[]
                run_trans_x_list =[]
                run_trans_y_list =[]
                run_trans_z_list =[]
                with open (motion_file, 'rU') as motion_param_file:
                    for line in motion_param_file:
                        linelist = line.split("  ")
                        run_rot_x_list.append(linelist[0])
                        run_rot_y_list.append(linelist[1])
                        run_rot_z_list.append(linelist[2])
                        run_trans_x_list.append(linelist[3])
                        run_trans_y_list.append(linelist[4])
                        run_trans_z_list.append(linelist[5])
                motion_param_dict[subj_run]['max_rot_x'] = abs(max((map(float, run_rot_x_list)), key=abs))
                motion_param_dict[subj_run]['max_rot_y'] = abs(max((map(float, run_rot_y_list)), key=abs))
                motion_param_dict[subj_run]['max_rot_z'] = abs(max((map(float, run_rot_z_list)), key=abs))
                motion_param_dict[subj_run]['max_trans_x'] = abs(max((map(float, run_trans_x_list)), key=abs))
                motion_param_dict[subj_run]['max_trans_y'] = abs(max((map(float, run_trans_y_list)), key=abs))
                motion_param_dict[subj_run]['max_trans_z'] = abs(max((map(float, run_trans_z_list)), key=abs))

motion_summary = pd.DataFrame.from_dict(motion_param_dict, orient="index")
motion_summary.to_csv('/Users/Failla/Desktop/PIEC/300HPF/Motion/motion_5-8-18.csv')
