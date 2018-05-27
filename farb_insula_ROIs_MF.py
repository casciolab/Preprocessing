# This script will run files on featquery hopefully skipping through errors
# Jennifer M. Quinde
# 05.21.18

# import what is needed for the operating system
import os

# import csv for reading subject run list
import csv

# we are going to pull in list of files we want to run and create a for loop to run through each file individually
# and skip rather than stop on faulty files

# define subjects and their runs that warrant processing (to exclude certain runs)
# this code creates a dictionary that we can look up what each run number is for each subject

StatsText = " 12   stats/pe1 stats/pe2 stats/pe3 stats/pe4 stats/cope1 stats/cope2 stats/cope3 stats/cope4 stats/zstat1 " \
            "stats/zstat2 stats/zstat3 stats/zstat4 "

Masks = {"Insula_f1": "/Volumes/psr/Cross_Study_Analyses/Insula_Volume/InsulaMNIROIs/MNI_Single_InsulaROIs/colinatlas_2_MNI2mm.nii_shadowreg_f1_thr50.nii.gz",
          "Insula_f2": "/Volumes/psr/Cross_Study_Analyses/Insula_Volume/InsulaMNIROIs/MNI_Single_InsulaROIs/colinatlas_2_MNI2mm.nii_shadowreg_f2_thr50.nii.gz",
          "Insula_f3": "/Volumes/psr/Cross_Study_Analyses/Insula_Volume/InsulaMNIROIs/MNI_Single_InsulaROIs/colinatlas_2_MNI2mm.nii_shadowreg_f3_thr50.nii.gz",
          "Insula_f4": "/Volumes/psr/Cross_Study_Analyses/Insula_Volume/InsulaMNIROIs/MNI_Single_InsulaROIs/colinatlas_2_MNI2mm.nii_shadowreg_f4_thr50.nii.gz",
          "Insula_f5": "/Volumes/psr/Cross_Study_Analyses/Insula_Volume/InsulaMNIROIs/MNI_Single_InsulaROIs/colinatlas_2_MNI2mm.nii_shadowreg_f5_thr50.nii.gz",
          "Insula_f6": "/Volumes/psr/Cross_Study_Analyses/Insula_Volume/InsulaMNIROIs/MNI_Single_InsulaROIs/colinatlas_2_MNI2mm.nii_shadowreg_f6_thr50.nii.gz",
          "Insula_f7": "/Volumes/psr/Cross_Study_Analyses/Insula_Volume/InsulaMNIROIs/MNI_Single_InsulaROIs/colinatlas_2_MNI2mm.nii_shadowreg_f7_thr50.nii.gz",
          "Insula_f8": "/Volumes/psr/Cross_Study_Analyses/Insula_Volume/InsulaMNIROIs/MNI_Single_InsulaROIs/colinatlas_2_MNI2mm.nii_shadowreg_f8_thr50.nii.gz",
          "Insula_l1": "/Volumes/psr/Cross_Study_Analyses/Insula_Volume/InsulaMNIROIs/MNI_Single_InsulaROIs/colinatlas_2_MNI2mm.nii_shadowreg_l1_thr50.nii.gz",
          "Insula_l2": "/Volumes/psr/Cross_Study_Analyses/Insula_Volume/InsulaMNIROIs/MNI_Single_InsulaROIs/colinatlas_2_MNI2mm.nii_shadowreg_l2_thr50.nii.gz",
          "Insula_l3": "/Volumes/psr/Cross_Study_Analyses/Insula_Volume/InsulaMNIROIs/MNI_Single_InsulaROIs/colinatlas_2_MNI2mm.nii_shadowreg_l3_thr50.nii.gz",
          "Insula_l4": "/Volumes/psr/Cross_Study_Analyses/Insula_Volume/InsulaMNIROIs/MNI_Single_InsulaROIs/colinatlas_2_MNI2mm.nii_shadowreg_l4_thr50.nii.gz",
          "Insula_l5": "/Volumes/psr/Cross_Study_Analyses/Insula_Volume/InsulaMNIROIs/MNI_Single_InsulaROIs/colinatlas_2_MNI2mm.nii_shadowreg_l5_thr50.nii.gz",
          "Insula_l6": "/Volumes/psr/Cross_Study_Analyses/Insula_Volume/InsulaMNIROIs/MNI_Single_InsulaROIs/colinatlas_2_MNI2mm.nii_shadowreg_l6_thr50.nii.gz",
          "Insula_l7": "/Volumes/psr/Cross_Study_Analyses/Insula_Volume/InsulaMNIROIs/MNI_Single_InsulaROIs/colinatlas_2_MNI2mm.nii_shadowreg_l7_thr50.nii.gz",
          "Insula_l8": "/Volumes/psr/Cross_Study_Analyses/Insula_Volume/InsulaMNIROIs/MNI_Single_InsulaROIs/colinatlas_2_MNI2mm.nii_shadowreg_l8_thr50.nii.gz"}


with open ('/Users/Failla/Desktop/PIEC/Scripts/first_level_files.csv', 'rU') as filelist:
    allpaths = csv.reader(filelist, delimiter=',')
    for row in allpaths:
        row = "".join(row)
        filepath = row
        print filepath
        for maskname in Masks:
            MaskFile = Masks[maskname]
            trans_matrix = filepath + "/reg/standard2example_func.mat"
            insula_subj = filepath + "/" + maskname + ".nii.gz"
            example_func = filepath + "/reg/example_func.nii.gz"
            print ("flirt -in " + str(MaskFile) + " -applyxfm -init " + str(trans_matrix) +
                " -out " + insula_subj + " -paddingsize 0.0 -interp trilinear -ref " + str(example_func))
            os.system("flirt -in " + str(MaskFile) + " -applyxfm -init " + str(trans_matrix) +
                " -out " + insula_subj + " -paddingsize 0.0 -interp trilinear -ref " + str(example_func))
            maskname_thr = filepath + "/" + maskname + "_thr50.nii.gz"
            print ("fslmaths " + insula_subj + " -thrp 50 " + maskname_thr)
            os.system("fslmaths " + insula_subj + " -thrp 50 " + maskname_thr)
            print ("featquery 1 " + str(filepath) + str(StatsText) + str(maskname) + " " + str(maskname_thr))
            os.system("featquery 1 " + str(filepath) + str(StatsText) + str(maskname) + " " + str(maskname_thr))
print "the end"