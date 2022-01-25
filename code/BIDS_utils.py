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
    OUTPUTS: returns the database in a pandas dataframe
    """
    
    url_share = input("Enter the Google Spreadsheet URL: ")
    url_csv = url_share.replace("/edit#gid=", "/export?format=csv&gid=")
    df = pd.read_csv(url_csv, sep=',', na_filter=True)
    return(df)
