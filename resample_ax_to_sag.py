from nilearn.image import resample_img
import nibabel
import os

def resample_mri_1_on_mri2(image1_path, image2_path):
    """ resample image1_path on image2_path, image1_path is the image to be
    transform"""

    #resampling_path = '/Users/dogerdespeville/Desktop/resampling_im.nii'

    # load the images
    mri_seq1 = nibabel.load(image1_path)
    mri_seq2 = nibabel.load(image2_path)

    # get the affine matrix

    mri_seq1_affine = mri_seq1.get_affine()
    print mri_seq1_affine

    # Resample a mri to
    resampling_im = resample_img(mri_seq2, mri_seq1_affine)
    #print "Executing resampling {0}".format(sujet)

    # Save the file
    #nibabel.save(resampling_im, resampling_path)


    resampling_im.to_filename('/Users/dogerdespeville/Desktop/resampling2_im.nii')

    return resampling_im, resampling_path

if __name__ == '__main__':
    image1_path = '/Users/dogerdespeville/Desktop/sag.nii'
    image2_path = '/Users/dogerdespeville/Desktop/bravo.nii'

    resampling_im, resampling_path = resample_mri_1_on_mri2(image1_path, image2_path)


