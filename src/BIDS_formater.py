import os
import pandas as pd
# import glob

from datetime import datetime as date
from shutil import copyfile

from src import BIDS_utils as utils
from src import common_functions as common

"""
SCRIPT DESCRIPTION:

This script transforms the auditory test data saved as .csv (OAE tests) or
placed in a properly formatted spreadsheet (other tests).
Template available here:
[ https://docs.google.com/spreadsheets/d/
  1aKakQJvJnvPUouTUciGm3FMlnNAGIX8NXhulbhjq9d4/edit?usp=sharing ]

This script uses the BIDS_formater.py and common_functions.py scripts to be
able to process data and generate a BIDS-format compatible dataset out of
auditory test data.

It can either be used as a standalone script or be used through the UI master
script, main.py.
"""


# Create a list of the subjects and a reference path for the results
subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06']

# Specify the columns to be used for each test
# -> Subject and session settings data
columns_conditions = ["Participant_ID", "Date",
                      "Session_ID", "Protocol name",
                      "Protocol condition", "Scan type"]

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
x_teoae = ["order", "side", "freq", "oae",
           "noise", "snr", "confidence"]
x_dpoae = ["order", "side", "freq1", "freq2", "l1",
           "l2", "dp", "snr", "noise+2sd", "noise+1sd",
           "2f2-f1", "3f1-2f2", "3f2-2f1", "4f1-3f2"]
x_growth = ["order", "side", "freq1", "freq2", "l1",
            "l2", "dp", "snr", "noise+2sd", "noise+1sd",
            "2f2-f1", "3f1-2f2", "3f2-2f1", "4f1-3f2"]

# Specify the protocol conditions including OAE tests
condition_OAE = ["Baseline",
                 "Condition 2 (2-7 days post-scan)",
                 "Condition 3A (OAEs right before the scan)",
                 "Condition 3B (OAEs right after the scan)"]

# Specifiy the different tests used in those different protocol conditions
ls_test = ["Tymp", "Reflex", "PTA", "MTX", "TEOAE", "DPOAE",
           "DPGrowth_2kHz", "DPGrowth_4kHz", "DPGrowth_6kHz"]


def fetch_db(data_path):
    """This function retrieves a database to work on.
    INPUTS:
    -data_path: path to the [repo_root]/data/ folder
    OUTPUTS:
    -returns a dataframe containing the database to use
    """

    df = common.retrieve_db(data_path)

#    if df == "break":
#        quit()
#    else:
#        pass

    # Manage the empty boxes
    df.fillna(value='n/a', inplace=True)

    return df


def fetch_oae_data(data_path):
    """This function retrieves the list of OAE test data files
    INPUTS:
    -data_path: path to the [repo_root]/data/auditory_tests/ folder
    OUTPUTS
    -returns: - the list of all the OAE test data filenames
              - a dataframe containing a by-test breakdown information:
                  - the participant ID
                  - the session experimental condition and date
                  - the type of test
                  - the tested ear
    """

    path = os.path.join(data_path, "OAE")
    ls_file = os.listdir(path)

    ls_of_ls = []

    for i in ls_file:
        single_test_ls = i.rstrip(".csv").split("_")
        ls_of_ls.append(single_test_ls)

    df = pd.DataFrame(ls_of_ls,
                      columns=["Participant_ID",
                               "Condition",
                               "Test",
                               "Ear"])

    return ls_file, df


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


# Check if the session-level folders exist for each participant
# If not, create them
def create_folder_session(subject, session_count, parent_path):
    """
    This function creates by-session folders in the BIDS_data/sub-0*/ folder
    INPUTS:
    -subject: subject ID used in the database's dataframe (format: Sub0X or
              sub-0x)
    -session_count: number of line(s) in the by-subject dataframe
    OUTPUTS:
    -folders for each session in the provided subject's folder
    -returns the list of the session folder names
    """

    if subject.startswith("Sub"):
        sub_ID = subject.lstrip("Sub")
        children_path = os.path.join(parent_path, f"sub-{sub_ID}")

    elif subject.startswith("sub-"):
        children_path = os.path.join(parent_path, subject)

    dir_content = os.listdir(children_path)

    ls_ses = []

    for j in range(1, session_count + 1):
        if dir_content.count(f"ses-{j:02d}") == 1:
            ls_ses.append(f"ses-{j:02d}")
        else:
            os.mkdir(os.path.join(children_path, f"ses-{j:02d}"))
            ls_ses.append(f"ses-{j:02d}")

    return ls_ses, children_path


