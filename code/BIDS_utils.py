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

