### This script creates confound files for each run
# It will loop through all subjects and runs that are valid
# and run FD and DVARS confounds for use in motion correction
# Michelle Failla
# created 06-13-17

# import what is needed for the operating system
import os
# import glob which in this case helps match files in directories
import glob
#import csv for reading subject run list
import csv

# set up base directory and base subject directory
bDir = "/Users/Failla/Desktop/PIEC"
basesubjDir = bDir + "/Subjs"

# get list of subject files (all files in subject directory)
subject_files = [os.path.basename(x) for x in glob.glob(basesubjDir + "*/*")]
# get list to compare to - only subjects that have valid runs (to exclude certain subjects)
subjects_to_process = open("/Users/Failla/Desktop/PIEC/Scripts/300hpf_rerun.txt").read()

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
            # define functional file for that run
            funcfile = basesubjDir + "/" + subj + "/func/" + str(runnumber) + ".nii.gz"
            # define output for the confound files
            output = basesubjDir + "/" + subj + "/func/" + str(runnumber) + "/FD_DVARS_MotionOutliers/"
            # check if the directory already exists, make it if it doesnt
            if not os.path.exists(output):
                os.makedirs(output)
            # define all the outputs for DVARS and FD confound files
            dvars_output = output + "dvars_confoundEV.txt"
            dvars_values = output + "dvars_metricvals.txt"
            dvars_graph = output + "dvars_graph.png"
            dvars_log = output + "dvars_processinfo.txt"
            fd_output = output + "fd_confoundEV.txt"
            fd_values = output + "fd_metricvals.txt"
            fd_graph = output + "fd_graph.png"
            fd_log = output + "fd_processinfo.txt"

            # check if the DVARS confound file exists, if not, run the FSL command to make DVARS confound file
            # this allows us to only process if necessary
            if not os.path.isfile(dvars_output):
                os.system("fsl_motion_outliers -i " + funcfile + " -o " + dvars_output + " --dvars -s " + dvars_values + " -p " + dvars_graph + " -v " + dvars_log)
            else:
                print "Already ran DVARS for %s" %subj + ": %r" %runnumber
            # only processing FD if necessary
            if not os.path.isfile(fd_output):
                os.system("fsl_motion_outliers -i " + funcfile + " -o " + fd_output + " --fd -s " + fd_values + " -p " + fd_graph + " -v " + fd_log)
            else:
                print "Already ran FD for %s" % subj + ": %r" % runnumber
