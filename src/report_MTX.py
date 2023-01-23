import os
import pandas as pd
import colorama as color
import statistics as stats

from src import report_common as report
from src import common_functions as common

# Initialize colorama
color.init(autoreset=True)


def report_df(ls_cond, ls_L1=None, ls_L2=None, L1=None, L2=None):
    """
    This function takes the lists of tested conditions and calculated
    before/after variations and places them into a dataframe.
    INPUTS:
    -L1: language used as the first language
    -L2: language used as the second language
    -ls_cond: list of the tested conditions
    -ls_L1: the [post - pre] differences for the first language
    -ls_L2: the [post - pre] differences for the second language
    OUTPUTS
    -returns a report dataframe ready to be saved into .tsv format
    """

    ls_cond.append("Mean")
    ls_cond.append("Standard Deviation")
    ls_cond.append("Language")

    if ls_L1 is None and ls_L2 is None:
        print(color.Fore.RED
              + color.Style.BRIGHT
              + ("\nCRITICAL ERROR: One of the script loops sent no valid "
                 "values to the report_df function.\nPlease correct the data "
                 "files in the database and run this functionality again.\n"))
        return None

    elif ls_L2 is None:
        columns = ["condition", "diff_L1"]
        var_len = ls_L1
        case = 1

    elif ls_L1 is None:
        columns = ["condition", "diff_L2"]
        var_len = ls_L2
        case = 2

    else:
        columns = ["condition", "diff_L1", "diff_L2"]
        var_len = ls_L1
        case = 3

    ls2df = []

    for i in range(0, len(ls_cond)):
        row = []
        row.append(ls_cond[i])

        if i < len(var_len):
            if case == 1:
                row.append(ls_L1[i])

            elif case == 2:
                row.append(ls_L2[i])

            elif case == 3:
                row.append(ls_L1[i])
                row.append(ls_L2[i])

        else:
            if ls_cond[i] == "Mean":
                if case == 1:
                    try:
                        stats.mean(ls_L1)
                    except TypeError:
                        row.append("n/a")
                    else:
                        row.append(stats.mean(ls_L1))

                elif case == 2:
                    try:
                        stats.mean(ls_L2)
                    except TypeError:
                        row.append("n/a")
                    else:
                        row.append(stats.mean(ls_L2))

                elif case == 3:
                    try:
                        stats.mean(ls_L1)
                    except TypeError:
                        row.append("n/a")
                    else:
                        row.append(stats.mean(ls_L1))

                    try:
                        stats.mean(ls_L1)
                    except TypeError:
                        row.append("n/a")
                    else:
                        row.append(stats.mean(ls_L1))

            elif ls_cond[i] == "Standard Deviation":
                if case == 1:
                    try:
                        stats.pstdev(ls_L1)
                    except TypeError:
                        row.append("n/a")
                    else:
                        row.append(stats.pstdev(ls_L1))

                elif case == 2:
                    try:
                        stats.pstdev(ls_L2)
                    except TypeError:
                        row.append("n/a")
                    else:
                        row.append(stats.pstdev(ls_L2))

                elif case == 3:
                    try:
                        stats.pstdev(ls_L1)
                    except TypeError:
                        row.append("n/a")
                    else:
                        row.append(stats.pstdev(ls_L1))

                    try:
                        stats.pstdev(ls_L2)
                    except TypeError:
                        row.append("n/a")
                    else:
                        row.append(stats.pstdev(ls_L2))

            elif ls_cond[i] == "Language":
                if case == 1:
                    row.append(L1)
                elif case == 2:
                    row.append(L2)
                elif case == 3:
                    row.append(L1)
                    row.append(L2)

        ls2df.append(row)

    df = pd.DataFrame(data=ls2df, columns=columns)

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
    -returns the list of before/after response variations
    """

    df_1.reset_index(drop=True, inplace=True)
    df_2.reset_index(drop=True, inplace=True)

    ls_diff = []

    for a in columns:
        try:
            float(df_2.at[0, a])
        except ValueError:
            pass
        else:
            df_2.at[0, a] = float(df_2.at[0, a])

        try:
            float(df_1.at[0, a])
        except ValueError:
            pass
        else:
            df_1.at[0, a] = float(df_1.at[0, a])

        if (df_2.at[0, a] == "n/a"
                or df_1.at[0, a] == "n/a"):
            value = "n/a"
            ls_diff.append(value)

        elif type(df_2.at[0, a]) != str and type(df_1.at[0, a]) != str:
            value = df_2.at[0, a] - df_1.at[0, a]
            ls_diff.append(value)

    return ls_diff


def report_prepost(ls, sub, path_ses, path_reports):
    """
    This function takes a list of couples of pre/post sessions, calculates
    the response differences, generates and saves a dataframe
    INPUTS:
    -ls: list of pre/post session couples
    -sub: subject ID
    -path_ses: path inside the subject's BIDS folder
               ([repo_root]/results/BIDS_data/[subject_folder]/)
    -path_reports: path inside the report folder
                   ([repo_root]/results/reports/)
    OUTPUTS:
    -saves dataframe into .tsv files
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
            if a.find("MTX") != -1 and a.endswith(".tsv"):
                file_pre = os.path.join(path_pre, a)
            else:
                pass

        for b in file_ls_post:
            if b.find("MTX") != -1 and b.endswith(".tsv"):
                file_post = os.path.join(path_post, b)
            else:
                pass

        df_pre = pd.read_csv(file_pre, sep="\t", na_filter=False)
        df_post = pd.read_csv(file_post, sep="\t", na_filter=False)

        language = df_pre.at[0, "language"]

        df_pre.drop(columns=["order", "language", "practice"], inplace=True)
        df_post.drop(columns=["order", "language", "practice"], inplace=True)
        df_pre.astype(float, copy=False, errors="ignore")
        df_post.astype(float, copy=False, errors="ignore")

        columns = df_pre.columns.tolist()

        # Calculation of the [post - pre] differences
        ls_diff = extract_diff(df_pre, df_post, columns)

        # Dataframe generation
        df_report = report_df(columns, ls_L1=ls_diff, L1=language)

        if df_report is None:
            print(color.Fore.YELLOW
                  + color.Style.BRIGHT
                  + "Files to verify:\n"
                  + color.Fore.CYAN
                  + color.Style.NORMAL
                  + f"{file_pre}\n"
                  + color.Fore.WHITE
                  + "and\n"
                  + color.Fore.CYAN
                  + f"{file_post}\n")
            exit()

        else:

            # Save df_report to .tsv
            report_filename = f"{sub}_report-MTX_{i[0]}_{i[1]}.tsv"
            report_path = os.path.join(path_reports, sub, report_filename)
            df_report.to_csv(report_path, sep="\t", index=False)