def master_run(data_path, result_path):
    """
    This is the master function that activates the others.
    INPUTS:
    -data_path: path to the data folder ([repo_root]/data/)
    -result_path: path to the results folder ([repo_root]/results/)
    OUTPUTS:
    -NO specific return to the script (highest function level)
    -prints some feedback to the user in the terminal
    """

    # retrieve a database
    df = fetch_db(data_path)
    auditory_test_path = os.path.join(data_path, "auditory_tests")
    oae_file_list, oae_tests_df = fetch_oae_data(auditory_test_path)

    # Verifications:
    # - existence of the "BIDS_data" folder
    # - existence of the run-level json sidecar originals
    #   (tymp, reflex, PTA, MTX)
    # If not, creates them.
    utils.result_location(result_path)

    parent_path = os.path.join(result_path, "BIDS_data")
    
    # Add the .json sidecar files in the BIDS_data folder
    json_origin = os.path.join(result_path, "BIDS_sidecars_originals")

    copyfile(os.path.join(json_origin, "sessions.json"),
             os.path.join(parent_path, "sessions.json"))
    copyfile(os.path.join(json_origin, "task-Tymp_beh.json"),
             os.path.join(parent_path, "task-Tymp_beh.json"))
    copyfile(os.path.join(json_origin, "task-Reflex_beh.json"),
             os.path.join(parent_path, "task-Reflex_beh.json"))
    copyfile(os.path.join(json_origin, "task-PTA_beh.json"),
             os.path.join(parent_path, "task-PTA_beh.json"))
    copyfile(os.path.join(json_origin, "task-MTX_beh.json"),
             os.path.join(parent_path, "task-MTX_beh.json"))
    copyfile(os.path.join(json_origin, "task-TEOAE_beh.json"),
             os.path.join(parent_path, "task-TEOAE_beh.json"))
    copyfile(os.path.join(json_origin, "task-DPOAE_beh.json"),
             os.path.join(parent_path, "task-DPOAE_beh.json"))
    copyfile(os.path.join(json_origin, "task-DPGrowth_beh.json"),
             os.path.join(parent_path, "task-DPGrowth_beh.json"))

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

    for i in subjects:

        # Check if the subject-level folders exist
        # If not, create them
        common.create_folder_subjects(i, parent_path)

        # Extraction of all the session for the subject
        data_sub = subject_extractor(df, i)
        data_oae_sub = subject_extractor(oae_tests_df, i)

        data_sub.insert(loc=3, column="Session_ID", value=None)

        # Add a session line for the post-scan OAE condition
        k = 0
        while k < len(data_sub):

            data_sub["Session_ID"][k] = f"{k+1:02d}"

            if data_sub["Protocol condition"][k] == ("Condition 3A "
                                                     "(OAEs right before "
                                                     "the scan)"):
                sub_df_A = data_sub.iloc[:k+1]
                sub_df_B = data_sub.iloc[k+1:]

                sub_df_C = data_sub.copy()
                sub_df_C.drop(sub_df_C.index[k+1:], inplace=True)
                sub_df_C.drop(sub_df_C.index[0:k], inplace=True)

                sub_df_C.loc[k, "Protocol condition"] = ("Condition 3B (OAEs "
                                                         "right after the "
                                                         "scan)")
                sub_df_C.loc[k, "Session_ID"] = f"{k+2:02d}"

                ls_columns = sub_df_C.columns.tolist()
                index_tests = ls_columns.index("Tymp_RE")
                del ls_columns[0:index_tests]

                for m in ls_columns:
                    sub_df_C[m][k] = "n/a"

                data_sub = pd.concat([sub_df_A, sub_df_C, sub_df_B])
                data_sub.reset_index(inplace=True, drop=True)

                k += 1

            else:
                pass

            k += 1

        # Creation of a folder for each session
        ls_ses, subject_folder_path = create_folder_session(i,
                                                            len(data_sub),
                                                            parent_path)

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
        oae = data_sub[columns_conditions]

        # Replace PTA values "130" with "No response"
        for n in columns_PTA:
            for p in range(0, len(pta)):
                if pta.iloc[p][n] == 130:
                    pta.iloc[p][n] = "No response"
                else:
                    pass

        # Dataframe reconstruction
        utils.extract_tymp(tymp, columns_tymp_R,
                           columns_tymp_L, x_tymp,
                           result_path)
        utils.extract_reflex(reflex, columns_reflex_R,
                             columns_reflex_L, x_reflex,
                             result_path)
        utils.extract_pta(pta, columns_PTA_R,
                          columns_PTA_L, x_PTA,
                          result_path)
        utils.extract_mtx(mtx, columns_MTX_L1,
                          columns_MTX_L2, x_MTX,
                          result_path)
        utils.extract_teoae(oae, data_oae_sub, oae_file_list,
                            x_teoae, auditory_test_path, result_path)
        utils.extract_dpoae(oae, data_oae_sub, oae_file_list,
                            x_dpoae, auditory_test_path, result_path)
        utils.extract_growth(oae, data_oae_sub, oae_file_list,
                             x_growth, auditory_test_path, result_path)

        # .tsv session-level reference file creation
        column_reference = ["session_id", "session_name",
                            "condition", "delay", "scan_type"]

        for w in ls_test:
            column_reference.append(w)

        index_reference = []
        for x in range(0, len(ls_ses)):
            index_reference.append(x)

        ls_name = []
        ls_condition = []
        ls_delay = []
        ls_scan = []
        for y in range(0, len(data_sub)):

            # Calculation of the number of days since Baseline #1
            index_date_bsl = data_sub.index[(data_sub["Protocol name"]
                                             == "Baseline 1")].tolist()
            date_bsl = date.strptime(data_sub.at[index_date_bsl[0], "Date"],
                                     "%Y-%m-%d")
            date_ses = date.strptime(data_sub.at[y, "Date"],
                                     "%Y-%m-%d")
            value_delay = date_ses - date_bsl

            ls_name.append(data_sub.at[y, "Protocol name"])
            ls_condition.append(data_sub.at[y, "Protocol condition"])
            ls_delay.append(value_delay.days)
            ls_scan.append(data_sub.at[y, "Scan type"])

        ref = pd.DataFrame(index=index_reference, columns=column_reference)

        for a in ref.index:
            ref.at[a, "session_id"] = ls_ses[a]
            ref.at[a, "session_name"] = ls_name[a]
            ref.at[a, "condition"] = ls_condition[a]
            ref.at[a, "delay"] = ls_delay[a]
            ref.at[a, "scan_type"] = ls_scan[a]

            ls_data = utils.retrieve_tests(subject_folder_path, ls_ses[a])

            if "Tymp" in ls_data:
                ref.at[a, "Tymp"] = "X"
            else:
                ref.at[a, "Tymp"] = ""

            if "Reflex" in ls_data:
                ref.at[a, "Reflex"] = "X"
            else:
                ref.at[a, "Reflex"] = ""

            if "PTA" in ls_data:
                ref.at[a, "PTA"] = "X"
            else:
                ref.at[a, "PTA"] = ""

            if "MTX" in ls_data:
                ref.at[a, "MTX"] = "X"
            else:
                ref.at[a, "MTX"] = ""

            if "TEOAE" in ls_data:
                ref.at[a, "TEOAE"] = "X"
            else:
                ref.at[a, "TEOAE"] = ""

            if "DPOAE" in ls_data:
                ref.at[a, "DPOAE"] = "X"
            else:
                ref.at[a, "DPOAE"] = ""

            if "Growth_2" in ls_data:
                ref.at[a, "DPGrowth_2kHz"] = "X"
            else:
                ref.at[a, "DPGrowth_2kHz"] = ""

            if "Growth_4" in ls_data:
                ref.at[a, "DPGrowth_4kHz"] = "X"
            else:
                ref.at[a, "DPGrowth_4kHz"] = ""

            if "Growth_6" in ls_data:
                ref.at[a, "DPGrowth_6kHz"] = "X"
            else:
                ref.at[a, "DPGrowth_6kHz"] = ""

        ref.set_index("session_id", inplace=True)

        ref_name = i + "_sessions"
        ref_save_path = os.path.join(subject_folder_path, ref_name + ".tsv")
        ref.to_csv(ref_save_path, sep="\t")

        print(f"The tsv and json files for {i} have been created.\n")

    # This code section is present if, for any reason, the .tsv files are not
    # properly saved. You will first need to activate the "import glob" line
    # (line 3). It is then possible to replace the variable "ext"'s value in
    # the save_df function (BIDS_utils.py) with ".csv" and rerun the script
    # with this section to rename all the files with the correct ".tsv" file
    # extension.

    # file_list = glob.glob(os.path.join(parent_path, "sub-*/ses-*/*.csv"))

    # for path in file_list:
    #     new_path = os.path.splitext(path)[0]+".tsv"
    #     os.system(f"mv {path} {new_path}")


if __name__ == "__main__":
    root_path = ".."
    data_path = os.path.join(root_path, "data")
    result_path = os.path.join(root_path, "results")

    master_run(data_path, result_path)
    print("\n")


else:
    pass
