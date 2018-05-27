### This script takes output from MatLAB scripts and organizes for accuracy comparison with participants counts
### Then these data will be compared in R
# Michelle Failla
# Created 4-20-18

# import csv for reading csv
import csv
# import numpy for data calc
import numpy as np
# for dataframe and export
import pandas as pd


# two different physio file type 1 (old) or 2 (recovered)
# runs linked with subject, file type (folder), and run type (type)
run_dictionary = {}
with open('/Volumes/psr/PIEC/Interoception fMRI/scan_list_run.csv', 'rU') as subject_run_file:
    subject_run_data = csv.reader(subject_run_file, delimiter=',')
    next(subject_run_data, None)  # Skip header
    for row in subject_run_data:
        run_dictionary[row[0]] = {}
        run_dictionary[row[0]]['study_id'] = row[1]
        run_dictionary[row[0]]['r1'] = row[2]
        run_dictionary[row[0]]['r2'] = row[3]
        run_dictionary[row[0]]['r3'] = row[4]
        run_dictionary[row[0]]['r4'] = row[5]
        run_dictionary[row[0]]['File_Type'] = row[6]
        run_dictionary[row[0]]['Run_Type'] = row[7]

# pull in data from MatLAB physio script
matlab_dictionary = {}
with open('/Users/Failla/Desktop/MatLab/SCANPHYSLOG_Tools-master/data_output/SCANPHYSLOG.csv', 'rU') as scanfile:
    matlab_data = csv.reader(scanfile, delimiter=',')
    next(matlab_data, None)  # Skip header
    for row in matlab_data:
        print row
        heartbeat_data = row[5:][::-1]
        print heartbeat_data[0]
        if row[3].find("Cascio") == 13:  # check if "Cascio" is at position 13, if so, it's a type 1 physio file
            scanfile = row[3].split("_")
            id = scanfile[2]
            run = "_".join(scanfile[3:5])
            run_number = next(key for key, value in run_dictionary[id].items() if value == run)
            run_id = (id,run_number)
        else:
            scanfile = row[3].split("_")
            id = scanfile[2]
            run = scanfile[4].split(".")
            run_number = "r" + run[0]
            run_id = (id, run_number)
        matlab_dictionary[run_id] = {}
        matlab_dictionary[run_id]['date'] = row[1]
        matlab_dictionary[run_id]['time'] = row[2]
        matlab_dictionary[run_id]['file'] = row[3]
        # extract heart beats per epoch and then reverse it
        # matlab can only really work backwards from the stop signal in the scanner
        # so we know the timing of the epochs by working backwards from the last epoch

        #if heartbeat_data[0] == "":
        #    heartbeat_data.pop(0)
        if run_dictionary[id]['Run_Type'] == '1':
            matlab_dictionary[run_id]['count8'] = sum(np.float32(heartbeat_data[0:2]))
            matlab_dictionary[run_id]['count7'] = sum(np.float32(heartbeat_data[3:5]))
            matlab_dictionary[run_id]['count6'] = sum(np.float32(heartbeat_data[6:8]))
            matlab_dictionary[run_id]['count5'] = sum(np.float32(heartbeat_data[9:11]))
            matlab_dictionary[run_id]['count4'] = sum(np.float32(heartbeat_data[12:14]))
            matlab_dictionary[run_id]['count3'] = sum(np.float32(heartbeat_data[15:17]))
            matlab_dictionary[run_id]['count2'] = sum(np.float32(heartbeat_data[18:20]))
            matlab_dictionary[run_id]['count1'] = sum(np.float32(heartbeat_data[21:23]))
        else:
            matlab_dictionary[run_id]['count6'] = sum(np.float32(heartbeat_data[0:2]))
            matlab_dictionary[run_id]['count5'] = sum(np.float32(heartbeat_data[3:5]))
            matlab_dictionary[run_id]['count4'] = sum(np.float32(heartbeat_data[6:8]))
            matlab_dictionary[run_id]['count3'] = sum(np.float32(heartbeat_data[9:11]))
            matlab_dictionary[run_id]['count2'] = sum(np.float32(heartbeat_data[12:14]))
            matlab_dictionary[run_id]['count1'] = sum(np.float32(heartbeat_data[15:17]))

df = pd.DataFrame.from_dict(matlab_dictionary, orient="index")
df.to_csv("/Volumes/psr/PIEC/Interoception fMRI/scanner_heartbeats.csv")

### visual data! eprime crap.
eprime2 = pd.read_csv('/Volumes/psr/PIEC/PulseOx_Physlog_Data/Eprime_merges/merge2.csv')
eprime2_counts = eprime2.groupby(['Subject','Block','Procedure[Block]','Running[Block]'])['Subject'].count()
eprime2_counts.to_csv('/Volumes/psr/PIEC/PulseOx_Physlog_Data/Eprime_merges/counts_merge2.csv')

eprime3 = pd.read_csv('/Volumes/psr/PIEC/PulseOx_Physlog_Data/Eprime_merges/merge3.csv')
eprime3_counts = eprime3.groupby(['Subject','Block','Procedure[Block]','Running[Block]'])['Subject'].count()
eprime3_counts.to_csv('/Volumes/psr/PIEC/PulseOx_Physlog_Data/Eprime_merges/counts_merge3.csv')

eprime4 = pd.read_csv('/Volumes/psr/PIEC/PulseOx_Physlog_Data/Eprime_merges/merge4.csv')
eprime4_counts = eprime4.groupby(['Subject','Block','Procedure[Block]','Running[Block]'])['Subject'].count()
eprime4_counts.to_csv('/Volumes/psr/PIEC/PulseOx_Physlog_Data/Eprime_merges/counts_merge4.csv')

