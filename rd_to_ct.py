
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

def inverse_affine(affine):
    """ Invert an affine transformation the rd is on the same orientation than the ct.
    """
    invr = numpy.linalg.inv(affine[:3, :3])
    inv_affine = numpy.zeros((4, 4))
    inv_affine[3, 3] = 1
    inv_affine[:3, :3] = invr
    inv_affine[:3, 3] =  - numpy.dot(invr, affine[:3, 3])
    return inv_affine


def threed_dot(matrice, vector):
    """ Dot product between a 3d matrix and an image of 3d vectors.
    """
    res = numpy.zeros(vector.shape)
    for i in range(3):
	    res[..., i] = (matrice[i, 0] * vector[..., 0] + 
                       matrice[i, 1] * vector[..., 1] + 
                       matrice[i, 2] * vector[..., 2] +
                       matrice[i, 3])
    return res


def rd_to_ct(ct_nii, rd_nii, cut_brain_index, output_dir):
    """ Register the rd to the ct space.
    """
    
    # Output autocompletion
    rd_rescale_file = os.path.join(output_dir, "rd_rescale.nii.gz")

    # Load images
    ct_im = nibabel.load(ct_nii)
    ct_data = ct_im.get_data()
    rd_im = nibabel.load(rd_nii)
    rd_data = rd_im.get_data()
    cta = ct_im.get_affine()
    rda = rd_im.get_affine()

    # Correct the rda affine matrix
    rda[2, 2] = 3

    # Inverse affine transformation
    irda = inverse_affine(rda)
    t = numpy.dot(irda, cta)

    # Matricial dot product
    rd_rescale = numpy.zeros(ct_data.shape)
    dot_image = numpy.zeros(ct_data.shape + (3, ))
    x = numpy.linspace(0, ct_data.shape[0] - 1, ct_data.shape[0])
    y = numpy.linspace(0, ct_data.shape[1] - 1, ct_data.shape[1])
    z = numpy.linspace(0, ct_data.shape[2] - 1, ct_data.shape[2])
    xg, yg, zg = numpy.meshgrid(x, y, z)
    dot_image[..., 0] = yg
    dot_image[..., 1] = xg
    dot_image[..., 2] = zg
    dot_image = threed_dot(t, dot_image)

    cnt = 0
    print ct_data.size
    for x in range(ct_data.shape[0]):
        for y in range(ct_data.shape[1]):
            for z in range(cut_brain_index, ct_data.shape[2]):
                if cnt % 100000 == 0:
                    print cnt  
                cnt += 1          
                voxel_rd = dot_image[x, y, z]
                if (voxel_rd > 0).all() and (voxel_rd < (numpy.asarray(rd_data.shape) - 1)).all():
                    rd_voxel = numpy.round(voxel_rd)
                    rd_rescale[x, y, z] = rd_data[rd_voxel[0], rd_voxel[1], rd_voxel[2]]

    rd_rescale_im = nibabel.Nifti1Image(rd_rescale, cta)
    nibabel.save(rd_rescale_im, rd_rescale_file)

    return rd_rescale_file
    
if __name__ == "__main__":
  
    # Create output directory
    output_dir = "/neurospin/grip/protocols/MRI/dosimetry_elodie_2015/voxel_to_voxel_ana/results/rd_to_ct/sujet_005"
    if not os.path.exists(output_dir):
	   os.makedirs(output_dir)  
	
	# Global Parameters	
    analysis_path = '/neurospin/grip/protocols/MRI/dosimetry_elodie_2015/voxel_to_voxel_ana'
    data_folder = os.path.join(analysis_path,"dataset")    
    sujet_folder = os.path.join(data_folder,"sujet_005")
    # Specific Parameters
    rd_nii = os.path.join(sujet_folder,"rd","dicom_01","sujet_005_20121001_101257VOLENTIER300H20ss006a000.nii.gz")
    ct_nii = os.path.join(sujet_folder,"ct","dicom_01","sujet_005_20121001_095610RTMEDULLO1SPIRALEs006a005.nii.gz")
    
    
    
rd_rescale_file = rd_to_ct(ct_nii, rd_nii, 156, output_dir) 
# 156 = cut_brain_index integer in the z axis, where to cut the matrix(image)
