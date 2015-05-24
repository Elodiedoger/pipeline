"""hola."""
# System import
import os
import subprocess


def ct_to_atlas(trans_nl, trans_2, atlas_nii, ct_cut_brain_nii,
                output_dir):
    """ Register the CT to the template."""
    # Output autocompletion
    combined_trans = os.path.join(output_dir,
                                  "combined_ct_to_atlas_field.nii.gz")
    ct_cut_brain_to_atlas_nii = os.path.join(output_dir,
                                             "cut_ct_to_atlas.nii.gz")

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

if __name__ == "__main__":
    # Create output directory
    output_dir = "/neurospin/grip/protocols/MRI/dosimetry_elodie_2015/voxel_to_voxel_ana/results/ct_to_atlas/sujet_005"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Global Parameters
    analysis_path = '/neurospin/grip/protocols/MRI/dosimetry_elodie_2015/voxel_to_voxel_ana'
    data_folder = os.path.join(analysis_path, "dataset")
    sujet_folder = os.path.join(data_folder, "sujet_005")
    # Specific Parameters
    atlas_nii = os.path.join(sujet_folder, "atlas", "atlas_t1.nii.gz")
    ct_cut_brain_nii = os.path.join(analysis_path, "results", "ct_to_mri",
                                    "sujet_005", "ct_cut_brain.nii.gz")
    trans_2 = os.path.join(analysis_path, "results", "ct_to_mri", "sujet_005",
                           "trans_2.txt")
    trans_nl = os.path.join(analysis_path, "mri_to_atlas", "sujet_005",
                            "t1_to_atlas_nl_field.nii.gz")

    ct_cut_brain_to_atlas_nii, combined_trans = ct_to_atlas(trans_nl, trans_2, atlas_nii, ct_cut_brain_nii,
                 output_dir)
