"""Execute preprocessing pipeline."""
import os
import argparse
import pipeline_steps as ps

if __name__ == "__main__":

    # Create a commande line parsing
    parser = argparse.ArgumentParser(description='Run experimental design')
    parser.add_argument('-rdir',
                        type=str,
                        default=os.getcwd(),
                        help='root directory that contains data folder')
    parser.add_argument('subject',
                        type=int,
                        help='id of the subject')
    args = parser.parse_args()

    subject_folder = "sujet{0:03d}".format(args.subject)

    ps.ct_to_atlas(trans_nl, trans_2, atlas_nii, ct_cut_brain_nii,
                   combined_trans, ct_cut_brain_to_atlas_nii)
