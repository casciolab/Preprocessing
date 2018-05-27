### This script organizes physio files in batches for analysis in MatLab
### These files are located in two places and have two different run numbering systems
### They all need to be in one input file for MatLab to process them for HR
# Michelle Failla
# Last Updated 4-13-18

# import what is needed for the operating system
import os
# import glob which in this case helps match files in directories
import glob
# import fnmatch for filename matching
import shutil
# import csv for reading csv
import csv
# import zipfile to unzip all the old physlogs from directory 1
import zipfile

# label each possible directory
directory1 = "/Volumes/psr/PIEC/Interoception fMRI/"
directory2 = "/Volumes/psr/PIEC/PulseOx_Physlog_Data/"
out_directory = "/Users/Failla/Desktop/MatLab/SCANPHYSLOG_Tools-master/data_input/"

run_dictionary = {}
with open ('/Volumes/psr/PIEC/Interoception fMRI/scan_list_run.csv', 'rU') as subject_run_file:
    subject_run_data = csv.reader(subject_run_file, delimiter=',')
    next(subject_run_data, None)  # Skip header
    for row in subject_run_data:
        run_dictionary[row[0]] = {}
        run_dictionary[row[0]]['study_id'] = row[1]
        run_dictionary[row[0]]['r1'] = row[2]
        run_dictionary[row[0]]['r2'] = row[3]
        run_dictionary[row[0]]['r3'] = row[4]
        run_dictionary[row[0]]['r4'] = row[5]
        run_dictionary[row[0]]['Folder'] = row[6]
        run_dictionary[row[0]]['Type'] = row[7]


# this is the phys log data files linked to their runs for directory 2
recovered_dictionary = {}
with open ('/Volumes/psr/PIEC/PulseOx_Physlog_Data/PIEC_Physlog_Recovery_Dictionary.csv', 'rU') as recover_file:
    recover_data = csv.reader(recover_file, delimiter=',')
    next(recover_data, None)  # Skip header
    for row in recover_data:
        recovered_dictionary[row[0]] = {}
        recovered_dictionary[row[0]]['study_id'] = row[1]
        recovered_dictionary[row[0]]['r1'] = row[4]
        recovered_dictionary[row[0]]['r2'] = row[5]
        recovered_dictionary[row[0]]['r3'] = row[6]
        recovered_dictionary[row[0]]['r4'] = row[7]

# Find files
for scan in run_dictionary:
    if run_dictionary[scan]['Folder']=='1':
        id = run_dictionary[scan]['study_id']
        find_runs = directory1 + id + "/Behavioral/Heartbeat/"
        # call run number definitions from the dictionary
        r1 = run_dictionary[scan]['r1']
        r2 = run_dictionary[scan]['r2']
        r3 = run_dictionary[scan]['r3']
        r4 = run_dictionary[scan]['r4']
        # build run list to loop through
        runlist = [r1, r2, r3, r4]
        for run in runlist:
            # unzip file and extract the physlog file and save in input for processing
            run_zip_file = [os.path.basename(x) for x in glob.glob(find_runs + "*" + run + "*" + ".ZIP")]
            if len(run_zip_file) == 0:
                print "No physlogs found for %r" % id + " run %r" % run
                continue
            run_find = run_zip_file[0].split('Z')
            run_log = run_find[0] + "SCANPHYSLOG.LOG"
            run_zip_file_find = find_runs + run_zip_file[0]
            if os.path.isfile(run_zip_file_find):
                run_zip = zipfile.ZipFile(run_zip_file_find)
                run_zip.extract(run_log, out_directory)
                run_zip.close()

    if run_dictionary[scan]['Folder']=='2':
        if scan in recovered_dictionary:
            subj_dir = directory2 + scan + "/"
            # call run number definitions from the dictionary
            run1_file = recovered_dictionary[scan]['r1']
            run2_file = recovered_dictionary[scan]['r2']
            run3_file = recovered_dictionary[scan]['r3']
            run4_file = recovered_dictionary[scan]['r4']
            # build a run list to loop through
            runlist = [run1_file,run2_file,run3_file,run4_file]
            # process by valid runs
            for runnumber in runlist:
                # copy and move file for MatLab processing
                run = subj_dir + runnumber + ".log"
                run_num = runlist.index(runnumber) + 1
                run_move = out_directory + scan + "_run_" + str(run_num) + ".log"
                if os.path.isfile(run):
                    print "Copying %s" % scan + " run %r" % run_num + "as %r" % runnumber + " to %r" % run_move
                    shutil.copy(run, run_move)
                else:
                    print "%s" % scan + " run  %r does not exist?" % run_num

# renaming files from directory2 - need them all to have the word "SCANPHYSLOG" for MatLab processing
for filename in os.listdir("/Users/Failla/Desktop/MatLab/SCANPHYSLOG_Tools-master/data_input/"):
    print filename
    old = out_directory + filename
    new = out_directory + "SCANPHYSLOG_" + filename
    print new
    os.rename(old, new)



