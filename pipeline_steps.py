"""All possible steps to be employed for preprocessing and analysis."""
import subprocess


def ct_to_atlas(trans_nl, trans_2, atlas_nii, ct_cut_brain_nii,
                combined_trans, ct_cut_brain_to_atlas_nii):
    """ Register the CT to the template."""
    # Combine transformation
    cmd = ["convertwarp", "--ref={0}".format(atlas_nii),
           "--warp1={0}".format(trans_nl), "--premat={0}".format(trans_2),
           "--out={0}".format(combined_trans)]
    print "Executing: '{0}'.".format(" ".join(cmd))
    subprocess.check_call(cmd)

    # Warp the ct
    cmd = ["applywarp", "-i", ct_cut_brain_nii, "-o",
           ct_cut_brain_to_atlas_nii,
           "-r", atlas_nii, "-w", combined_trans]
    print "Executing: '{0}'.".format(" ".join(cmd))
    subprocess.check_call(cmd)

    return ct_cut_brain_to_atlas_nii, combined_trans


def mri_to_atlas(t1_nii, atlas_nii, register_t1_aff_nii,
                 trans_aff, register_t1_nl_nii, trans_nl):
    """ Register the subject t1 to the template."""
    # Affine registration
    cmd = ["flirt", "-cost", "normmi", "-omat", trans_aff, "-in", t1_nii,
           "-ref", atlas_nii, "-out", register_t1_aff_nii]
    print "Executing: '{0}'.".format(" ".join(cmd))
    subprocess.check_call(cmd)

    # NL registration
    cmd = ["fnirt", "--ref={0}".format(atlas_nii), "--in={0}".format(t1_nii),
           "--iout={0}".format(register_t1_nl_nii),
           "--fout={0}".format(trans_nl), "--aff={0}".format(trans_aff),
           "--config=T1_2_MNI152_2mm.cnf"]
    print "Executing: '{0}'.".format(" ".join(cmd))
    subprocess.check_call(cmd)

    return trans_aff, trans_nl
