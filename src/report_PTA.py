import os
import pandas as pd
import colorama as color
# import statistics as stats

from src import report_common as report
from src import common_functions as common

# Initialize colorama
color.init(autoreset=True)


def report_df(ls_freq, ls_R, ls_L):
    """
    This function takes the lists of tested frequencies and calculated
    before/after variations and places them into a dataframe.
    INPUTS:
    -ls_freq: list of the tested frequencies
    -ls_R: the [post - pre] differences for the right ear
    -ls_L: the [post - pre] differences for the left ear
    OUTPUTS
    -returns a report dataframe ready to be saved into .tsv format
    """

#    ls_freq.append("Mean")
#    ls_freq.append("Standard Deviation")

    columns = ["freq", "diff_L", "diff_R"]
    ls2df = []

    for i in range(0, len(ls_freq)):
        row = []
        row.append(ls_freq[i])

#        try:
#            float(ls_freq[i])
#        except ValueError:
#            if ls_freq[i] == "Mean":
#                row.append(stats.mean(ls_L))
#                row.append(stats.mean(ls_R))
#            elif ls_freq[i] == "Standard Deviation":
#                row.append(stats.pstdev(ls_L))
#                row.append(stats.pstdev(ls_R))
#        else:
#            row.append(ls_L[i])
#            row.append(ls_R[i])
        row.append(ls_L[i])
        row.append(ls_R[i])

        ls2df.append(row)

    df = pd.DataFrame(data=ls2df, columns=columns)

    return df


def distrib_df(columns, ls_freq, ls_R, ls_L, test_type):
    """
    This function takes the tested frequencies, regroup them by their
    calculated before/after variations and places them in a dataframe
    INPUTS:
    -columns: original BIDS dataset's PTA file column titles
    -ls_freq: list of the tested frequencies
    -ls_R: the [post - pre] differences for the right ear
    -ls_L: the [post - pre] differences for the left ear
    -test_type: variable to keep track of small variations between the two
                experimental conditions processed by this script
    OUTPUTS:
    -returns a distribution dataframe ready to be saved into .tsv format
    """

    ls_threshold = []

    for i in ls_L:
        if i in ls_threshold:
            pass
        else:
            try:
                float(i)
            except ValueError:
                pass
            else:
                ls_threshold.append(float(i))

    for j in ls_R:
        if j in ls_threshold:
            pass
        else:
            try:
                float(j)
            except ValueError:
                pass
            else:
                ls_threshold.append(float(j))

    ls_threshold.sort()

    data = []
    for u in range(0, len(ls_threshold)):
        data.append([])

    for k in range(0, len(data)):
        data[k].append(ls_threshold[k])
        data[k].append([])
        data[k].append([])
        for a in range(0, len(ls_R)):
            if ls_R[a] == ls_threshold[k]:
                data[k][2].append(columns[a])
            else:
                pass
        for b in range(0, len(ls_L)):
            if ls_L[b] == ls_threshold[k]:
                data[k][1].append(columns[b])
            else:
                pass

    if test_type == "prepost":
        names_columns = ["pre-post_diff", "freq_R", "freq_L"]
    elif test_type == 48:
        names_columns = ["48post-baseline_diff", "freq_L", "freq_R"]

    df = pd.DataFrame(data=data, columns=names_columns)

    return df


def extract_diff(df_1, df_2, columns):
    """
    This function calculates the response variations between two
    acquisition sessions.
    INPUTS:
    -df_1: first timepoint's dataframe (reference)
    -df_2: second timepoint's dataframe (data after scan session)
    -columns: list of columns to go through
    OUTPUTS:
    -returns three lists: -two lists (one for each ear) of before/after
                           response variations
                          -one list with the tested frequencies
    """

    for i in [0, 1]:
        ls_diff = []
        ls_freq = []

        for a in columns:
            ls_freq.append(int(a.rstrip("_hz")))

            try:
                float(df_2.at[i, a])
            except ValueError:
                pass
            else:
                df_2.at[i, a] = float(df_2.at[i, a])

            try:
                float(df_1.at[i, a])
            except ValueError:
                pass
            else:
                df_1.at[i, a] = float(df_1.at[i, a])

            if (df_2.at[i, a] == "n/a"
                    or df_1.at[i, a] == "n/a"):
                value = "n/a"
                ls_diff.append(value)

            elif (df_2.at[i, a] != "No response"
                  and df_1.at[i, a] != "No response"):
                value = df_2.at[i, a] - df_1.at[i, a]
                ls_diff.append(value)

            elif (df_2.at[i, a] == "No response"
                  and df_1.at[i, a] != "No response"):
                value_1 = df_1.at[i, a]
                value = f"After = NR ({value_1} before)"
                ls_diff.append(value)

            elif (df_2.at[i, a] != "No response"
                  and df_1.at[i, a] == "No response"):
                value_2 = df_2.at[i, a]
                value = f"Before = NR ({value_2} after)"
                ls_diff.append(value)

            elif (df_2.at[i, a] == "No response"
                  and df_1.at[i, a] == "No response"):
                value = "Both = NR"
                ls_diff.append(value)

        if i == 0:
            ls_R = ls_diff
        elif i == 1:
            ls_L = ls_diff

    return ls_R, ls_L, ls_freq


