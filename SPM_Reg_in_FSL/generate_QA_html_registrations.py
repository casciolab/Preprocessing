import os
import glob

# We will start with the registration png files
out_dir = "/Users/Failla/Desktop/PIEC/300HPF/SPM_Reg/QA"
out_file = out_dir + "/SPM_registration_check.html"
spm_template = "/Users/Failla/Desktop/PIEC/300HPF/SPM_Reg/rspm_template_gray_xnat.nii"

all_feats = sorted(glob.glob('/Users/Failla/Desktop/PIEC/300HPF/Axial/FirstLevel_SPMReg/*.feat/'))

for feat in all_feats:
    # stats file
    stats_file = feat + "stats/logfile"
    # check for stats file, only check reg if stats log exists
    if os.path.exists(stats_file):
        warped_mean_func = feat + "mean_func.nii.gz"
        rendered_file = feat + "mean_func_spm_gray_template.nii.gz"
        png_file = feat + "mean_func_spm_gray_template_image.png"
        os.system("overlay 1 1 " + warped_mean_func + " -a " + spm_template + " 0.16 0.653 " + rendered_file)
        print ("overlay 1 1 " + spm_template + " -a " + warped_mean_func + " " + rendered_file)
        os.system("slices " + rendered_file + " -o " + png_file)
        print ("slices " + rendered_file + " -o " + png_file)

f = open(out_file, "w")
for feat in list(all_feats):
    # stats file
    stats_file = feat + "stats/logfile"
    # check for stats file, only check reg if stats log exists
    if os.path.exists(stats_file):
        f.write("<p>============================================")
        f.write("<p>%s" % (feat))
        f.write("<IMG SRC=\"%s/mean_func_spm_gray_template_image.png\">" % (feat))
f.close()


