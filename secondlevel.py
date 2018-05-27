### This script runs second level analysis on all valid runs for each subject
### It will loop through all subjects and runs and combine into a second level model
### for each individual subject
### Michelle Failla
### Created 06-15-17

# import what is needed for the operating system
import os
# import glob which in this case helps match files in directories
import glob
# import time for adding to rerun templates
import time
#import csv for reading subject run list
import csv

print

# set up base directory and base subject directory
bDir = "/Users/Failla/Desktop/PIEC/300HPF"
basesubjDir = "/Users/Failla/Desktop/PIEC/Subjs"
subjfolder = bDir + "/FirstLevel/"
baseanatDir = "/Users/Failla/Desktop/PIEC/AnatLevel/"

# get list of subject files (all files in subject directory)
subject_files = [os.path.basename(x) for x in glob.glob(basesubjDir + "*/*")]
# get list to compare to - only subjects that have valid runs (to exclude certain subjects)
subjects_to_process = open("/Users/Failla/Desktop/PIEC/Scripts/300hpf_rerun_confound_5-10-18").read()

# define subjects and their runs that warrant processing (to exclude certain runs)
# this code creates a dictionary that we can look up what each run number is for each subject
Subjects_RunNumbers = {}
with open ('/Volumes/psr-1/Failla/PIEC/subjects_runs_2ndlevel_5-8-18.csv', 'rU') as subject_run_file:
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
        # date to add to template file later
        date = time.strftime("%m%d%Y")
        # name output for subject's second level directory
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
        print "Subject %s " %subj + "has %r runs." %runlistlength

        # pick template based on number of valid runs
        if runlistlength == 1 :
            template = "/Users/Failla/Desktop/PIEC/Templates/2ndLevelTemplate_1run.fsf"
            templateContent = open(template).read()
            funcfile1 = subjfolder + subj + "_" + runlist[0] + ".feat"
            # Copy template and append new data to it
            newTemplateFile = "/Users/Failla/Desktop/PIEC/300HPF/Templates/2ndLevel/" + subj + "_" + date + ".fsf"
            with open(newTemplateFile, "a") as newTemplate:
                newTemplate.write(templateContent)
                newTemplate.write("set fmri(outputdir) " + '"' + output + '"' + "\n")
                newTemplate.write("set feat_files(1) " + '"' + funcfile1 + '"' + "\n")
                newTemplate.write("set feat_files(2) " + '"' + funcfile1 + '"' + "\n")

            os.system("feat " + newTemplateFile)

        if runlistlength == 2 :
            template = "/Users/Failla/Desktop/PIEC/Templates/2ndLevelTemplate_2runs.fsf"
            templateContent = open(template).read()
            funcfile1 = subjfolder + subj + "_" + runlist[0] + ".feat"
            funcfile2 = subjfolder + subj + "_" + runlist[1] + ".feat"


            # Copy template and append new data to it
            newTemplateFile = "/Users/Failla/Desktop/PIEC/300HPF/Templates/2ndLevel/" + subj + "_" + date + ".fsf"
            with open(newTemplateFile, "a") as newTemplate:
                newTemplate.write(templateContent)
                newTemplate.write("set fmri(outputdir) " + '"' + output + '"' + "\n")
                newTemplate.write("set feat_files(1) " + '"' + funcfile1 + '"' + "\n")
                newTemplate.write("set feat_files(2) " + '"' + funcfile2 + '"' + "\n")

            os.system("feat " + newTemplateFile)

        if runlistlength == 3 :
            template = "/Users/Failla/Desktop/PIEC/Templates/2ndLevelTemplate_3runs.fsf"
            templateContent = open(template).read()
            funcfile1 = subjfolder + subj + "_" + runlist[0] + ".feat"
            funcfile2 = subjfolder + subj + "_" + runlist[1] + ".feat"
            funcfile3 = subjfolder + subj + "_" + runlist[2] + ".feat"

            # Copy template and append new data to it
            newTemplateFile = "/Users/Failla/Desktop/PIEC/300HPF/Templates/2ndLevel/" + subj + "_" + date + ".fsf"
            with open(newTemplateFile, "a") as newTemplate:
                newTemplate.write(templateContent)
                newTemplate.write("set fmri(outputdir) " + '"' + output + '"' + "\n")
                newTemplate.write("set feat_files(1) " + '"' + funcfile1 + '"' + "\n")
                newTemplate.write("set feat_files(2) " + '"' + funcfile2 + '"' + "\n")
                newTemplate.write("set feat_files(3) " + '"' + funcfile3 + '"' + "\n")

            os.system("feat " + newTemplateFile)

        if runlistlength == 4 :
            template = "/Users/Failla/Desktop/PIEC/Templates/2ndLevelTemplate_4runs.fsf"
            templateContent = open(template).read()
            funcfile1 = subjfolder + subj + "_" + runlist[0] + ".feat"
            funcfile2 = subjfolder + subj + "_" + runlist[1] + ".feat"
            funcfile3 = subjfolder + subj + "_" + runlist[2] + ".feat"
            funcfile4 = subjfolder + subj + "_" + runlist[3] + ".feat"

            # Copy template and append new data to it
            newTemplateFile = "/Users/Failla/Desktop/PIEC/300HPF/Templates/2ndLevel/" + subj + "_" + date + ".fsf"
            with open(newTemplateFile, "a") as newTemplate:
                newTemplate.write(templateContent)
                newTemplate.write("set fmri(outputdir) " + '"' + output + '"' + "\n")
                newTemplate.write("set feat_files(1) " + '"' + funcfile1 + '"' + "\n")
                newTemplate.write("set feat_files(2) " + '"' + funcfile2 + '"' + "\n")
                newTemplate.write("set feat_files(3) " + '"' + funcfile3 + '"' + "\n")
                newTemplate.write("set feat_files(4) " + '"' + funcfile4 + '"' + "\n")

            os.system("feat " + newTemplateFile)

    else:
        print "Subject %s" %subj + " does not have valid first level. Not processed."