def report_48(ls, ses_baseline, sub, filepath_ref,
              df_ref, path_ses, path_reports):
    """
    This function takes a list of [48h, 7 days] sessions, calculates
    the response differences between these sessions and the baseline session,
    generates and saves a dataframe
    INPUTS:
    -ls: list of pre/post session couples
    -ses_baseline: session identifier for the reference/baseline session used
                   to make the comparisons
    -sub: subject ID
    -filepath_ref: path to the reference .tsv file
    -df_ref: dataframe with the reference session data
    -path_ses: path inside the subject's BIDS folder
               ([repo_root]/results/BIDS_data/[subject_folder]/)
    -path_reports: path inside the report folder
                   ([repo_root]/results/reports/)
    OUTPUTS:
    -saves dataframe into .tsv files
    -NO specific return to the script
    """

    if len(df_ref) == 1:
        l1_bsl = df_ref.at[0, "language"]
        l2_bsl = None
        l1 = True
        l2 = False

    elif len(df_ref) == 2:
        l1_bsl = df_ref.at[0, "language"]
        l2_bsl = df_ref.at[1, "language"]
        l1 = True
        l2 = True

    df_ref.drop(columns=["order", "language", "practice"], inplace=True)
    df_ref.astype(float, copy=False, errors="ignore")

    for i in ls:

        # Extraction of the post-procedure dataframe
        path_48 = os.path.join(path_ses, i)

        file_ls_48 = os.listdir(path_48)
        file_ls_48.sort()

        for a in file_ls_48:
            if a.find("MTX") != -1 and a.endswith(".tsv"):
                file_48 = os.path.join(path_48, a)
            else:
                pass

        df_48 = pd.read_csv(file_48, sep="\t", na_filter=False)

        if len(df_48) == 1:
            l1_48 = df_48.at[0, "language"]
            l2_48 = None

            if l1_bsl == l1_48:
                pass
            else:
                l1 = False

        elif len(df_48) == 2:
            l1_48 = df_48.at[0, "language"]
            l2_48 = df_48.at[1, "language"]

            if l1_bsl == l1_48:
                pass
            else:
                print(color.Fore.YELLOW
                      + (f"\nWARNING: The first language presented to {sub} "
                         f"during {i} ({l1_48}) doesn't match the first "
                         f"language presented in {ses_baseline} ({l1_bsl})."
                         f"\nThe MTX data for the chronic phase of {i} will "
                         f"not be processed.\n"))
                l1 = False

            if l2_bsl == l2_48:
                pass
            else:
                print(color.Fore.YELLOW
                      + (f"\nWARNING: The second language presented to {sub} "
                         f"during {i} ({l1_48}) doesn't match the second "
                         f"language presented in {ses_baseline} ({l1_bsl})."
                         f"\nThe MTX data for the chronic phase of {i} will "
                         f"not be processed.\n"))
                l2 = False

        df_48.drop(columns=["order", "language", "practice"], inplace=True)
        df_48.astype(float, copy=False, errors="ignore")

        columns = df_ref.columns.tolist()

        if l1 is True and l2 is True:
            # Calculation of the [post - pre] differences
            ls_diff_L1 = extract_diff(df_ref.loc[[0]], df_48.loc[[0]], columns)
            ls_diff_L2 = extract_diff(df_ref.loc[[1]], df_48.loc[[1]], columns)

            # Dataframe generation
            df_report = report_df(columns,
                                  ls_L1=ls_diff_L1, ls_L2=ls_diff_L2,
                                  L1=l1_bsl, L2=l2_bsl)

        elif l1 is True and l2 is False:
            # Calculation of the [post - pre] differences
            ls_diff_L1 = extract_diff(df_ref.loc[[0]], df_48.loc[[0]], columns)

            # Dataframe generation
            df_report = report_df(columns, ls_L1=ls_diff_L1, L1=l1_bsl)

        elif l1 is False and l2 is True:
            # Calculation of the [post - pre] differences
            ls_diff_L2 = extract_diff(df_ref.loc[[1]], df_48.loc[[1]], columns)

            # Dataframe generation
            df_report = report_df(columns, ls_L2=ls_diff_L2, L2=l2_bsl)

        elif l1 is False and l2 is False:
            print(color.Fore.RED
                  + (f"\nERROR: The order of presentation of the languages "
                     f"used with {sub} during {i} ({l1_48}, {l2_48}) doesn't "
                     f"match the order used during {ses_baseline} ({l1_bsl}, "
                     f"{l2_bsl}).\nThe MTX data for the chronic phase of {i} "
                     f"will not be processed.\nPlease correct the data files "
                     f"in the database and run this functionality again."))
            continue

        if df_report is None:
            print(color.Fore.YELLOW
                  + color.Style.BRIGHT
                  + "Files to verify:\n"
                  + color.Fore.CYAN
                  + color.Style.NORMAL
                  + f"{filepath_ref}\n"
                  + color.Fore.WHITE
                  + "and\n"
                  + color.Fore.CYAN
                  + f"{file_48}\n")
            exit()

        else:

            # Save df_report to .tsv
            report_filename = f"{sub}_report-MTX_{ses_baseline}_{i}.tsv"
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

        # Extract reference data
        ses_baseline = ses_ls_df.at[1, "session_id"]

        # Path inside the Baseline folder
        path_base_ses = os.path.join(path_ses, ses_baseline)
        ls_folder_baseline = os.listdir(path_base_ses)

        baseline_ref = None
        stop_48 = False

        for a in ls_folder_baseline:
            if a.find("MTX") != -1 and a.endswith(".tsv"):
                baseline_ref = a
            else:
                pass

        if baseline_ref is None:
            print(color.Fore.RED
                  + (f"ERROR: No MTX baseline file was found for {i} in "
                     f"the {ses_baseline} folder.\nThe MTX data for the "
                     f"chronic phase of {i} will not be processed.\n"))
            stop_48 = True

        else:
            pass

        # Extract list of pre/post and 48h post scan session IDs
        ls_prepost, ls_48 = report.extract_ses_ls(ses_ls_df, i, "MTX")

        # Production of the reports regarding the accute phase effects
        report_prepost(ls_prepost, i, path_ses, path_reports)

        if stop_48 is True:
            pass

        else:

            # Path to the Baseline PTA data file
            filepath_ref = os.path.join(path_base_ses, baseline_ref)
            df_ref = pd.read_csv(filepath_ref, sep="\t", na_filter=False)

            # Production of the reports regarding the chronic phase effects
            report_48(ls_48, ses_baseline, i, filepath_ref,
                      df_ref, path_ses, path_reports)

        print(color.Fore.GREEN
              + f"The MTX reports for {i} have been generated.\n")


if __name__ == "__main__":
    root_path = ".."
    result_path = os.path.join(root_path, "results")
    master_run(result_path)

else:
    pass
