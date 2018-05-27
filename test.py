### This script runs first level stats on all valid runs for each subject
# It will loop through all subjects and runs
# Michelle Failla
# created 11-22-16

# import what is needed for the operating system
import os
# import glob which in this case helps match files in directories
import glob
# import time for adding to rerun templates
import time
#import csv for reading subject run list
import csv

# set up base directory and base subject directory
bDir = "/Users/Failla/Desktop/PIEC"
basesubjDir = bDir + "/Subjs"
subjfolder = bDir + "/Preprocessing/"

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
        # define if the subject has long or short design based on what their subject number is
        # subj is a string, converting to integer for math statement
        subjnum = int(subj)
        if subjnum < 212000:
            runtype = "Long"
            template = "/Users/Failla/Desktop/PIEC/Templates/1stLevelTemplate_Stats_180vols.fsf"
            number_confound_lines = 180

        else:
            runtype = "Short"
            template = "/Users/Failla/Desktop/PIEC/Templates/1stLevelTemplate_Stats_135vols.fsf"
            number_confound_lines = 135

        templateContent = open(template).read()

        # define anatomical directory for the subject, fsl will import proper anatomical image
        anatomical = baseanatDir + "/" + subj + ".anat/T1_biascorr_brain"

        # call the definitions from the dictionary
        run1 = Subjects_RunNumbers[str(subj)]['Run1']
        run2 = Subjects_RunNumbers[str(subj)]['Run2']
        run3 = Subjects_RunNumbers[str(subj)]['Run3']
        run4 = Subjects_RunNumbers[str(subj)]['Run4']
        # build a run list to loop through
        runlist = [run1, run2, run3, run4]
        # process by valid runs
        runcounter=1
        for runnumber in runlist:
            funcfile = subjfolder + subj + "_" + str(runnumber) + ".feat"
            if os.path.exists(funcfile):
                heart_timingfile = bDir + "/TimingFiles/" + runtype + "/run" + str(runcounter) + "heart.txt"
                visual_timingfile = bDir + "/TimingFiles/" + runtype + "/run" + str(runcounter) + "visual.txt"
                print heart_timingfile
                print visual_timingfile
                print anatomical
                print funcfile
                confoundfile = basesubjDir + "/" + subj + "/func/" + str(runnumber) + "/" + "FD_DVARS_MotionOutliers/FD_DVARS_common_outliers.txt"
                print confoundfile
                print template
                # Copy template and append new data to it
                date = time.strftime("%m%d%Y")
                newTemplateFile = "/Users/Failla/Desktop/PIEC/Templates/1stLevelSubj/" + subj + "_" + str(
                    runnumber) + "_" + date + ".fsf"
                with open(newTemplateFile, "a") as newTemplate:
                    newTemplate.write(templateContent)
                    newTemplate.write("set fmri(outputdir) " + '"' + output + '"' + "\n")
                    newTemplate.write("set feat_files(1) " + '"' + funcfile + '"' + "\n")
                    newTemplate.write("set highres_files(1) " + '"' + anatomical + '"' + "\n")
                    newTemplate.write("set confoundev_files(1) " + '"' + confoundfilenew + '"' + "\n")
                    newTemplate.write("set fmri(custom1) " + '"' + heart_timingfile + '"' + "\n")
                    newTemplate.write("set fmri(custom2) " + '"' + visual_timingfile + '"' + "\n")

                os.system("feat " + newTemplateFile)
            else:
                print "Subject %s:" %subj + " Run %r" %runcounter + " does not exist. Feat directory not found. Not calculating stats."
            runcounter += 1