function cfunc_file = coreg_func2T1(anat_file,func_file)

clear matlabbatch

matlabbatch{1}.spm.spatial.coreg.estimate.ref = {anat_file};
matlabbatch{1}.spm.spatial.coreg.estimate.source = {func_file};
%matlabbatch{1}.spm.spatial.coreg.estimate.other = {test_list};
matlabbatch{1}.spm.spatial.coreg.estimate.eoptions.cost_fun = 'nmi';
matlabbatch{1}.spm.spatial.coreg.estimate.eoptions.sep = [4 2];
matlabbatch{1}.spm.spatial.coreg.estimate.eoptions.tol = [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001];
matlabbatch{1}.spm.spatial.coreg.estimate.eoptions.fwhm = [7 7];

spm_jobman('run',matlabbatch)

