import os
import pandas as pd
import colorama as color
import statistics as stats

from src import report_common as report
from src import common_functions as common

# Initialize colorama
color.init(autoreset=True)


def report_df(ls_f, ls_R, ls_L):
    """
    This function takes the lists of tested frequencies and calculated
    before/after variations and places them into a dataframe.
    It also calculates and add to the dataframe the mean and standard
    deviations values for each of the ears
    INPUTS:
    -ls_f: list of the tested frequencies
    -ls_R: the [post - pre] differences for the right ear
    -ls_L: the [post - pre] differences for the left ear
    OUTPUTS
    -returns a report dataframe ready to be saved into .tsv format
    """

    ls_f.append("Mean")
    ls_f.append("Standard Deviation")
    columns = ["freq", "diff_L", "diff_R"]

    try:
        stats.mean(a for a in ls_L if a is not None)
    except stats.StatisticsError:
        mean_L = "n/a"
    else:
        mean_L = stats.mean(a for a in ls_L if a is not None)

    try:
        stats.mean(b for b in ls_R if b is not None)
    except stats.StatisticsError:
        mean_R = "n/a"
    else:
        mean_R = stats.mean(b for b in ls_R if b is not None)

    try:
        stats.pstdev(c for c in ls_L if c is not None)
    except stats.StatisticsError:
        stdev_L = "n/a"
    else:
        stdev_L = stats.pstdev(c for c in ls_L if c is not None)

    try:
        stats.pstdev(d for d in ls_R if d is not None)
    except stats.StatisticsError:
        stdev_R = "n/a"
    else:
        stdev_R = stats.pstdev(d for d in ls_R if d is not None)

    ls2df = []

    for i, element_i in enumerate(ls_f)):
        row = []
        row.append(element_i)

        try:
            float(element_i)
        except ValueError:
            if element_i == "Mean":
                row.append(mean_L)
                row.append(mean_R)
            elif element_i == "Standard Deviation":
                row.append(stdev_L)
                row.append(stdev_R)
        else:
            try:
                float(ls_L[i])
            except TypeError:
                row.append("n/a")
            else:
                row.append(ls_L[i])

            try:
                float(ls_R[i])
            except TypeError:
                row.append("n/a")
            else:
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
    ls_f = []

    for i in range(0, len(df_1)):
        value_pre = df_1.at[i, "oae"]
        noise_pre = df_1.at[i, "noise"]
        conf_pre = df_1.at[i, "confidence"]
        value_post = df_2.at[i, "oae"]
        noise_post = df_2.at[i, "noise"]
        conf_post = df_2.at[i, "confidence"]

        if (value_pre > noise_pre
                and value_post > noise_post
                and conf_pre >= 95
                and conf_post >= 95):
            value = value_post - value_pre
        else:
            value = None

        if df_1.at[i, "side"] == "R":
            ls_R.append(value)
        elif df_1.at[i, "side"] == "L":
            ls_L.append(value)

        if df_1.at[i, "freq"] in ls_f:
            pass
        else:
            ls_f.append(df_1.at[i, "freq"])

    return ls_R, ls_L, ls_f


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
            if a.find("TEOAE") != -1 and a.endswith(".tsv"):
                file_pre = os.path.join(path_pre, a)
            else:
                pass

        for b in file_ls_post:
            if b.find("TEOAE") != -1 and b.endswith(".tsv"):
                file_post = os.path.join(path_post, b)
            else:
                pass

        df_pre = pd.read_csv(file_pre, sep="\t", na_filter=False)
        df_post = pd.read_csv(file_post, sep="\t", na_filter=False)

        # Calculation of the [post - pre] differences
        ls_diff_R, ls_diff_L, ls_f = extract_diff(df_pre, df_post)

        # Dataframe generation
        df_report = report_df(ls_f, ls_diff_R, ls_diff_L)

        # Save df_report to .tsv
        report_filename = (f"{sub}_report-TEOAE_{i[0]}_{i[1]}.tsv")
        report_path = os.path.join(path_reports, sub, report_filename)
        df_report.to_csv(report_path, sep="\t", index=False)


def report_48(ls, ses_baseline, sub, df_ref, path_ses, path_reports):
    """
    This function takes a list of [48h, 7 days] sessions, calculates
    the response differences between these sessions and the baseline session,
    generates and saves the results dataframes
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
            if a.find("TEOAE") != -1 and a.endswith(".tsv"):
                file_48 = os.path.join(path_48, a)
            else:
                pass

        df_48 = pd.read_csv(file_48, sep="\t", na_filter=False)

        # Calculation of the [post - pre] differences
        ls_diff_R, ls_diff_L, ls_f2 = extract_diff(df_ref, df_48)

        # Dataframe generation
        df_report = report_df(ls_f2, ls_diff_R, ls_diff_L)

        # Save df_report to .tsv
        report_filename = (f"{sub}_report-TEOAE_{ses_baseline}_{i}.tsv")
        report_path = os.path.join(path_reports, sub, report_filename)
        df_report.to_csv(report_path, sep="\t", index=False)


def master_run(result_path):

    # Prompt the user for the baseline session to use as reference
    bsl_index = common.baseline_ID()

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

        # Extract reference data
        ses_baseline = ses_ls_df.at[bsl_index, "session_id"]

        # Path inside the Baseline folder
        path_base_ses = os.path.join(path_ses, ses_baseline)
        ls_folder_baseline = os.listdir(path_base_ses)

        baseline_ref = None
        stop_48 = False

        for a in ls_folder_baseline:
            if a.find("TEOAE") != -1 and a.endswith(".tsv"):
                baseline_ref = a
            else:
                pass

        if baseline_ref is None:
            ses_baseline_retry = ses_ls_df.at[1, "session_id"]

            path_base_ses = os.path.join(path_ses, ses_baseline_retry)
            ls_folder_baseline = os.listdir(path_base_ses)

            for x in ls_folder_baseline:
                if x.find("TEOAE") != -1 and x.endswith(".tsv"):
                    baseline_ref = x
                    print(color.Fore.YELLOW
                          + (f"WARNING: No TEOAE data file was found for {i} "
                             f"in the {ses_baseline} folder.\nThe TEOAE data "
                             f"file found in {ses_baseline_retry} was used as "
                             f"a replacement.\n"))
                else:
                    pass

            if baseline_ref is None:
                print(color.Fore.RED
                      + (f"ERROR: No TEOAE baseline file was found for {i} in "
                         f"the {ses_baseline} or the {ses_baseline_retry} "
                         f"folders.\nThe TEOAE data for the chronic phase of "
                         f"{i} will not be processed.\n"))
                stop_48 = True

        else:
            pass

        # Extract list of pre/post and 48h post scan session IDs
        ls_prepost, ls_48 = report.extract_ses_ls(ses_ls_df, i, "OAE")

        # Production of the report regarding the accute phase effects
        report_prepost(ls_prepost, i, path_ses, path_reports)

        if stop_48 is True:
            pass

        else:

            # Path to the Baseline DPOAE data file
            filepath_ref = os.path.join(path_base_ses, baseline_ref)
            df_ref = pd.read_csv(filepath_ref, sep="\t", na_filter=False)

            # Production of the report regarding the chronic phase effects
            report_48(ls_48, ses_baseline, i, df_ref, path_ses, path_reports)

        print(color.Fore.GREEN
              + f"The TEOAE reports for {i} have been generated.\n")


if __name__ == "__main__":
    root_path = ".."
    result_path = os.path.join(root_path, "results")
    master_run(result_path)

else:
    pass
