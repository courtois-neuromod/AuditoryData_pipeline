import os
import pandas as pd
# import glob

from src import BIDS_utils as utils


# Create a list of the subjects and a reference path for the results
subjects = ['Sub01', 'Sub02', 'Sub03', 'Sub04', 'Sub05', 'Sub06']

# Specify the columns to be used for each test
# -> Subject and session settings data
columns_conditions = ["Participant_ID", "DATE",
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

def fetch_db():
    """This function retrieves a database to work on.
    INPUTS: none
    OUTPUTS:
    -returns a dataframe containing the database to use
    """

    df = utils.retrieve_db()

    # Manage the empty boxes
    df.fillna(value='n/a', inplace=True)

    return df


def fetch_oae_data(data_path):
    path = os.path.join(data_path, "OAE")
    ls_file = os.listdir(path)
    #print(ls_file)
    
    ls_of_ls = []
    
    for i in ls_file:
        single_test_ls = i.rstrip(".csv").split("_")
        ls_of_ls.append(single_test_ls)
    
    df = pd.DataFrame(ls_of_ls,
                      columns=["Participant_ID",
                               "Condition",
                               "Test",
                               "Ear"])
    #print(df)
    
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
def create_folder_session(subject, session_count, parent_path):
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


def master_run(data_path, result_path):

    # retrieve a database
    df = fetch_db()
    oae_file_list, oae_tests_df = fetch_oae_data(data_path)

    # Verifications:
    # - existence of the "BIDS_data" folder
    # - existence of the run-level json sidecar originals
    #   (tymp, reflex, PTA, MTX)
    # If not, creates them.
    utils.result_location(result_path)

    parent_path = os.path.join(result_path, "BIDS_data")

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
        create_folder_subjects(i, parent_path)

        # Extraction of all the session for the subject
        data_sub = subject_extractor(df, i)
        data_oae_sub = subject_extractor(oae_tests_df, i)

        #print("\ndata_oae_sub\n", data_oae_sub)
        
        data_sub.insert(loc=3, column="Session_ID", value=None)
        #print("\ndata_sub\n", data_sub)

        # Add a session line for the post-scan OAE condition
        k = 0        
        while k < len(data_sub):

            data_sub["Session_ID"][k] = f"{k+1:02d}"
            #print(data_sub)


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
        create_folder_session(i, len(data_sub), parent_path)

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

        #print(pta)
        #print(oae)
        
        # Replace PTA values "130" with "No response"
        for n in columns_PTA:
            for p in range(0, len(pta)):
                #print(pta.iloc[p][n])
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
                            x_teoae, data_path, result_path)
        utils.extract_dpoae(oae, data_oae_sub, oae_file_list,
                            x_dpoae, data_path, result_path)

        print(f"The tsv and json files for {i} have been created.\n")

    # This code section is present if, for any reason, the .tsv files are not
    # properly saved. You will first need to activate the "import glob" line
    # (line 2). It is then possible to replace the variable "ext"'s value in
    # the save_df function with ".csv" and rerun the script with this section
    # to rename all the files with the correct ".tsv" file extansion.

    # file_list = glob.glob(os.path.join(parent_path, "sub-*/ses-*/*.csv"))

    # for path in file_list:
    #     new_path = os.path.splitext(path)[0]+".tsv"
    #     os.system(f"mv {path} {new_path}")


if __name__ == "__main__":
    root_path = ".."
    data_path = os.path.join(root_path, "data", "auditory_tests")
    result_path = os.path.join(root_path, "results")

    master_run(data_path, result_path)
    print("\n")


else:
    pass
