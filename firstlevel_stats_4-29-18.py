# import what is needed for the operating system
import os
# import glob which in this case helps match files in directories
import glob
# import time for adding to rerun templates
import time
#import csv for reading subject run list
import csv

# set up base directory, base subject directory, and base anatomical directory
bDir = "/Users/Failla/Desktop/PIEC"
basesubjDir = bDir + "/Subjs"
baseanatDir = bDir + "/AnatLevel"

# get list of subjects to process (all files in subject directory)
subjlist = [os.path.basename(x) for x in glob.glob(basesubjDir + "*/*")]

# define subjects to rerun list
hpfrerun = open("/Users/Failla/Desktop/PIEC/Scripts/300hpf_rerun_stats_5-9-18.txt").read()


# define subjects and their runs that warrant processing (to exclude certain runs)
# this code creates a dictionary that we can look up what each run number is for each subject
Subjects_RunNumbers = {}
with open ('/Volumes/psr-1/Failla/PIEC/subjects_runs_redostats_5-9-18.csv', 'rU') as subject_run_file:
    subject_run_data = csv.reader(subject_run_file, delimiter=',')
    next(subject_run_data, None)  # Skip header
    for row in subject_run_data:
        Subjects_RunNumbers[row[0]] = {}
        Subjects_RunNumbers[row[0]]['Run1'] = row[1]
        Subjects_RunNumbers[row[0]]['Run2'] = row[2]
        Subjects_RunNumbers[row[0]]['Run3'] = row[3]
        Subjects_RunNumbers[row[0]]['Run4'] = row[4]

# process by subject
for subj in subjlist:
    if subj in hpfrerun:
        # define folder where the functional images are found, organized by run
        subjfolder = bDir + "/300HPF/FirstLevel/"
        # generate run list for this subject based on all func images *.nii.gz
        runlist = glob.glob(subjfolder + str(subj) + "*.feat")

        # define if the subject has long or short design based on what their subject number is
        # subj is a string, converting to integer for math statement
        subjnum=int(subj)
        if subjnum < 130269:
            runtype = "Short"
            template = "/Users/Failla/Desktop/PIEC/300HPF/Templates/1stLevelTemplate_Stats_135vols.fsf"
            number_confound_lines = 135
        else:
            if subjnum < 212000:
                runtype = "Long"
                template = "/Users/Failla/Desktop/PIEC/300HPF/Templates/1stLevelTemplate_Stats_180vols.fsf"
                number_confound_lines=180

            else:
                runtype = "Short"
                template = "/Users/Failla/Desktop/PIEC/300HPF/Templates/1stLevelTemplate_Stats_135vols.fsf"
                number_confound_lines = 135

        templateContent = open(template).read()

        # define anatomical directory for the subject, fsl will import proper anatomical image
        anatomical = baseanatDir + "/" + subj +".anat/T1_biascorr_brain"

        # process all runs for this subject, will need confound file and timing file
        # taking the path list and just getting run numbers, sorting them in numerical order
        # call the definitions from the dictionary
        run1 = Subjects_RunNumbers[str(subj)]['Run1']
        run2 = Subjects_RunNumbers[str(subj)]['Run2']
        run3 = Subjects_RunNumbers[str(subj)]['Run3']
        run4 = Subjects_RunNumbers[str(subj)]['Run4']
        # build a run list to loop through
        runlist = [run1,run2,run3,run4]
        # process by valid runs
        for runcall in Subjects_RunNumbers[str(subj)]:
            runnumber = Subjects_RunNumbers[str(subj)][runcall]
            run_order_num = runcall.split('Run')
            heart_timingfile = bDir + "/TimingFiles/" + runtype + "/run" + run_order_num[1] + "heart.txt"
            visual_timingfile = bDir + "/TimingFiles/" + runtype + "/run" + run_order_num[1] + "visual.txt"
            print heart_timingfile
            print visual_timingfile
            print anatomical
            funcfile = bDir + "/300HPF/FirstLevel/" + subj + "_" + str(runnumber) + ".feat"
            print funcfile

            confoundfilenew = basesubjDir + "/" + subj + "/func/" + str(runnumber) + "/" + "FD_DVARS_MotionOutliers/FD_DVARS_common_outliers.txt"

            if not os.path.isfile(confoundfilenew):
                confoundfilenew = ""
            output=bDir + "/300HPF/FirstLevel/" + subj + "_" + str(runnumber) + ".feat"
            print output
            print template

            # Copy template and append new data to it
            date = time.strftime("%m%d%Y")
            newTemplateFile= "/Users/Failla/Desktop/PIEC/300HPF/Templates/1stLevelSubj/Stats/" + subj + "_" + str(runnumber) + "_" + date + ".fsf"

            with open(newTemplateFile, "a") as newTemplate:
                newTemplate.write(templateContent)
                newTemplate.write("set fmri(outputdir) " + '"' + output + '"' + "\n")
                newTemplate.write("set feat_files(1) " + '"' + funcfile + '"' + "\n")
                newTemplate.write("set highres_files(1) " + '"' + anatomical + '"' + "\n")
                newTemplate.write("set confoundev_files(1) " + '"' + confoundfilenew + '"' + "\n")
                newTemplate.write("set fmri(custom1) " + '"' + heart_timingfile + '"' + "\n")
                newTemplate.write("set fmri(custom2) " + '"' + visual_timingfile + '"' + "\n")


            os.system("feat " + newTemplateFile)