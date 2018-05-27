##Loop through fcmri conn data from xnat
# get avaerages
# Michelle Failla
# created 04-30-2018

import pandas as pd
import numpy as np
import fnmatch
import os
import glob
import csv
from scipy.stats import ttest_ind


# set up base directory and base subject directory
bDir = "/Users/Failla/Desktop/PIEC/RestingState/"

# get list of subject files (all files in subject directory)
subject_files = [os.path.basename(x) for x in glob.glob(bDir + "*CONNMAT*")]

KEEPGM_SCRUB_FILES=[]
for filename in fnmatch.filter(subject_files, "*KEEPGM_SCRUB*"):
    KEEPGM_SCRUB_FILES.append(os.path.join(bDir, filename))

Subjects_Dx = {}
with open ('/Users/Failla/Desktop/PIEC/RestingState/scaninfo_5-4-18.csv', 'rU') as subject_dx_file:
    subject_dx_data = csv.reader(subject_dx_file, delimiter=',')
    next(subject_dx_data, None)  # Skip header
    for row in subject_dx_data:
        Subjects_Dx[row[0]] = row[4]

asd_dictionary = {}
td_dictionary = {}
for data_file in KEEPGM_SCRUB_FILES:
    data = pd.read_csv(data_file, sep= ",", header=0)
    data2 = data.drop(["Row"], axis=1)
    file_split = data_file.split("-")
    if Subjects_Dx.get(file_split[2]) == None:
        continue
    else:
        if Subjects_Dx[file_split[2]] == '0':
            td_dictionary[file_split[2]] = data2
        if Subjects_Dx[file_split[2]] == '1':
            asd_dictionary[file_split[2]] = data2


KEEPGM_SCRUB_ASD = pd.Panel(asd_dictionary)
KEEPGM_SCRUB_TD = pd.Panel(td_dictionary)

#KEEPGM_SCRUB_ALL = pd.concat([KEEPGM_SCRUB_ASD, KEEPGM_SCRUB_TD], axis=0)
#KEEPGM_SCRUB_ALL_Z = KEEPGM_SCRUB_ALL.apply(np.arctanh)
KEEPGM_SCRUB_ASD_Z = KEEPGM_SCRUB_ASD.apply(np.arctanh)
KEEPGM_SCRUB_TD_Z = KEEPGM_SCRUB_TD.apply(np.arctanh)

#mean_KEEPGM_NOSCRUB_ASD_Z = KEEPGM_SCRUB_ASD_Z.mean(axis=0)
#mean_KEEPGM_NOSCRUB_TD_Z = KEEPGM_SCRUB_TD_Z.mean(axis=0)
#mean_KEEPGM_NOSCRUB_ALL_Z = KEEPGM_SCRUB_ALL_Z.mean(axis=0)

#KEEPGM_SCRUB_ALL_Z_df = KEEPGM_SCRUB_ALL_Z.to_frame()
KEEPGM_SCRUB_ASD_Z_df = KEEPGM_SCRUB_ASD_Z.to_frame()
KEEPGM_SCRUB_TD_Z_df = KEEPGM_SCRUB_TD_Z.to_frame()


asd = KEEPGM_SCRUB_ASD_Z_df.stack()
asd1 = asd.unstack('minor')
asd2 = asd1.swaplevel(i=-2,j=-1,axis=0)
asd3 = asd2.stack('minor')
asd4 = pd.DataFrame(asd3)
asd5 = asd4.rename(index=str, columns={0:"Z"})

td = KEEPGM_SCRUB_TD_Z_df.stack()
td1 = td.unstack('minor')
td2 = td1.swaplevel(i=-2,j=-1,axis=0)
td3 = td2.stack('minor')
td4 = pd.DataFrame(td3)
td5 = td4.rename(index=str, columns={0:"Z"})

d = {'ASD' : asd5, 'TD' : td5}
all_df_flip = pd.concat(d.values(),axis=0,keys=d.keys())

all_df_flip1 = all_df_flip.swaplevel(i=0, j=2, axis=0)
all_df_flip2 = all_df_flip1.swaplevel(i=1, j=2, axis=0)
all_df = all_df_flip2.swaplevel(i=2, j=3, axis=0)

index = pd.MultiIndex.from_product([set(all_df.index.get_level_values(0)), set(all_df.index.get_level_values(2)), ['t', 'p']])
result = pd.DataFrame(columns=['Z'], index=index)

for roi_num in set(all_df.index.get_level_values(0)):
    for roi_across in set(all_df.index.get_level_values(2)):
        t, p = ttest_ind( all_df.loc[roi_num].loc['ASD'].loc[roi_across] , all_df.loc[roi_num].loc['TD'].loc[roi_across], equal_var=True)
        result.loc[(roi_num, roi_across, 't')] = t
        result.loc[(roi_num, roi_across, 'p')] = p
print result


result.to_csv("/Users/Failla/Desktop/PIEC/RestingState/mean_z_group_diff.csv")


mean_KEEPGM_NOSCRUB_ASD_Z.to_csv("/Users/Failla/Desktop/PIEC/RestingState/mean_asd.csv")
mean_KEEPGM_NOSCRUB_TD_Z.to_csv("/Users/Failla/Desktop/PIEC/RestingState/mean_td.csv")
mean_KEEPGM_NOSCRUB_ALL_Z.to_csv("/Users/Failla/Desktop/PIEC/RestingState/mean_all_z.csv")

test=result.unstack(1)
test2=test.unstack(1)
df = test2.swaplevel(1,2, axis=1).sort_index(axis=1)
df.columns = ['_'.join(col) for col in df.columns]

p_cols = [c for c in df.columns if c.lower()[:4] != 't']

df_p_only=df[t_cols]

p_cols = [c for c in df.columns if c.lower()[:4] != 'p']

df_t_only=df[p_cols]

### for later
### save out and import results, because far too long to compute result dataframe

df_p_only.to_csv("/Users/Failla/Desktop/PIEC/RestingState/r_to_z_group_diff_t.csv")
df_t_only.to_csv("/Users/Failla/Desktop/PIEC/RestingState/r_to_z_group_diff_p.csv")

df_t = pd.DataFrame.from_csv("/Users/Failla/Desktop/PIEC/RestingState/r_to_z_group_diff_t.csv")
df_p = pd.DataFrame.from_csv("/Users/Failla/Desktop/PIEC/RestingState/r_to_z_group_diff_p.csv")


import matplotlib.pyplot as plt

plt.imshow(df_t, cmap='hot', interpolation='nearest')
plt.show()

