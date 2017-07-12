### This script runs preprocessing on all valid runs for each subject
# It will loop through all subjects and runs
# and run FD and DVARS confounds for use in motion correction
# Michelle Failla
# created 06-16-17

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
subjfolder = bDir + "/FirstLevel/"

# get list of subject files (all files in subject directory)
subject_files = [os.path.basename(x) for x in glob.glob(basesubjDir + "*/*")]
# get list to compare to - only subjects that have valid runs (to exclude certain subjects)
subjects_to_process = open("/Users/Failla/Desktop/PIEC/Scripts/anatrerunlist_06-15-2017.txt").read()

# define subjects and their runs that warrant processing (to exclude certain runs)
# this code creates a dictionary that we can look up what each run number is for each subject
Subjects_RunNumbers = {}
with open ('/Volumes/psr/Failla/PIEC/DesktopBackup/subjectsandruns_confoundex_06-15-17.csv', 'rU') as subject_run_file:
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
        subjnum=int(subj)
        if subjnum < 130269:
            runtype = "Short"
            template = "/Users/Failla/Desktop/PIEC/Templates/1stLevelTemplate_Preprocessing_135vols.fsf"
            number_confound_lines = 135
        else:
            if subjnum < 212000:
                runtype = "Long"
                template = "/Users/Failla/Desktop/PIEC/Templates/1stLevelTemplate_Preprocessing_180vols.fsf"
                number_confound_lines=180

            else:
                runtype = "Short"
                template = "/Users/Failla/Desktop/PIEC/Templates/1stLevelTemplate_Preprocessing_135vols.fsf"
                number_confound_lines = 135

        templateContent = open(template).read()

        # define anatomical directory for the subject, fsl will import proper anatomical image
        anatomical = bDir + "/Anat_Level/" + subj + ".anat/T1_biascorr_brain.nii.gz"

        # call the definitions from the dictionary
        run1 = Subjects_RunNumbers[str(subj)]['Run1']
        run2 = Subjects_RunNumbers[str(subj)]['Run2']
        run3 = Subjects_RunNumbers[str(subj)]['Run3']
        run4 = Subjects_RunNumbers[str(subj)]['Run4']
        # build a run list to loop through
        runlist = [run1,run2,run3,run4]
        # process by valid runs
        for runnumber in runlist:
            # set a check so that you're only running ones that need to be run
            regfolder = subjfolder + subj + "_" + runnumber + ".feat/reg/"
            if not os.path.exists(regfolder):
                # if there is not a reg folder in the feat directory, no preprocessing has been done
                # define files for that run
                print anatomical
                funcfile = basesubjDir + "/" + subj + "/func/" + str(runnumber) + ".nii.gz"
                print funcfile
                output=subjfolder + subj + "_" + runnumber + ".feat"
                print output
                print template

                # Copy template and append new data to it
                date = time.strftime("%m%d%Y")
                newTemplateFile= "/Users/Failla/Desktop/PIEC/Templates/1stLevelSubj/Preprocessing/" + subj + "_" + str(runnumber) + "_" + date + ".fsf"

                with open(newTemplateFile, "a") as newTemplate:
                    newTemplate.write(templateContent)
                    newTemplate.write("set feat_files(1) " + '"' + funcfile + '"' + "\n")
                    newTemplate.write("set highres_files(1) " + '"' + anatomical + '"' + "\n")
                    newTemplate.write("set fmri(outputdir) " + '"' + output + '"' + "\n")


                os.system("feat " + newTemplateFile)




