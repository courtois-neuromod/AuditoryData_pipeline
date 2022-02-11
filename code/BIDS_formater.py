import pandas as pd
import os
from shutil import copyfile
import glob


if __name__ == "__main__":
    import BIDS_utils as utils

else:
    from . import BIDS_utils as utils


# Create a list of the subjects and a reference path for the results
subjects = ['Sub01', 'Sub02', 'Sub03', 'Sub04', 'Sub05', 'Sub06']

# Retrieve the database
df = utils.retrieve_db()
# Manage the empty boxes
df.fillna(value='n/a', inplace=True)

# Specify the columns to be used for each test
# -> Subject and session settings data
columns_conditions = ['Participant_ID', 'DATE',
                      'Protocol name', 'Protocol condition',
                      'Scan type']

# Initialize empty lists to be filled with the proper column titles
# for each test
columns_tymp = []
columns_tymp_R = []
columns_tymp_L = []

columns_reflex = []
columns_reflex_R = []
columns_reflex_L = []

columns_PTA = []
columns_PTA_R = []
columns_PTA_L = []

columns_MTX = []
columns_MTX_L1 = []
columns_MTX_L2 = []

# Generate column title lists to be able to extract the data for each test
for i in df.columns:
    if i.endswith("_RE") is True:
        columns_tymp.append(i)
        columns_tymp_R.append(i)
    elif i.endswith("_LE") is True:
        columns_tymp.append(i)
        columns_tymp_L.append(i)
    elif i.startswith("REFLEX_RE_") is True:
        columns_reflex.append(i)
        columns_reflex_R.append(i)
    elif i.startswith("REFLEX_LE_") is True:
        columns_reflex.append(i)
        columns_reflex_L.append(i)
    elif i.startswith("RE_") is True:
        columns_PTA.append(i)
        columns_PTA_R.append(i)
    elif i.startswith("LE_") is True:
        columns_PTA.append(i)
        columns_PTA_L.append(i)
    elif i.startswith("MTX1") is True:
        columns_MTX.append(i)
        columns_MTX_L1.append(i)
    elif i.startswith("MTX2") is True:
        columns_MTX.append(i)
        columns_MTX_L2.append(i)

# Generate the column titles to be used in the tsv files
x_tymp = ["order", "side", 'type', 'tpp', 'ecv', 'sc', 'tw']
x_reflex = ["order", "side",
            "500_hz", "1000_hz", "2000_hz", "4000_hz", 'noise']
x_PTA = ["order", "side", "250_hz", "500_hz", "1000_hz",
         "2000_hz", "3000_hz", "4000_hz", "6000_hz", "8000_hz",
         "9000_hz", "10000_hz", "11200_hz", "12500_hz",
         "14000_hz", "16000_hz", "18000_hz", "20000_hz"]
x_MTX = ["order", "language", "practice", "sp_bin_no_bin",
         "sp_l_no_bin", "sp_r_no_bin", "sp_l_no_l", "sp_r_no_r"]


def subject_extractor(df, subject_ID):
    """
    This function extracts from the database all the lines that are linked to a
    single participant and returns them into a new dataframe.
    INPUTS:
    -df: database in a pandas dataframe format
    -subject_ID: the subject ID to look for in the Participant_ID column of the
                 dataframe
    OUTPUTS:
    -returns a dataframe containing only the selected participant's lines
    """
    
    mask = df['Participant_ID'] == subject_ID
    sub_df = df[mask].reset_index(drop=True)

    return sub_df


def create_folder_subjects(subject, parent_path):
    """This function creates by-subject folders in the BIDS_data/ folder
    INPUTS:
    -subject: subject ID used in the database's dataframe (format: Sub0X)
    -parent_path: path to get inside the BIDS_data/ folder
    OUTPUTS:
    -folder for the provided subject ID in the BIDS_data/ folder
    -NO specific return to the script
    """
    
    dir_content = os.listdir(parent_path)
    dir_content.sort()
    sub_ID = subject.lstrip("Sub")

    if dir_content.count(f"sub-{sub_ID}") == 1:
        pass
    else:
        os.mkdir(os.path.join(parent_path, f"sub-{sub_ID}"))


# Check if the session-level folders exist for each participant
# If not, create them
def create_folder_session(subject, session_count):
    """
    This function creates by-session folders in the BIDS_data/sub-0*/ folder
    INPUTS:
    -subject: subject ID used in the database's dataframe (format: Sub0X)
    -session_count: number of line(s) in the by-subject dataframe
    OUTPUTS:
    -folders for each session in the provided subject's folder
    -NO specific return to the script
    """
    
    sub_ID = subject.lstrip("Sub")
    children_path = os.path.join(parent_path, f"sub-{sub_ID}")
    dir_content = os.listdir(children_path)

    for j in range(1, session_count + 1):
        if dir_content.count(f"ses-{j:02d}") == 1:
            pass
        else:
            os.mkdir(os.path.join(children_path, f"ses-{j:02d}"))