def report_prepost(ls, sub, path_ses, path_reports):
    """
    This function takes a list of couples of pre/post sessions, calculates
    the response differences, generates and saves two dataframes (report and
    distribution of variations)
    INPUTS:
    -ls: list of pre/post session couples
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

        # Extraction of the pair of dataframes
        path_pre = os.path.join(path_ses, i[0])
        path_post = os.path.join(path_ses, i[1])

        file_ls_pre = os.listdir(path_pre)
        file_ls_pre.sort()
        file_ls_post = os.listdir(path_post)
        file_ls_post.sort()

        for a in file_ls_pre:
            if a.find("PTA") != -1 and a.endswith(".tsv"):
                file_pre = os.path.join(path_pre, a)
            else:
                pass

        for b in file_ls_post:
            if b.find("PTA") != -1 and b.endswith(".tsv"):
                file_post = os.path.join(path_post, b)
            else:
                pass

        df_pre = pd.read_csv(file_pre, sep="\t", na_filter=False)
        df_post = pd.read_csv(file_post, sep="\t", na_filter=False)

        df_pre.drop(columns=["order", "side"], inplace=True)
        df_post.drop(columns=["order", "side"], inplace=True)
        df_pre.astype(int, copy=False, errors="ignore")
        df_post.astype(int, copy=False, errors="ignore")

        columns = df_pre.columns

        # Calculation of the [post - pre] differences
        ls_diff_R, ls_diff_L, ls_freq = extract_diff(df_pre, df_post, columns)

        # Dataframe generation
        df_report = report_df(ls_freq, ls_diff_R, ls_diff_L)

        # Save df_report to .tsv
        report_filename = f"{sub}_report-PTA_{i[0]}_{i[1]}.tsv"
        report_path = os.path.join(path_reports, sub, report_filename)
        df_report.to_csv(report_path, sep="\t", index=False)

        # Difference distribution report generation
        df_distrib = distrib_df(columns, ls_freq,
                                ls_diff_R, ls_diff_L,
                                "prepost")

        # Save df_distrib to .tsv
        distrib_filename = f"{sub}_distribution-PTA_{i[0]}_{i[1]}.tsv"
        distrib_path = os.path.join(path_reports, sub, distrib_filename)
        df_distrib.to_csv(distrib_path, sep="\t")


def report_48(ls, ses_baseline, sub, df_ref, path_ses, path_reports):
    """
    This function takes a list of [48h, 7 days] sessions, calculates
    the response differences between these sessions and the baseline session,
    generates and save two dataframes (report and distribution of variations)
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

    df_ref.drop(columns=["order", "side"], inplace=True)
    df_ref.astype(int, copy=False, errors="ignore")

    for i in ls:

        # Extraction of the post-procedure dataframe
        path_48 = os.path.join(path_ses, i)

        file_ls_48 = os.listdir(path_48)
        file_ls_48.sort()

        for a in file_ls_48:
            if a.find("PTA") != -1 and a.endswith(".tsv"):
                file_48 = os.path.join(path_48, a)
            else:
                pass

        df_48 = pd.read_csv(file_48, sep="\t", na_filter=False)

        df_48.drop(columns=["order", "side"], inplace=True)
        df_48.astype(int, copy=False, errors="ignore")

        columns = df_ref.columns

        # Calculation of the [post - pre] differences
        ls_diff_R, ls_diff_L, ls_freq = extract_diff(df_ref, df_48, columns)

        # Dataframe generation
        df_report = report_df(ls_freq, ls_diff_R, ls_diff_L)

        # Save df_report to .tsv
        report_filename = f"{sub}_report-PTA_{ses_baseline}_{i}.tsv"
        report_path = os.path.join(path_reports, sub, report_filename)
        df_report.to_csv(report_path, sep="\t", index=False)

        # Difference distribution report generation
        df_distrib = distrib_df(columns, ls_freq, ls_diff_R, ls_diff_L, 48)

        # Save df_distrib to .tsv
        distrib_filename = f"{sub}_distribution-PTA_{ses_baseline}_{i}.tsv"
        distrib_path = os.path.join(path_reports, sub, distrib_filename)
        df_distrib.to_csv(distrib_path, sep="\t")


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
            if a.find("PTA") != -1 and a.endswith(".tsv"):
                baseline_ref = a
            else:
                pass

        if baseline_ref is None:
            ses_baseline_retry = ses_ls_df.at[1, "session_id"]

            path_base_ses = os.path.join(path_ses, ses_baseline_retry)
            ls_folder_baseline = os.listdir(path_base_ses)

            for x in ls_folder_baseline:
                if x.find("PTA") != -1 and x.endswith(".tsv"):
                    baseline_ref = x
                    print(color.Fore.YELLOW
                          + (f"WARNING: No PTA data file was found for {i} in "
                             f"the {ses_baseline} folder.\nThe PTA data file "
                             f"found in {ses_baseline_retry} was used as a "
                             f"replacement.\n"))
                else:
                    pass

            if baseline_ref is None:
                print(color.Fore.RED
                      + (f"ERROR: No PTA baseline file was found for {i} in "
                         f"the {ses_baseline} or the {ses_baseline_retry} "
                         f"folders.\nThe PTA data for the chronic phase of "
                         f"{i} will not be processed.\n"))
                stop_48 = True

        else:
            pass

        # Extract list of pre/post and 48h post scan session IDs
        ls_prepost, ls_48 = report.extract_ses_ls(ses_ls_df, i, "PTA")

        # Production of the reports regarding the accute phase effects
        report_prepost(ls_prepost, i, path_ses, path_reports)

        if stop_48 is True:
            pass

        else:

            # Path to the Baseline PTA data file
            filepath_ref = os.path.join(path_base_ses, baseline_ref)
            df_ref = pd.read_csv(filepath_ref, sep="\t", na_filter=False)

            # Production of the reports regarding the chronic phase effects
            report_48(ls_48, ses_baseline, i, df_ref, path_ses, path_reports)

        print(color.Fore.GREEN
              + f"The PTA reports for {i} have been generated.\n")

if __name__ == "__main__":
    root_path = ".."
    result_path = os.path.join(root_path, "results")
    master_run(result_path)

else:
    pass
