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
adultrerun = open("/Users/Failla/Desktop/PIEC/Scripts/anatrerunlist_11-14-2016").read()

# process by subject
for subj in subjlist:
    if subj in adultrerun:
        # define folder where the functional images are found, organized by run
        subjfolder = bDir + "/Preprocessing/"
        # generate run list for this subject based on all func images *.nii.gz
        runlist = glob.glob(subjfolder + str(subj) + "*.feat")

        # define if the subject has long or short design based on what their subject number is
        # subj is a string, converting to integer for math statement
        subjnum=int(subj)
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

                # confound files were not properly formatted for fsl to read
                # check if formatted file exists

                # identify the files and a new formatted
                confoundfile = basesubjDir + "/" + subj + "/func/" + str(runnumber) + "/" + "FD_DVARS_MotionOutliers/FD_dvars_common_confound_evs.txt"

                confoundfilenew = basesubjDir + "/" + subj + "/func/" + str(runnumber) + "/" + "FD_DVARS_MotionOutliers/FD_dvars_common_confound_evs_newformat.txt"

                if not os.path.isfile(confoundfilenew):
                    # only use the first 180 or 135 lines depending on runtype of the confoundfile
                    # this is because some of them have been duplicated within the text file (bash error)
                    # so this code makes sure to only use the needed number of lines (number_confound_lines)
                    # read each line of the confound file and write to variable
                    confoundcontent_formatted = ''
                    x = 0
                    with open(confoundfile) as data:
                        for line in data:
                            if x < number_confound_lines:
                                confoundcontent_formatted = confoundcontent_formatted + line
                                x = x + 1
                    # remove tabs
                    confoundcontent_formatted = confoundcontent_formatted.replace('\t', '   ')

                    # write formatted content to new file
                    with open(confoundfilenew, 'w') as newconfound:
                        newconfound.write(confoundcontent_formatted)

                num_lines_confoundfile = sum(1 for line in open(confoundfile))
                num_lines_newconfoundfile = sum(1 for line in open(confoundfilenew))

                print "There are %s lines in the confound file" % num_lines_confoundfile
                print "There are %s lines in the new confound file" % num_lines_newconfoundfile

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


