if __name__ == "__main__":
    master_path = ".."    
    result_path = os.path.join(master_path, "results")
    
    # Verifications:
    # - existence of the "BIDS_data" folder
    # - existence of the run-level json sidecar originals
    #   (tymp, reflex, PTA, MTX)
    # If not, creates them.
    utils.result_location(result_path)

    # Folder where to put each participants' folder
    parent_path = os.path.join(result_path, "BIDS_data")

    for i in subjects:

        # Check if the subject-level folders exist
        # If not, create them
        create_folder_subjects(i, parent_path)
        
        # Extraction of all the session for the subject
        data_sub = subject_extractor(df, i)
        
        # Creation of a folder for each session
        create_folder_session(i, len(data_sub))

        # Extraction of the test columns
        tymp = utils.eliminate_columns(data_sub,
                                       columns_conditions,
                                       columns_tymp)
        reflex = utils.eliminate_columns(data_sub,
                                         columns_conditions,
                                         columns_reflex)
        pta = utils.eliminate_columns(data_sub,
                                      columns_conditions,
                                      columns_PTA)
        mtx = utils.eliminate_columns(data_sub,
                                      columns_conditions,
                                      columns_MTX)

        # Dataframe reconstruction
        utils.extract_tymp(tymp, columns_tymp_R,
                           columns_tymp_L, x_tymp,
                           parent_path)
        utils.extract_reflex(reflex, columns_reflex_R,
                             columns_reflex_L, x_reflex,
                             parent_path)
        utils.extract_pta(pta, columns_PTA_R,
                          columns_PTA_L, x_PTA,
                          parent_path)
        utils.extract_mtx(mtx, columns_MTX_L1,
                          columns_MTX_L2, x_MTX,
                          parent_path)

        print(f"The tsv and json files for {i} have been created.")


    # This code section is present if, for any reason, the .tsv files are not
    # properly saved. You will first need to activate the "import glob" line
    # (line 2). It is then possible to replace the variable "ext"'s value in
    # the save_df function with ".csv" and rerun the script with this section
    # to rename all the files with the correct ".tsv" file extansion.

    # file_list = glob.glob(os.path.join(parent_path, "sub-*/ses-*/*.csv"))

    # for path in file_list:
    #     new_path = os.path.splitext(path)[0]+".tsv"
    #     os.system(f"mv {path} {new_path}")


else:
    result_path = os.path.join("results")

    # Verifications:
    # - existence of the "BIDS_data" folder
    # - existence of the run-level json sidecar originals
    #   (tymp, reflex, PTA, MTX)
    # If not, creates them.
    utils.result_location(result_path)

    # Folder where to put each participants' folder
    parent_path = os.path.join(result_path, "BIDS_data")

    for i in subjects:
        # Creation of the subject folder
        create_folder_subjects(i, parent_path)

        # Extraction of all the session for the subject
        data_sub = subject_extractor(df, i)

        # Creation of a folder for each session
        create_folder_session(i, len(data_sub))

        # Extraction of the test columns
        tymp = utils.eliminate_columns(data_sub,
                                       columns_conditions,
                                       columns_tymp)
        reflex = utils.eliminate_columns(data_sub,
                                         columns_conditions,
                                         columns_reflex)
        pta = utils.eliminate_columns(data_sub,
                                      columns_conditions,
                                      columns_PTA)
        mtx = utils.eliminate_columns(data_sub,
                                      columns_conditions,
                                      columns_MTX)

        # Dataframe reconstruction
        utils.extract_tymp(tymp, columns_tymp_R,
                               columns_tymp_L, x_tymp,
                               parent_path)
        utils.extract_reflex(reflex, columns_reflex_R,
                                   columns_reflex_L, x_reflex,
                                   parent_path)
        utils.extract_pta(pta, columns_PTA_R,
                             columns_PTA_L, x_PTA,
                             parent_path)
        utils.extract_mtx(mtx, columns_MTX_L1,
                             columns_MTX_L2, x_MTX,
                             parent_path)

        print(f"The tsv and json files for {i} have been created.")


    # This code section is present if, for any reason, the .tsv files are not
    # properly saved. You will first need to activate the "import glob" line
    # (line 2). It is then possible to replace the variable "ext"'s value in
    # the save_df function with ".csv" and rerun the script with this section
    # to rename all the files with the correct ".tsv" file extansion.

    # file_list = glob.glob(os.path.join(parent_path, "sub-*/ses-*/*.csv"))

    # for path in file_list:
    #     new_path = os.path.splitext(path)[0]+".tsv"
    #     os.system(f"mv {path} {new_path}")
