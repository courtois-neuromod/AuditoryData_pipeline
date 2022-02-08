import pandas as pd
import os
from shutil import copyfile
import json_sidecar_generator as jsg
# import glob

def retrieve_db():
    """
    This function prompts the user for a URL and retrieves the Google
    Spreadsheet located at the specified URL.
    INPUTS: none
    OUTPUTS:
    -returns the database in a pandas dataframe
    """

    url_share = input("Enter the Google Spreadsheet URL: ")
    url_csv = url_share.replace("/edit#gid=", "/export?format=csv&gid=")
    df = pd.read_csv(url_csv, sep=',', na_filter=True)
    return(df)


def result_location(result_path):
    """
    This function makes sure that the destination for the formated file exists.
    INPUTS:
    -result_path: path of the results folder
    OUTPUTS: none
    """
    
    # Results location existence verifications
    content_result_path = os.listdir(result_path)
    #print(content_result_path)
    content_result_path.sort()
    #print(content_result_path)
    
    # Verification of the existence of the "BIDS_data" folder
    if content_result_path.count("BIDS_data") == 1:
        print("The results/BIDS_data folder is present.")
        pass
    else:
        os.mkdir(os.path.join(result_path, "BIDS_data"))
        print("The results/BIDS_data folder was created.")

    parent_path = os.path.join(result_path, "BIDS_data")

    # Verification of the existence of the json sidecar originals
    if content_result_path.count("BIDS_sidecars_originals") == 1:
        print("The results/BIDS_sidecars_originals folder is present.")
        sidecar_folder = os.path.join(result_path, "BIDS_sidecars_originals")
        sidecar_list = os.listdir(sidecar_folder)
        sidecar_list.sort()
        if (sidecar_list.count("tymp_run_level.json") == 1
            and sidecar_list.count("reflex_run_level.json") == 1
            and sidecar_list.count("pta_run_level.json") == 1
            and sidecar_list.count("mtx_run_level.json") == 1):
            print("The run-level json sidecars for tymp, reflex, PTA and "\
                  "MTX are presents.")
            pass
        else:
            # run json_sidecar_generator.py
            jsg
            print("The run-level json sidecars for tymp, reflex, PTA and "\
                  "MTX were created in the results/BIDS_sidecars_originals "\
                  "folder.")
    else:
        # run json_sidecar_generator.py
        jsg
        print("The run-level json sidecars for tymp, reflex, PTA and MTX were "\
              "created in the results/BIDS_sidecars_originals folder.")


# Single test sub-df extraction from each participant's sub-df
def eliminate_columns(sub_df, columns_conditions, test_columns):
    to_keep = columns_conditions + test_columns
    df_test = sub_df[to_keep]

    return df_test


def save_df(data_tosave_df, single_test_df, index, test, run="01"):
    """
    This function is used to save the tsv files and json sidecars.
    INPUTS:
    -df to be saved in the tsv file
    -df containing the test columns for a single participant
    -the line index (in single_test_df) linked with the data to save
     (data_tosave_df)
    -the selected test marker
    OUTPUTS:
    -saved tsv file
    -NO specific return to the script
    """
    
    sub = single_test_df['Participant_ID'][index].lstrip('Sub_')

    if (index + 1) < 10:
        ses = '0' + str(index + 1)
    else:
        ses = str(index + 1)

    # The next variable ("ext") can take the value ".csv".
    # The last code section must then be activated
    ext = '.tsv'

    path = os.path.join(parent_path, 'sub-' + sub, 'ses-' + ses)
    file_name = os.path.join('sub-' + sub + '_ses-' + ses + '_task-' + test
                             + '_run-' + run + "_beh")

    data_tosave_df.to_csv(os.path.join(path, file_name + ext), sep='\t')

    json_origin = os.path.join("..", "results", "BIDS_sidecars_originals")

    if test == "Tymp":
        copyfile(os.path.join(json_origin, "tymp_run_level.json"),
                 os.path.join(path, file_name + ".json"))
    elif test == "Reflex":
        copyfile(os.path.join(json_origin, "reflex_run_level.json"),
                 os.path.join(path, file_name + ".json"))
    elif test == "PTA":
        copyfile(os.path.join(json_origin, "pta_run_level.json"),
                 os.path.join(path, file_name + ".json"))
    elif test == "MTX":
        copyfile(os.path.join(json_origin, "mtx_run_level.json"),
                 os.path.join(path, file_name + ".json"))
