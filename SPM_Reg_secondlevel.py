### This script runs second level analysis on all valid runs for each subject
### It will loop through all subjects and runs and combine into a second level model
### for each individual subject
### Michelle Failla
### Created 06-15-17

# import what is needed for the operating system
import os
# import time for adding to rerun templates
import time
# import csv for reading subject run list
import csv
# for finding files in directories
import glob2
# for copying files
import shutil


# set up base directory and base subject directory
bDir = "/Users/Failla/Desktop/PIEC/300HPF/Axial"
# where your first levels are
subjfolder = bDir + "/FirstLevel_SPMReg/"

# Define identity matrix  - will be used to make sure data wont be moved at all
ident_mat = "/Users/Failla/fsl/etc/flirtsch/ident.mat"

# get list of subject files (all files in subject directory)
spm_first_dirs = glob2.glob(subjfolder + '/*.feat')
# get list to compare to - only subjects that have valid runs (to exclude certain subjects)
# this can also be used to run only new subjects, just change this list otherwise you'll run ALL your old subjects
subjects_to_process = [line.rstrip('\r\n') for line in open('/Volumes/psr/Failla/PIEC/DesktopBackup/Scripts/spm_rerun_9-18-2018')]

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

# define output directory for 2nd level
second_level = "/Users/Failla/Desktop/PIEC/300HPF/SPM_Reg/SecondLevel/"

# prep first levels for second level
for path in spm_first_dirs:
    stats = path + "/stats/logfile"
    if os.path.exists(stats):
        # get subject number from path
        subj_run = path.split("/")[8]
        subj = subj_run.split("_")[0]
        run = subj_run.split("_")[1].split(".")[0]

        # delete all matrix files from reg subfolder in each first level feat
        # this will make sure only the identity matrix will be used for our "fake" registration
        mat_files_to_delete = glob2.glob((path + "/reg/*.mat"))
        for mat_file in mat_files_to_delete:
            os.remove(mat_file)
            print mat_file
            print "Deleted"

        # copy identity matrix into first level for "registration"
        example_func2standard = path + "/reg/example_func2standard.mat"
        example_func2highres = path + "/reg/example_func2highres.mat"
        shutil.copy(ident_mat,example_func2standard)
        shutil.copy(ident_mat,example_func2highres)
        mean_func = path + "/mean_func.nii.gz"
        standard = path +"/reg/standard.nii.gz"
        shutil.copy(mean_func,standard)

# run second levels
for subj in subjects_to_process:
    print subj
    # date to add to template file later
    date = time.strftime("%m%d%Y")
    # name output for subject's second level directory
    output = second_level + subj + ".feat"

    if not os.path.exists(output):
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
            template = "/Users/Failla/Desktop/PIEC/300HPF/Cue/Templates/2ndLevelTemplate_1run.fsf"
            templateContent = open(template).read()
            funcfile1 = subjfolder + subj + "_" + runlist[0] + ".feat"
            # Copy template and append new data to it
            newTemplateFile = "/Users/Failla/Desktop/PIEC/300HPF/Axial/Templates/2ndLevel/" + subj + "_" + date + ".fsf"
            with open(newTemplateFile, "a") as newTemplate:
                newTemplate.write(templateContent)
                newTemplate.write("set fmri(outputdir) " + '"' + output + '"' + "\n")
                newTemplate.write("set feat_files(1) " + '"' + funcfile1 + '"' + "\n")
                newTemplate.write("set feat_files(2) " + '"' + funcfile1 + '"' + "\n")

            os.system("feat " + newTemplateFile)

        if runlistlength == 2 :
            template = "/Users/Failla/Desktop/PIEC/300HPF/Cue/Templates/2ndLevelTemplate_2runs.fsf"
            templateContent = open(template).read()
            funcfile1 = subjfolder + subj + "_" + runlist[0] + ".feat"
            funcfile2 = subjfolder + subj + "_" + runlist[1] + ".feat"


            # Copy template and append new data to it
            newTemplateFile = "/Users/Failla/Desktop/PIEC/300HPF/Axial/Templates/2ndLevel/" + subj + "_" + date + ".fsf"
            with open(newTemplateFile, "a") as newTemplate:
                newTemplate.write(templateContent)
                newTemplate.write("set fmri(outputdir) " + '"' + output + '"' + "\n")
                newTemplate.write("set feat_files(1) " + '"' + funcfile1 + '"' + "\n")
                newTemplate.write("set feat_files(2) " + '"' + funcfile2 + '"' + "\n")

            os.system("feat " + newTemplateFile)

        if runlistlength == 3 :
            template = "/Users/Failla/Desktop/PIEC/300HPF/Cue/Templates/2ndLevelTemplate_3runs.fsf"
            templateContent = open(template).read()
            funcfile1 = subjfolder + subj + "_" + runlist[0] + ".feat"
            funcfile2 = subjfolder + subj + "_" + runlist[1] + ".feat"
            funcfile3 = subjfolder + subj + "_" + runlist[2] + ".feat"

            # Copy template and append new data to it
            newTemplateFile = "/Users/Failla/Desktop/PIEC/300HPF/Axial/Templates/2ndLevel/" + subj + "_" + date + ".fsf"
            with open(newTemplateFile, "a") as newTemplate:
                newTemplate.write(templateContent)
                newTemplate.write("set fmri(outputdir) " + '"' + output + '"' + "\n")
                newTemplate.write("set feat_files(1) " + '"' + funcfile1 + '"' + "\n")
                newTemplate.write("set feat_files(2) " + '"' + funcfile2 + '"' + "\n")
                newTemplate.write("set feat_files(3) " + '"' + funcfile3 + '"' + "\n")

            os.system("feat " + newTemplateFile)

        if runlistlength == 4 :
            template = "/Users/Failla/Desktop/PIEC/300HPF/Cue/Templates/2ndLevelTemplate_4runs.fsf"
            templateContent = open(template).read()
            funcfile1 = subjfolder + subj + "_" + runlist[0] + ".feat"
            funcfile2 = subjfolder + subj + "_" + runlist[1] + ".feat"
            funcfile3 = subjfolder + subj + "_" + runlist[2] + ".feat"
            funcfile4 = subjfolder + subj + "_" + runlist[3] + ".feat"

            # Copy template and append new data to it
            newTemplateFile = "/Users/Failla/Desktop/PIEC/300HPF/Axial/Templates/2ndLevel/" + subj + "_" + date + ".fsf"
            with open(newTemplateFile, "a") as newTemplate:
                newTemplate.write(templateContent)
                newTemplate.write("set fmri(outputdir) " + '"' + output + '"' + "\n")
                newTemplate.write("set feat_files(1) " + '"' + funcfile1 + '"' + "\n")
                newTemplate.write("set feat_files(2) " + '"' + funcfile2 + '"' + "\n")
                newTemplate.write("set feat_files(3) " + '"' + funcfile3 + '"' + "\n")
                newTemplate.write("set feat_files(4) " + '"' + funcfile4 + '"' + "\n")

            os.system("feat " + newTemplateFile)
        else:
            print "Subject %s" %subj + " may not have all valid runs. Not processed."

    else:
        print "Subject %s" %subj + " already has second level. Not processed."



