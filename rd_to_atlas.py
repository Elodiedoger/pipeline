
# System import
import numpy
import os
import subprocess
import scipy.signal
import glob
import shutil

# Plot import
import matplotlib.pyplot as plt

# IO import
import nibabel

def rd_to_atlas(rd_rescale_file, trans_nl, t1_nii, atlas_nii, ct_brain_init, output_dir) :
    """Register the rd to the atlas"""

    # Output autocompletion
    combined_trans_3 = os.path.join(output_dir, "combined_ct_to_atlas_field_trans_3.nii.gz")
    cut_rd_to_atlas_nii = os.path.join(output_dir, "cut_rd_to_atlas.nii.gz")
    rd_rescale_file_init = os.path.join(output_dir, "cut_rd_to_t1.nii.gz")
    trans_3 = os.path.join(output_dir, "trans_3.txt")
    # Register
    cmd = ["flirt", "-cost", "normmi", "-omat", trans_3, "-in", rd_rescale_file,
           "-ref", t1_nii, "-out",rd_rescale_file_init, "-init", ct_brain_init]
    print "Executing: '{0}'.".format(" ".join(cmd))
    subprocess.check_call(cmd)

    # Combine transformation
    cmd = ["convertwarp", "--ref={0}".format(atlas_nii),
           "--warp1={0}".format(trans_nl),"--premat={0}".format(trans_3) ,
           "--out={0}".format(combined_trans_3)]
    print "Executing: '{0}'.".format(" ".join(cmd))
    subprocess.check_call(cmd)

    # Warp the labels
    cmd = ["applywarp", "-i", rd_rescale_file, "-o", cut_rd_to_atlas_nii,
           "-r", atlas_nii, "-w", combined_trans_3]
    print "Executing: '{0}'.".format(" ".join(cmd))
    subprocess.check_call(cmd)

    return cut_rd_to_atlas_nii

if __name__ == "__main__":

    # Create output directory
    output_dir = "/neurospin/grip/protocols/MRI/dosimetry_elodie_2015/voxel_to_voxel_ana/results/rd_to_atlas/sujet_005"
    if not os.path.exists(output_dir):
	   os.makedirs(output_dir)  
	
	# Global Parameters	
    analysis_path = '/neurospin/grip/protocols/MRI/dosimetry_elodie_2015/voxel_to_voxel_ana'
    data_folder = os.path.join(analysis_path,"dataset")    
    sujet_folder = os.path.join(data_folder,"sujet_005")
    # Specific Parameters
    atlas_nii = "/neurospin/grip/protocols/MRI/dosimetry_elodie_2015/voxel_to_voxel_ana/dataset/atlas/atlas_t1.nii.gz"
    trans_2 = os.path.join(analysis_path, "results","ct_to_mri","sujet_005", "trans_2.txt")
    trans_nl = os.path.join(analysis_path,"results","mri_to_atlas","sujet_005","t1_to_atlas_nl_field.nii.gz")
    rd_rescale_file = os.path.join(,"results","rd_to_ct","sujet_005","rd_rescale.nii.gz")
    t1_nii = t1_nii = os.path.join(sujet_folder,"mri","mri_bravo","nifti_01","sujet_005_nifti_005.nii")
    ct_brain_init = "/neurospin/grip/protocols/MRI/dosimetry_elodie_2015/voxel_to_voxel_ana/results/ct_to_mri/sujet_005/ct_mri_init.txt"
cut_rd_to_atlas_nii = rd_to_atlas(rd_rescale_file, trans_nl, t1_nii, atlas_nii, ct_brain_init, output_dir)
