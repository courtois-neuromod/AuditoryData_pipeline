import os
import pandas as pd
import colorama as color
import statistics as stats

from src import report_common as report
from src import common_functions as common

# Initialize colorama
color.init(autoreset=True)


def report_df(ls_f2, ls_R, ls_L):
    """
    This function takes the lists of tested frequencies and calculated
    before/after variations and places them into a dataframe.
    It also calculates and add to the dataframe the mean and standard
    deviations values for each of the ears
    INPUTS:
    -ls_f2: list of the tested frequencies
    -ls_R: the [post - pre] differences for the right ear
    -ls_L: the [post - pre] differences for the left ear
    OUTPUTS
    -returns a report dataframe ready to be saved into .tsv format
    """

    ls_f2.append("Mean")
    ls_f2.append("Standard Deviation")

    columns = ["freq2", "diff_L", "diff_R"]

    ls2df = []

    for i in range(0, len(ls_f2)):
        row = []
        row.append(ls_f2[i])

        try:
            float(ls_f2[i])
        except ValueError:
            if ls_f2[i] == "Mean":
                row.append(stats.mean(ls_L))
                row.append(stats.mean(ls_R))
            elif ls_f2[i] == "Standard Deviation":
                row.append(stats.pstdev(ls_L))
                row.append(stats.pstdev(ls_R))
        else:
            row.append(ls_L[i])
            row.append(ls_R[i])

        ls2df.append(row)

    df = pd.DataFrame(data=ls2df, columns=columns)

    return df


def extract_diff(df_1, df_2):
    """
    This function calculates the response variations between two
    acquisition sessions.
    INPUTS:
    -df_1: first timepoint's dataframe (reference)
    -df_2: second timepoint's dataframe (data after scan session)
    OUTPUTS:
    -returns three lists: -two lists (one for each ear) of before/after
                           response variations
                          -one list with the tested frequencies
    """

    ls_R = []
    ls_L = []
    ls_f2 = []

    for i in range(0, len(df_1)):
        value = df_2.at[i, "dp"] - df_1.at[i, "dp"]

        if df_1.at[i, "side"] == "R":
            ls_R.append(value)
        elif df_1.at[i, "side"] == "L":
            ls_L.append(value)

        if df_1.at[i, "freq2"] in ls_f2:
            pass
        else:
            ls_f2.append(df_1.at[i, "freq2"])

    return ls_R, ls_L, ls_f2


def report_prepost(ls, sub, path_ses, path_reports):
    """
    This function takes a list of couples of pre/post sessions, calculates
    the response differences, generates and saves the results dataframe
    INPUTS:
    -ls: list of pre/post session couples
    -sub: subject ID
    -path_ses: path inside the subject's BIDS folder
               ([repo_root]/results/BIDS_data/[subject_folder]/)
    -path_reports: path inside the report folder
                   ([repo_root]/results/reports/)
    OUTPUTS:
    -saves dataframe into .tsv file
    -NO specific return to the script
    """

    for i in ls:

        # Extraction of the pair of dataframes
        path_pre = os.path.join(path_ses, i[0])
        path_post = os.path.join(path_ses, i[1])

        file_ls_pre = os.listdir(path_pre)
        file_ls_pre.sort()
        file_ls_post = os.listdir(path_post)
        file_ls_post.sort()

        for a in file_ls_pre:
            if a.find("DPOAE") != -1 and a.endswith(".tsv"):
                file_pre = os.path.join(path_pre, a)
            else:
                pass

        for b in file_ls_post:
            if b.find("DPOAE") != -1 and b.endswith(".tsv"):
                file_post = os.path.join(path_post, b)
            else:
                pass

        df_pre = pd.read_csv(file_pre, sep="\t", na_filter=False)
        df_post = pd.read_csv(file_post, sep="\t", na_filter=False)

        # Calculation of the [post - pre] differences
        ls_diff_R, ls_diff_L, ls_f2 = extract_diff(df_pre, df_post)

        # Dataframe generation
        df_report = report_df(ls_f2, ls_diff_R, ls_diff_L)

        # Save df_report to .tsv
        report_filename = (f"{sub}_report-DPOAE_{i[0]}_{i[1]}.tsv")
        report_path = os.path.join(path_reports, sub, report_filename)
        df_report.to_csv(report_path, sep="\t", index=False)


