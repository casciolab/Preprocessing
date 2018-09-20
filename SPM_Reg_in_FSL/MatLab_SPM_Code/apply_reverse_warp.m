function vatlas_file = apply_reverse_warp(invdef_file,native_file,atlas_file,interp)

% We could push the inverse deformation, but that doesn't let us specify
% the interpolation method. So we compute the inverse of the inverse
% deformation and do a pull instead.
clear matlabbatch
matlabbatch{1}.spm.util.defs.comp{1}.inv.comp{1}.def = {invdef_file};
matlabbatch{1}.spm.util.defs.comp{1}.inv.space = {native_file};
matlabbatch{1}.spm.util.defs.out{1}.pull.fnames = {atlas_file};
matlabbatch{1}.spm.util.defs.out{1}.pull.savedir.savesrc = 1;
matlabbatch{1}.spm.util.defs.out{1}.pull.interp = interp;
matlabbatch{1}.spm.util.defs.out{1}.pull.mask = 1;
matlabbatch{1}.spm.util.defs.out{1}.pull.fwhm = [0 0 0];

spm_jobman('run',matlabbatch)

[p,n,e] = fileparts(atlas_file);
vatlas_file = fullfile(p,['w' n e]);
