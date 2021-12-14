import os
import random
import numpy as np
import pandas as pd

# Test subjects IDs
subjects = ["sub-01", "sub-02", "sub-03", "sub-04", "sub-05", "sub-06"]

# Number of session files to be generated for each subject
session_count = 4

# Random seed for replicability purposes
random.seed(1)

# Inter-stimuli interval (sec.)
ISI = 5

# Single stimulus file duration (sec.)
duration = 3

# Column names to be used in the .tsv event file
tsv_columns = ["trial_type", "onset", "duration"]

# Session design file generation loop for each subject
for i in subjects:

    # File generation for each session
    for j in range(0, session_count):
        sub_number = ""

        for k in range(0, len(i)):
            if i[k].isdigit():
                sub_number += str(i[k])
            else:
                continue

        # Dataframe containing the subject specific intensities to be used
        data_path = os.path.join("..", "data", "MRI_sessions")
        stimuli_L = pd.read_csv(os.path.join(data_path,
                                             ("sub-" + sub_number +
                                              "_desc-L.tsv")),
                                sep="\t")
        stimuli_R = pd.read_csv(os.path.join(data_path,
                                             ("sub-" + sub_number + 
                                              "_desc-R.tsv")),
                                sep="\t")
        stimuli_df = pd.concat([stimuli_L, stimuli_R], ignore_index=True)

        # Dataframe to list
        stimuli_ls = stimuli_df.to_numpy().flatten().tolist()

        # Randomized presentation order list
        random_stimuli_ls = random.sample(stimuli_ls, len(stimuli_ls))

        # Build a dataframe to receive the different values to be saved
        df = pd.DataFrame(columns=tsv_columns,
                          index=np.arange(0, len(random_stimuli_ls)))
        
        for m in range(0, len(df)):
            df["trial_type"][m] = random_stimuli_ls[m]
            df["onset"][m] = m * duration + m * ISI
            df["duration"][m] = duration

        # Save the dataframe to .tsv
        ses_ID = str(j+1).zfill(3)
        filename = f"sub-{sub_number}_ses-{ses_ID}_task-puretones_events.tsv"
        
        df.to_csv(os.path.join(data_path, "stimuli", filename), sep="\t")
