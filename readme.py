import os



file = ""

def flip_file(file) :
    """ flip or not the ct"""
    with open(file) as openfile:
        for item in openfile.readlines():
            subject_name, swap_map = item.split()

    # Get a dict with tupples
    subject_swap = zip(subject_name, swap_map)

    # Get a dictionnarry

    subject_swap_dict = dict(subject_swap)

    # get value from key

    value = subject_swap_dict.get("subj_id")

return value

if value == 1
