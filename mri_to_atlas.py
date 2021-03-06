
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


def mri_to_atlas(t1_nii, atlas_nii, output_dir):
   
    """ Register the template to the t1 subject reference.
    """
    # Output autocompletion
    register_t1_aff_nii = os.path.join(output_dir, "t1_to_atlas_aff.nii.gz")
    trans_aff = os.path.join(output_dir, "t1_to_atlas_aff.txt")
    register_t1_nl_nii = os.path.join(output_dir, "t1_to_atlas_nl.nii.gz")
    trans_nl = os.path.join(output_dir, "t1_to_atlas_nl_field.nii.gz")

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

if __name__ == "__main__":
	
 # Create output directory
    output_dir = "/neurospin/grip/protocols/MRI/dosimetry_elodie_2015/voxel_to_voxel_ana/results/mri_to_atlas/sujet_005"
    if not os.path.exists(output_dir):
	   os.makedirs(output_dir)  
	
	# Global Parameters	
    analysis_path = '/neurospin/grip/protocols/MRI/dosimetry_elodie_2015/voxel_to_voxel_ana'
    data_folder = os.path.join(analysis_path,"dataset")    
    sujet_folder = os.path.join(data_folder,"sujet_005")
    # Specific Parameters
    t1_nii = os.path.join(sujet_folder,"mri","mri_bravo","nifti_01","sujet_005_nifti_005.nii")
    atlas_nii = os.path.join(sujet_folder,"atlas","atlas_t1.nii.gz")
    
trans_aff, trans_nl = mri_to_atlas(t1_nii, atlas_nii, output_dir)
