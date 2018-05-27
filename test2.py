### This script runs second level analysis on all valid runs for each subject
# It will loop through all subjects and runs and combine into a second level model
# for each individual subject
# Michelle Failla
# created 11-22-16

# import what is needed for the operating system
import os
# import glob which in this case helps match files in directories
import glob

#import csv for reading subject run list
import csv

# set up base directory and base subject directory
bDir = "/Users/Failla/Desktop/PIEC"
basesubjDir = bDir + "/Subjs"
subjfolder = bDir + "/Preprocessing/"
baseanatDir = bDir + "/Anat_Level/"

# get list of subject files (all files in subject directory)
subject_files = [os.path.basename(x) for x in glob.glob(basesubjDir + "*/*")]
# get list to compare to - only subjects that have valid runs (to exclude certain subjects)
subjects_to_process = open("/Users/Failla/Desktop/PIEC/Scripts/subjectlist_postconfound.txt").read()

# define subjects and their runs that warrant processing (to exclude certain runs)
# this code creates a dictionary that we can look up what each run number is for each subject
Subjects_RunNumbers = {}
with open ('/Volumes/psr/Failla/PIEC/DesktopBackup/subjectsandruns_confoundex_11-22-16.csv', 'rU') as subject_run_file:
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
        output = bDir + "/SecondLevel/" + subj + ".feat"

        # call the definitions from the dictionary
        run1 = Subjects_RunNumbers[str(subj)]['Run1']
        run2 = Subjects_RunNumbers[str(subj)]['Run2']
        run3 = Subjects_RunNumbers[str(subj)]['Run3']
        run4 = Subjects_RunNumbers[str(subj)]['Run4']

        # build valid run list
        runlist = []
        if run1:
            runlist.append(run1)
        if run2:
            runlist.append(run2)
        if run3:
            runlist.append(run3)
        if run4:
            runlist.append(run4)

        # get number of runs
        runlistlength = len(runlist)
        print "Subject %s " %subj + "has %r" %runlistlength

        # set counter to be able to know which run you're in (run 1,2,3,4)
        # this is important for timing files
        if runlistlength == 1 :
            template = "/Users/Failla/Desktop/PIEC/Templates/2ndLevelTemplate_1run.fsf"
            templateContent = open(template).read()
            funcfile1 = subjfolder + subj + "_" + run1 + ".feat"
            print template
            print funcfile1

        if runlistlength == 2 :
            template = "/Users/Failla/Desktop/PIEC/Templates/2ndLevelTemplate_2runs.fsf"
            templateContent = open(template).read()
            funcfile1 = subjfolder + subj + "_" + run1 + ".feat"
            funcfile2 = subjfolder + subj + "_" + run2 + ".feat"
            print template
            print funcfile1
            print funcfile2


        if runlistlength == 3 :
            template = "/Users/Failla/Desktop/PIEC/Templates/2ndLevelTemplate_3runs.fsf"
            templateContent = open(template).read()
            funcfile1 = subjfolder + subj + "_" + run1 + ".feat"
            funcfile2 = subjfolder + subj + "_" + run2 + ".feat"
            funcfile3 = subjfolder + subj + "_" + run3 + ".feat"
            print template
            print funcfile1
            print funcfile2
            print funcfile3


        if runlistlength == 4 :
            template = "/Users/Failla/Desktop/PIEC/Templates/2ndLevelTemplate_4runs.fsf"
            templateContent = open(template).read()
            funcfile1 = subjfolder + subj + "_" + run1 + ".feat"
            funcfile2 = subjfolder + subj + "_" + run2 + ".feat"
            funcfile3 = subjfolder + subj + "_" + run3 + ".feat"
            funcfile4 = subjfolder + subj + "_" + run4 + ".feat"

            print template
            print funcfile1
            print funcfile2
            print funcfile3
            print funcfile4

    else:
        print "Subject %s does not have valid first level. Not processed." % subj

