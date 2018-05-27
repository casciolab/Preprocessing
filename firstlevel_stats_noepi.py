# import what is needed for the operating system
import os
# import glob which in this case helps match files in directories
import glob
# import time for date use later
import time
# set up base directory, base subject directory, and base anatomical directory
bDir="/Users/Failla/Desktop/PIEC"
basesubjDir=bDir + "/Subjs"
baseanatDir=bDir + "/Anat_Level"

# get list of subjects to process (all files in subject directory)
subjlist=[os.path.basename(x) for x in glob.glob(basesubjDir + "*/2*")]

# define adults with no epi test subj list
adult = open("/Users/Failla/Desktop/PIEC/Scripts/adults_missing_epitest.txt").read()


# process by subject
for subj in subjlist:
    # check if adult subject
    if subj in adult:

        # define folder where the functional images are found, organized by run
        subjfolder=basesubjDir + "/" + subj + "/func"
        # generate run list for this subject based on all func images *.nii.gz
        runlist=glob.glob(subjfolder + "/*.nii.gz")

        # define if the subject has long or short design based on what their subject number is
        # subj is a string, converting to integer for math statement
        subjnum=int(subj)
        if subjnum < 212000:
            runtype = "Long"
            template = "/Users/Failla/Desktop/PIEC/Templates/1stLevelTemplate_Stats_180vols.fsf"

        else:
            runtype = "Short"
            template = "/Users/Failla/Desktop/PIEC/Templates/1stLevelTemplate_Stats_135vols.fsf"

        templateContent = open(template).read()

        # define anatomical directory for the subject, fsl will import proper anatomical image
        anatomical = baseanatDir + "/" + subj +".anat/T1_biascorr_brain"

        # process all runs for this subject, will need confound file and timing file
        # taking the path list and just getting run numbers, sorting them in numerical order
        runfilelist = [os.path.basename(x) for x in glob.glob(subjfolder + "/*.nii.gz")]
        runnumberlist = []
        for run in runfilelist:
            runnumberlist.append(run.replace(".nii.gz",""))
        runnumberlist.sort()

        # selecting timing files for each run
        # set the run number list to 1 because we dont need to skip the epi test for these scans
        runnumberlistitemcounter = 1
        for runnumber in runnumberlist:
            if runnumberlistitemcounter > 0:
                heart_timingfile = bDir + "/TimingFiles/" + runtype + "/run" + str(runnumberlistitemcounter) + "heart.txt"
                visual_timingfile = bDir + "/TimingFiles/" + runtype + "/run" + str(runnumberlistitemcounter) + "visual.txt"
                print heart_timingfile
                print visual_timingfile
                print anatomical
                funcfile = bDir + "/Preprocessing/" + subj + "_" + runnumber + ".feat"
                print funcfile

                # confound files were not properly formatted for fsl to read
                # identify the files and a new formatted one
                confoundfile=subjfolder + "/" + runnumber + "/" + "FD_DVARS_MotionOutliers/FD_dvars_common_confound_evs.txt"
                confoundfilenew=subjfolder + "/" + runnumber + "/" + "FD_DVARS_MotionOutliers/FD_dvars_common_confound_evs_formatted.txt"
                # get content of original
                confoundcontent = open(confoundfile).read()
                # format to replace tabs with 3 spaces
                confoundcontent_formatted=confoundcontent.replace('\t', '   ')
                # write formatted content to new file
                with open(confoundfilenew, "a") as newconfound:
                    newconfound.write(confoundcontent_formatted)
                print confoundfilenew

                output=bDir + "/FirstLevel/" + subj + "_" + runnumber + ".feat"
                print output
                print template


                # Copy template and append new data to it
                date = time.strftime("%m%d%Y")
                newTemplateFile = "/Users/Failla/Desktop/PIEC/Templates/1stLevelSubj/" + subj + "_" + str(runnumber) + "_" + date + ".fsf"

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


















