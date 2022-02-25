import os
import random
import numpy as np
import pandas as pd


# Random seed for replicability purposes
random.seed(1)

# Test subjects IDs
subjects = ["sub-01", "sub-02", "sub-03", "sub-04", "sub-05", "sub-06"]

# Column names to be used in the .tsv event file
tsv_columns = ["onset", "duration", "frequency",
               "volume", "ear", "trial_type"]

# Number of session files to be generated for each subject
# session_count = 4
Q_session_count = "How many sessions files should be generated "\
                  "for each participant?\n"

# Inter-stimuli interval (sec.)
# ISI = 5
Q_ISI = "What inter-stimuli interval (sec.) should be used in the "\
        "session design?\n"

# Single stimulus file duration (sec.)
# duration = 3
Q_duration = "What stimuli duration (sec.) should be used in the "\
             "session design?\n"


def number_verify(x, low, high):
    """
    This function verifies that an input respects specified conditions.
    INPUTS:
    -x: string-format value to inspect
    -low: lower boundary (included) of the validity interval
    -high: higher boundary (excluded) of the validity interval
    OUTPUTS:
    -returns False if the value x respects the specified conditions
     (to break the loop) or True if the value doesn't respect them (to
     stay in the loop).
    """

    # Is it a valid number?
    if x.isdigit():
        x = int(x)

        # Is it within the range of the specified conditions?
        # No specified higher boundary
        if high is None:
            if x >= low:
                return False
            else:
                return True

        # With a specified higher boundary
        elif high is not None:

            if low == high:
                if x == low:
                    return False
                else:
                    return True

            elif low != high:
                if x >= low and x < high:
                    return False
                else:
                    return True

    else:
        return True


def prompt_n_verify(question, low=0, high=None):
    """
    This function ask the provided question, verify the validity of the
    user's answer and retruns it when valid.
    INPUTS:
    -question: text of the question to ask to the user
    -low: lower boundary (included) of the validity interval
          -> Default value = 0
    -high: higher boundary (excluded) of the validity interval
           -> Default value = None
    OUTPUTS:
    -returns the valid user's answer to the asked question
    """

    loop = True

    while loop:
        prompt = input(question)
        loop = number_verify(prompt, low, high)

    prompt = int(prompt)
    return prompt


def master_run(output_path):

    duration = prompt_n_verify(Q_duration)
    ISI = prompt_n_verify(Q_ISI)
    session_count = prompt_n_verify(Q_session_count)

    # Session design file generation loop for each subject
    for i in subjects:
        sub_number = ""

        for k in range(0, len(i)):
            if i[k].isdigit():
                sub_number += str(i[k])
            else:
                continue

        # File generation for each session
        for j in range(0, session_count):

            # Dataframe containing the subject specific intensities to be used
            data_path = os.path.join(output_path, "MRI_sessions")
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
                ls_info_filename = random_stimuli_ls[m].split("_")
                frequency = ls_info_filename[0].rstrip("hz")
                level = "-" + ls_info_filename[2].rstrip("dBFS")
                ear = ls_info_filename[3].rstrip(".wav")

                df["onset"][m] = m * duration + m * ISI
                df["duration"][m] = duration
                df["frequency"][m] = frequency
                df["volume"][m] = level
                df["ear"][m] = ear
                df["trial_type"][m] = "pure_tone"

            # Save the dataframe to .tsv
            ses_ID = str(j+1).zfill(3)
            filename = f"sub-{sub_number}_ses-{ses_ID}_"\
                       f"task-puretones_events.tsv"

            df.to_csv(os.path.join(data_path, "stimuli", filename),
                      sep="\t", index=False)


if __name__ == "__main__":
    master_run("../data")

else:
    pass
