### This script creates takes the created confound files (FD and DVARS)
### and matches the spikes that are found in both files
### It will loop through all subjects and runs that are valid
### Michelle Failla
### Last Updated 06-16-17

# import what is needed for the operating system
import os
# import glob which in this case helps match files in directories
import glob
#import csv for reading subject run list
import csv


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
            fd = confound_dir + "fd_confoundEV.txt"
            dvars = confound_dir + "dvars_confoundEV.txt"
            outputfilename = confound_dir + "FD_DVARS_common_outliers.txt"

            if not os.path.isfile(outputfilename):
                # need to check if fd_spikes and dvars_spikes exist and overwrite them if they do
                if os.path.isfile(fd) and os.path.isfile(dvars):
                    print "Compare FD and DVARS for %s" %subj + " : %r" %runnumber

                    # Create a list of fd row numbers with a 1 (and count total rows)
                    fdSpikes = []
                    fdContentsRowCounter = 1
                    with open(fd) as fdContents:
                        for line in fdContents:
                            if '1' in line:
                                fdSpikes.append(int(fdContentsRowCounter))
                            fdContentsRowCounter += 1

                    # Because we process last row and then increase the counter,
                    # need to subtract 1 from the total row count to get real row count
                    totalRowCount = fdContentsRowCounter - 1

                    # Create a list of dvars row numbers with a 1
                    dvarsSpikes = []
                    dvarsContentsRowCounter = 1
                    with open(dvars) as dvarsContents:
                        for line in dvarsContents:
                            if '1' in line:
                                dvarsSpikes.append(int(dvarsContentsRowCounter))
                            dvarsContentsRowCounter += 1

                    # Create an empty list of common values,
                    # set a variable to count the total number of list items to get masterColumnCount
                    # Loop through list 1, check if each variable is in list 2,
                    # if it is, then add that line number to common values
                    commonSpikes = []
                    for lineNumber in fdSpikes:
                        if lineNumber in dvarsSpikes:
                            commonSpikes.append(int(lineNumber))

                    totalColumnCount = len(commonSpikes)

                     # Create a for loop that generates lists of zeros,
                    # ending when you reach the total rows that we determined above
                    outputfilename = confound_dir + "FD_DVARS_common_outliers.txt"
                    outputFile = open(outputfilename, 'w')
                    # Create a counter that tracks which row you are on
                    outputRowCounter = 1
                    # Create a counter that tracks the last column to have a 1 written to it (start it at column 1)
                    outputColumnCounter = 1
                    # Write the file
                    while (outputRowCounter <= totalRowCount):
                        linedata = ''
                        currentColumnPosition = 1

                        # Check if row is a spike row
                        spikeRow = False
                        if outputRowCounter in commonSpikes:
                            spikeRow = True

                         # Build the line of 1s and 0s
                        # Current column position is increased until it reaches the number of total columns needed to build each line
                        while (currentColumnPosition <= totalColumnCount):
                            if (currentColumnPosition == outputColumnCounter and spikeRow == True):
                                linedata += '1   '
                                outputColumnCounter += 1
                                # Set the spike row as false to avoid another 1 on the same line
                                spikeRow = False
                            else:
                                linedata += '0   '
                            currentColumnPosition += 1

                        # Trim the extra spaces at the end of the linedata
                        linedata = linedata.rstrip()

                        # Write the line to the output file
                        outputFile.write(linedata + "\n")
                        outputRowCounter += 1

                else:
                    print "Missing either FD or DVARS (no confounds found). Making empty file for %s" % subj + " : %r" % runnumber
                    outputfilename = confound_dir + "FD_DVARS_common_outliers.txt"
                    outputFile = open(outputfilename, 'w')
            else:
                print subj
                print runnumber