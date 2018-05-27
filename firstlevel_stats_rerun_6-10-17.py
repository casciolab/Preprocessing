# import what is needed for the operating system
import os
# import glob which in this case helps match files in directories
import glob
# import time for adding to rerun templates
import time

# set up base directory, base subject directory, and base anatomical directory
bDir = "/Users/Failla/Desktop/PIEC"
basesubjDir = bDir + "/Subjs"
baseanatDir = bDir + "/Anat_Level"

# get list of subjects to process (all files in subject directory)
subjlist = [os.path.basename(x) for x in glob.glob(basesubjDir + "*/2*")]

# define subjects to rerun list
hpfrerun = open("/Users/Failla/Desktop/PIEC/Scripts/anatrerunlist_4-27-2018").read()

# process by subject
for subj in subjlist:
    if subj in hpfrerun:
        # define folder where the functional images are found, organized by run
        subjfolder = bDir + "/FirstLevel/"
        # generate run list for this subject based on all func images *.nii.gz
        runlist = glob.glob(subjfolder + str(subj) + "*.feat")

        # define if the subject has long or short design based on what their subject number is
        # subj is a string, converting to integer for math statement
        subjnum=int(subj)
        if subjnum < 130269:
            runtype = "Short"
            template = "/Users/Failla/Desktop/PIEC/Templates/1stLevelTemplate_Stats_135vols.fsf"
            number_confound_lines = 135
        else:
            if subjnum < 212000:
                runtype = "Long"
                template = "/Users/Failla/Desktop/PIEC/Templates/1stLevelTemplate_Stats_180vols.fsf"
                number_confound_lines=180

            else:
                runtype = "Short"
                template = "/Users/Failla/Desktop/PIEC/Templates/1stLevelTemplate_Stats_135vols.fsf"
                number_confound_lines = 135

        templateContent = open(template).read()

        # define anatomical directory for the subject, fsl will import proper anatomical image
        anatomical = baseanatDir + "/" + subj +".anat/T1_biascorr_brain"

        # process all runs for this subject, will need confound file and timing file
        # taking the path list and just getting run numbers, sorting them in numerical order

        sorted_run_number_list = []
        for run in runlist:
            runfile = run.split('_')[1]
            sorted_run_number_list.append(int(runfile.replace(".feat", "")))
        sorted_run_number_list.sort()

        # selecting timing files for each run
        runnumberlistitemcounter = 0
        for runnumber in sorted_run_number_list:
            if runnumberlistitemcounter > 0:
                heart_timingfile = bDir + "/TimingFiles/" + runtype + "/run" + str(runnumberlistitemcounter) + "heart.txt"
                visual_timingfile = bDir + "/TimingFiles/" + runtype + "/run" + str(runnumberlistitemcounter) + "visual.txt"
                print heart_timingfile
                print visual_timingfile
                print anatomical
                funcfile = bDir + "/FirstLevel/" + subj + "_" + str(runnumber) + ".feat"
                print funcfile


                confoundfilenew = basesubjDir + "/" + subj + "/func/" + str(runnumber) + "/" + "FD_DVARS_MotionOutliers/FD_dvars_common_confound_evs_newformat.txt"

                if not os.path.isfile(confoundfilenew):
                    confoundfilenew = ""
                output=bDir + "/FirstLevel/" + subj + "_" + str(runnumber) + ".feat"
                print output
                print template

                # Copy template and append new data to it
                date = time.strftime("%m%d%Y")
                newTemplateFile= "/Users/Failla/Desktop/PIEC/Templates/1stLevelSubj/" + subj + "_" + str(runnumber) + "_" + date + ".fsf"

                with open(newTemplateFile, "a") as newTemplate:
                    newTemplate.write(templateContent)
                    newTemplate.write("set fmri(outputdir) " + '"' + output + '"' + "\n")
                    newTemplate.write("set feat_files(1) " + '"' + funcfile + '"' + "\n")
                    newTemplate.write("set highres_files(1) " + '"' + anatomical + '"' + "\n")
                    newTemplate.write("set confoundev_files(1) " + '"' + confoundfilenew + '"' + "\n")
                    newTemplate.write("set fmri(custom1) " + '"' + heart_timingfile + '"' + "\n")
                    newTemplate.write("set fmri(custom2) " + '"' + visual_timingfile + '"' + "\n")


                os.system("feat " + newTemplateFile)
            runnumberlistitemcounter += 1