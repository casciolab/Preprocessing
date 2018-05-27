### This script creates a summary of all confound files
### to evaluate the % of volumes dropped
### We will want to drop runs where FD/DVARS are dropping over 10% of volumes (just too much motion)
### It will loop through all subjects and runs that are valid
### Michelle Failla
### Last Updated 06-16-17

# import what is needed for the operating system
import os
# import glob which in this case helps match files in directories
import glob
#import csv for reading subject run list
import csv

# write total spikes for each subject and run to a csv file
summary_spike_file = "/Volumes/psr/Failla/PIEC/DesktopBackup/summary_spike_file_5-1-18.csv"

# set up base directory, base subject directory, and base anatomical directory
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
            confound_dir = basesubjDir + "/" + subj + "/func/" + str(runnumber) + "/FD_DVARS_MotionOutliers/"
            confoundfile = confound_dir + "FD_DVARS_common_outliers.txt"
            if os.stat(confoundfile).st_size == 0:
                num_cols = 0
            else:
                with open(confoundfile) as f:
                    reader = csv.reader(f, delimiter=' ', skipinitialspace=True)
                    first_row = next(reader)
                    num_cols = len(first_row)

            with open(summary_spike_file, 'a') as csvfile:
                spikewriter = csv.writer(csvfile, quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spikewriter.writerow([subj, runnumber, num_cols])
