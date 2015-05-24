
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

POSSIBLE_AXES_ORIENTATIONS = [
    "LAI", "LIA", "ALI", "AIL", "ILA", "IAL",
    "LAS", "LSA", "ALS", "ASL", "SLA", "SAL",
    "LPI", "LIP", "PLI", "PIL", "ILP", "IPL",
    "LPS", "LSP", "PLS", "PSL", "SLP", "SPL",
    "RAI", "RIA", "ARI", "AIR", "IRA", "IAR",
    "RAS", "RSA", "ARS", "ASR", "SRA", "SAR",
    "RPI", "RIP", "PRI", "PIR", "IRP", "IPR",
    "RPS", "RSP", "PRS", "PSR", "SRP", "SPR"]

CORRECTION_MATRIX_COLUMNS = {
    "R": (1, 0, 0),
    "L": (-1, 0, 0),
    "A": (0, 1, 0),
    "P": (0, -1, 0),
    "S": (0, 0, 1),
    "I": (0, 0, -1)
}

def swap_affine(axes):
    """ Build a correction matrix, from the given orientation
    of axes to RAS.
    """
    rotation = numpy.eye(4)
    rotation[:3, 0] = CORRECTION_MATRIX_COLUMNS[axes[0]]
    rotation[:3, 1] = CORRECTION_MATRIX_COLUMNS[axes[1]]
    rotation[:3, 2] = CORRECTION_MATRIX_COLUMNS[axes[2]]
    return rotation


def reorient_image(input_axes, output_dir):
    """ Rectify the orientation of an image.
    """
    # get the transformation to the RAS space
    rotation = swap_affine(input_axes)
    det = numpy.linalg.det(rotation)
    if det != 1:
        raise Exception("Determinant must be equal to "
                        "one got: {0}.".format(det))


    # save result
    reoriented_file = os.path.join(output_dir, "ct_mri_init.txt")
    numpy.savetxt(reoriented_file, rotation)

    return reoriented_file

def ct_to_mri(t1_nii, ct_nii, min_thr, output_dir, verbose=0):
    """ Register the ct to the mri t1 of the patient.
    """
    # Output autocompletion
    ct_cut_brain_to_t1_nii = os.path.join(output_dir, "ct_cut_brain_to_t1.nii.gz")
    trans_2 = os.path.join(output_dir, "trans_2.txt")
    ct_cut_brain_nii = os.path.join(output_dir, "ct_cut_brain.nii.gz")
    ct_modify_nii = os.path.join(output_dir, "ct_modify.nii.gz")
    print "ok"
    
    # Load ct and modify the data for brain extraction
    ct_im = nibabel.load(ct_nii)
    ct_data = ct_im.get_data()
    ct_shape = ct_data.shape
    ct_data[numpy.where(ct_data < 0)] = 0
    nibabel.save(ct_im, ct_modify_nii)
    
   

    # Detect the neck
    ct_im = nibabel.load(ct_modify_nii)
    ct_data = ct_im.get_data()
    power = numpy.sum(numpy.sum(ct_data, axis=0), axis=0)
    powerfilter = scipy.signal.savgol_filter(power, window_length=11, polyorder=1)
    mins = (numpy.diff(numpy.sign(numpy.diff(powerfilter))) > 0).nonzero()[0] + 1
    global_min = numpy.inf
    cut_brain_index = -1
    for index in mins:
        if powerfilter[index] > min_thr and global_min > powerfilter[index]:
            global_min = powerfilter[index]
            cut_brain_index = index
    cut_brain_index = os.path.join(output_dir, "ct_cut_brain_index.txt")
    # Diplay if verbose mode
    if verbose == 1:
        x = range(power.shape[0])
        plt.plot(x, power, '.', linewidth=1)
        plt.plot(x, powerfilter, '--', linewidth=1)    
        plt.plot(x[cut_brain_index], powerfilter[cut_brain_index], "o")       
        plt.show()

    # Cut the image
    ct_cut_data = ct_data[:, :, range(cut_brain_index, ct_data.shape[2])]
    brain_im = nibabel.Nifti1Image(ct_cut_data, ct_im.get_affine())
    nibabel.save(brain_im, ct_cut_brain_nii)
    

    
    # Reorient ct brain image
    ct_brain_init = reorient_image("LPS", output_dir)

    # Register
    cmd = ["flirt", "-cost", "normmi", "-omat", trans_2, "-in", ct_cut_brain_nii,
           "-ref", t1_nii, "-out",ct_cut_brain_to_t1_nii, "-init", ct_brain_init]
    print "Executing: '{0}'.".format(" ".join(cmd))
    subprocess.check_call(cmd)
    
   
    
    return trans_2, ct_cut_brain_nii, cut_brain_index, ct_cut_brain_to_t1_nii


if __name__ == "__main__":
    
    # Create output directory
    output_dir = "/neurospin/grip/protocols/MRI/dosimetry_elodie_2015/voxel_to_voxel_ana/results/ct_to_mri/sujet_005"
    if not os.path.exists(output_dir):
	   os.makedirs(output_dir)  
	
	# Global Parameters	
    analysis_path = '/neurospin/grip/protocols/MRI/dosimetry_elodie_2015/voxel_to_voxel_ana'
    data_folder = os.path.join(analysis_path,"dataset")    
    sujet_folder = os.path.join(data_folder,"sujet_005")
    # Specific Parameters
    t1_nii = os.path.join(sujet_folder,"mri","mri_bravo","nifti_01","sujet_005_nifti_005.nii")
    ct_nii = os.path.join(sujet_folder,"ct","dicom_01","sujet_005_20121001_095610RTMEDULLO1SPIRALEs006a005.nii.gz")
    
    trans_2, ct_cut_brain_nii, cut_brain_index, ct_cut_brain_to_t1_nii = ct_to_mri(
                    t1_nii, ct_nii, 50000, output_dir, verbose=0)

