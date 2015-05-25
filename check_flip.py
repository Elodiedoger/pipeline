"""."""
import os
import pandas as pd


def check_flip(flip_path, subject):
    """Check if the subject ct scan has to be flip.

    The information is assumed to be in a hand filled file flip.csv
    the flip.csv file should have column 'subject' with subject number
    and column 'flip' with boolean value.
    If the file is not in LPS orientation then its flip value is True.
    """
    flip_data = pd.read_csv(os.path.join(flip_path, 'flip.csv'))
    return flip_data[flip_data['subject'] == subject]['flip'].tolist()[0]
