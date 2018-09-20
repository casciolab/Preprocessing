
function SPM_xnat_registration_normalization(real_dir)

cd(real_dir)

f = spm_select('FPlist', pwd, '^func.*\.nii$');
g = cellstr(f);

for i=1:length(g)
    moving_file = g{i};
    coreg_func2T1('T1_axial.nii', moving_file)
    out_dir = pwd;
    apply_coreg_transform('initial_coreg_mat.txt',moving_file,out_dir)
end

m = spm_select('FPlist', pwd, '^cfunc.*\.nii$');
n = cellstr(m);

for i=1:length(n)
    moving_file = n{i};
    apply_warp('y_csrc_sn.nii',moving_file,4)
end

