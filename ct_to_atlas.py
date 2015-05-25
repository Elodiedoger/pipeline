"""hola."""
# System import
import os
import subprocess
import argparse


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

if __name__ == "__main__":

    # Create a commande line parsing
    parser = argparse.ArgumentParser(description='Run experimental design')
    parser.add_argument('-rdir',
                        type=str,
                        default=os.getcwd(),
                        help='root directory that contains data folder')
    parser.add_argument('subject_folder',
                        type=str,
                        help='name of the subject folder')
    args = parser.parse_args()

    # For directory preparation
    output_dir = os.path.join(args.rdir,
                              'results',
                              'ct_to_atlas',
                              args.subject_folder)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    sujet_data_dir = os.path.join(args.rdir,
                                  'dataset',
                                  args.subject_folder)
    # Setup input directories
    atlas_nii = os.path.join(sujet_data_dir, "atlas", "atlas_t1.nii.gz")
    ct_cut_brain_nii = os.path.join(args.rdir, "results", "ct_to_mri",
                                    args.subject_folder, "ct_cut_brain.nii.gz")
    trans_2 = os.path.join(args.rdir, "results", "ct_to_mri",
                           args.subject_folder,
                           "trans_2.txt")
    trans_nl = os.path.join(args.rdir, "mri_to_atlas", args.subject_folder,
                            "t1_to_atlas_nl_field.nii.gz")
    # Setup output directories
    combined_trans = os.path.join(output_dir,
                                  "combined_ct_to_atlas_field.nii.gz")
    ct_cut_brain_to_atlas_nii = os.path.join(output_dir,
                                             "cut_ct_to_atlas.nii.gz")
    # Run ct to atlas function
    (ct_cut_brain_to_atlas_nii,
     combined_trans) = ct_to_atlas(trans_nl,
                                   trans_2,
                                   atlas_nii,
                                   ct_cut_brain_nii,
                                   combined_trans,
                                   ct_cut_brain_to_atlas_nii)