def report_48(ls, ses_baseline, sub, df_ref, path_ses, path_reports):
    """
    This function takes a list of [48h, 7 days] sessions, calculates
    the response differences between these sessions and the baseline session,
    generates and saves the results dataframe
    INPUTS:
    -ls: list of pre/post session couples
    -ses_baseline: session identifier for the reference/baseline session used
                   to make the comparisons
    -sub: subject ID
    -path_ses: path inside the subject's BIDS folder
               ([repo_root]/results/BIDS_data/[subject_folder]/)
    -path_reports: path inside the report folder
                   ([repo_root]/results/reports/)
    OUTPUTS:
    -saves dataframes into .tsv files
    -NO specific return to the script
    """

    for i in ls:

        # Extraction of the post-procedure dataframe
        path_48 = os.path.join(path_ses, i)

        file_ls_48 = os.listdir(path_48)
        file_ls_48.sort()

        for a in file_ls_48:
            if a.find("DPOAE") != -1 and a.endswith(".tsv"):
                file_48 = os.path.join(path_48, a)
            else:
                pass

        df_48 = pd.read_csv(file_48, sep="\t", na_filter=False)

        # Calculation of the [post - pre] differences
        ls_diff_R, ls_diff_L, ls_f2 = extract_diff(df_ref, df_48)

        # Dataframe generation
        df_report = report_df(ls_f2, ls_diff_R, ls_diff_L)

        # Save df_report to .tsv
        report_filename = (f"{sub}_report-DPOAE_{ses_baseline}_{i}.tsv")
        report_path = os.path.join(path_reports, sub, report_filename)
        df_report.to_csv(report_path, sep="\t", index=False)


def master_run(result_path):

    # path to the BIDS formated dataset
    bids_path = os.path.join(result_path, "BIDS_data")

    # Content of the BIDS dataset: list of the subject folders
    try:
        os.listdir(bids_path)
    except FileNotFoundError:
        print(color.Fore.RED
              + ("\nERROR: The BIDS dataset folder is missing.\n"
                 "Please verify that the folder is correctly located "
                 "([repo_root]/results/BIDS_data/) or use the BIDS dataset "
                 "formating function to regenerate the dataset.\n"))
        exit()
    else:
        sub = os.listdir(bids_path)

    sub.sort()

    # Verification/Creation of the reports folder
    path_reports = report.report_file_verif(result_path)

    for i in sub:

        # Verification/Creation of the subjects' report folder
        common.create_folder_subjects(i, path_reports)

        # Path inside the subject's folder
        path_ses = os.path.join(bids_path, i)

        # Content of the subject's folder (sessions + reference .tsv file)
        ls_ses = os.listdir(path_ses)
        ls_ses.sort()

        # Retrieve the reference .tsv file
        filename_index = ls_ses.index(i + "_sessions.tsv")
        ref_filename = ls_ses.pop(filename_index)
        ses_ls_df = pd.read_csv(os.path.join(path_ses, ref_filename), sep="\t")

        # Extract reference data: ses-01 (Baseline #1)
        ses_baseline = ses_ls_df.at[0, "session_id"]

        # Path inside the Baseline #1 folder
        path_base_ses = os.path.join(path_ses, ses_baseline)
        ls_folder_baseline = os.listdir(path_base_ses)

        for a in ls_folder_baseline:
            if a.find("DPOAE") != -1 and a.endswith(".tsv"):
                baseline_ref = a
            else:
                pass

        # Path to the Baseline #1 DPOAE data file
        filepath_ref = os.path.join(path_base_ses, baseline_ref)
        df_ref = pd.read_csv(filepath_ref, sep="\t", na_filter=False)

        # Extract list of pre/post and 48h post scan session IDs
        ls_prepost, ls_48 = report.extract_ses_ls(ses_ls_df, i, "OAE")

        # Production of the report regarding the accute phase effects
        report_prepost(ls_prepost, i, path_ses, path_reports)

        # Production of the report regarding the chronic phase effects
        report_48(ls_48, ses_baseline, i, df_ref, path_ses, path_reports)


if __name__ == "__main__":
    root_path = ".."
    result_path = os.path.join(root_path, "results")
    master_run(result_path)

else:
    pass
