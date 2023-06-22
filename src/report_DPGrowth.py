import os
import numpy as np
import pandas as pd
import colorama as color
import statistics as stats

from scikit-learn.linear_model import LinearRegression
from scikit-learn.metrics import mean_squared_error, mean_absolute_error

from src import report_common as report
from src import common_functions as common

# Initialize colorama
color.init(autoreset=True)


def linreg_values(x_pre, y_pre, x_post, y_post):
    """
    This function computes linear regression models on the data and returns
    those models keys values (a, b and mean errors).
    INPUTS:
    -x_pre: array of the presented stimuli intensities (before)
    -y_pre: array of the measured responses (before)
    -x_post: array of the presented stimuli intensities (after)
    -y_post: array of the measured responses (after)
    OUTPUTS:
    -returns a list of two lists of keys values (a, b, mean errors)
     ([["before" values], ["after" values]])
    """

    ls2do = [x_pre, y_pre, x_post, y_post]
    
    for i in range(0, len(ls2do)):
        ls2do[i] = ls2do[i][ls2do[i] != None]

    #print(ls2do)

    x_pre, y_pre, x_post, y_post = ls2do
    
    #print(y_pre)
    
    # Linear regression values computation (a, b and mean errors)
    model_pre = LinearRegression()
    model_post = LinearRegression()

    model_pre.fit(x_pre.reshape(-1, 1), y_pre)
    model_post.fit(x_post.reshape(-1, 1), y_post)

    # Linear regression values: Coefficient (a)
    a_pre = model_pre.coef_[0]
    a_post = model_post.coef_[0]

    # Linear regression values: Intercept (b)
    b_pre = model_pre.intercept_
    b_post = model_post.intercept_

    # Linear regression values: mean errors
    pct_pre = model_pre.predict(x_pre.reshape(-1, 1))
    pct_post = model_post.predict(x_post.reshape(-1, 1))

    # Mean Squared Errors
    mse_pre = mean_squared_error(y_pre, pct_pre)
    mse_post = mean_squared_error(y_post, pct_post)

    # Mean Absolute Errors
    mae_pre = mean_absolute_error(y_pre, pct_pre)
    mae_post = mean_absolute_error(y_post, pct_post)

    ls_pre = [a_pre, b_pre, mse_pre, mae_pre]
    ls_post = [a_post, b_post, mse_post, mae_post]

    ls_of_ls = [ls_pre, ls_post]
    
    #print(ls_of_ls)

    return ls_of_ls


def report_df(ls_diff, ls_xpre, ls_ypre, ls_xpost, ls_ypost):
    """
    This function takes the arrays of tested frequencies and calculated
    before/after variations and places them into a dataframe.
    It also calculates and add to the dataframe the mean and standard
    deviations values for each of the ears
    INPUTS:
    -ls_diff: list of the calculated [after - before] difference lists
              ([Left side list, Right side list])
    -ls_xpre: list of the presented stimuli intensities arrays (before)
              ([Left side array, Right side array])
    -ls_ypre: list of the measured responses arrays (before)
              ([Left side array, Right side array])
    -ls_xpost: list of the presented stimuli intensities arrays (after)
               ([Left side array, Right side array])
    -ls_ypost: list of the measured responses arrays (after)
               ([Left side array, Right side array])
    OUTPUTS
    -returns a report dataframe ready to be saved into .tsv format
    """

    #print("ls_diff", ls_diff)
    
    ls_diff_no_none_0 = list(filter(lambda i: i != None, ls_diff[0]))
    ls_diff_no_none_1 = list(filter(lambda i: i != None, ls_diff[1]))

    names_columns = ["l2_target", "diff_L", "diff_R"]

    intensity_column = [65, 60, 55, 50, 45, 40, 35,
                        "Mean", "Standard Deviation",
                        "Reg_Pre_coef", "Reg_Pre_intercept",
                        "Reg_Pre_MSE", "Reg_Pre_MAE",
                        "Reg_Post_coef", "Reg_Post_intercept",
                        "Reg_Post_MSE", "Reg_Post_MAE"]

    # Linear model computations and value extractions (a, b, mse, mae)
    if len(ls_diff_no_none_0) < 1:
        values_L = [[None, None, None, None], [None, None, None, None]]
    else:
        values_L = linreg_values(ls_xpre[0], ls_ypre[0],
                                 ls_xpost[0], ls_ypost[0])
    if len(ls_diff_no_none_1) < 1:
        values_R = [[None, None, None, None], [None, None, None, None]]
    else:
        values_R = linreg_values(ls_xpre[1], ls_ypre[1],
                                 ls_xpost[1], ls_ypost[1])

    ls2df = []

    #print("values_L", values_L)
    #print("values_R", values_R)

    for i in range(0, len(intensity_column)):
        row = []
        row.append(intensity_column[i])
        
        try:
            float(intensity_column[i])
        except ValueError:
            if intensity_column[i] == "Mean":
                if len(ls_diff_no_none_0) < 1:
                    row.append(None)
                else:
                    row.append(stats.mean(ls_diff_no_none_0))
                #print(row)
                if len(ls_diff_no_none_1) < 1:
                    row.append(None)
                else:
                    row.append(stats.mean(ls_diff_no_none_1))
                #print(row)
            elif intensity_column[i] == "Standard Deviation":
                if len(ls_diff_no_none_0) < 1:
                    row.append(None)
                else:
                    row.append(stats.pstdev(ls_diff_no_none_0))
                #print(row)
                if len(ls_diff_no_none_1) < 1:
                    row.append(None)
                else:
                    row.append(stats.pstdev(ls_diff_no_none_1))
                #print(row)
            elif intensity_column[i] == "Reg_Pre_coef":
                row.append(values_L[0][0])
                row.append(values_R[0][0])
            elif intensity_column[i] == "Reg_Pre_intercept":
                row.append(values_L[0][1])
                row.append(values_R[0][1])
            elif intensity_column[i] == "Reg_Pre_MSE":
                row.append(values_L[0][2])
                row.append(values_R[0][2])
            elif intensity_column[i] == "Reg_Pre_MAE":
                row.append(values_L[0][3])
                row.append(values_R[0][3])
            elif intensity_column[i] == "Reg_Post_coef":
                row.append(values_L[1][0])
                row.append(values_R[1][0])
            elif intensity_column[i] == "Reg_Post_intercept":
                row.append(values_L[1][1])
                row.append(values_R[1][1])
            elif intensity_column[i] == "Reg_Post_MSE":
                row.append(values_L[1][2])
                row.append(values_R[1][2])
            elif intensity_column[i] == "Reg_Post_MAE":
                row.append(values_L[1][3])
                row.append(values_R[1][3])
        else:
            row.append(ls_diff[0][i])
            row.append(ls_diff[1][i])
        ls2df.append(row)

    #print("ls2df", ls2df)

    df = pd.DataFrame(data=ls2df, columns=names_columns)

    print(df)

    return df


def list_builder(df_1, df_2):
    """
    This function calculates the response variations between two acquistion
    sessions and extract the test values (stimulations and measured responses)
    for the linear regression models.
    INPUTS:
    -df_1: first timepoint's dataframe (reference)
    -df_2: second timepoint's dataframe (data after scan session)
    OUTPUTS:
    -returns a list of 10 elements (5 for each ear):
            -before/after response variations
            -presented stimuli intensities (before)
            -presented stimuli intensities (after)
            -measured responses (before)
            -measured responses (after)
    """

    diff_L = []
    xpre_L = []
    xpost_L = []
    ypre_L = []
    ypost_L = []
    diff_R = []
    xpre_R = []
    xpost_R = []
    ypre_R = []
    ypost_R = []

    for i in range(0, len(df_1)):
        value_pre = df_1.at[i, "dp"]
        noise_pre = df_1.at[i, "noise+2sd"]
        value_post = df_2.at[i, "dp"]
        noise_post = df_2.at[i, "noise+2sd"]
        
        if (value_pre > noise_pre and value_post > noise_post):
            value = value_post - value_pre
        else:
            value = None

        if df_1.at[i, "side"] == "L":
            diff_L.append(value)
            
            if value_pre > noise_pre:
                xpre_L.append(df_1.at[i, "l2"])
                ypre_L.append(df_1.at[i, "dp"])
            else:
                xpre_L.append(None)
                ypre_L.append(None)

            if value_post > noise_post:
                xpost_L.append(df_2.at[i, "l2"])
                ypost_L.append(df_2.at[i, "dp"])
            else:
                xpost_L.append(None)
                ypost_L.append(None)

        elif df_1.at[i, "side"] == "R":
            diff_R.append(value)

            if value_pre > noise_pre:
                xpre_R.append(df_1.at[i, "l2"])
                ypre_R.append(df_1.at[i, "dp"])
            else:
                xpre_R.append(None)
                ypre_R.append(None)

            if value_post > noise_post:
                xpost_R.append(df_2.at[i, "l2"])
                ypost_R.append(df_2.at[i, "dp"])
            else:
                xpost_R.append(None)
                ypost_R.append(None)

    ls_of_ls = [diff_L, xpre_L, xpost_L, ypre_L, ypost_L,
                diff_R, xpre_R, xpost_R, ypre_R, ypost_R]

    return ls_of_ls


def report_prepost(ls, sub, path_ses, path_reports):
    """
    This function takes a list of couples of pre/post sessions, calculates
    the response differences, generates and saves the results dataframes
    INPUTS:
    -ls: list of pre/post session couples
    -sub: subject ID
    -path_ses: path inside the subject's BIDS folder
               ([repo_root]/results/BIDS_data/[subject_folder]/)
    -path_reports: path inside the report folder
                   ([repo_root]/results/reports/)
    OUTPUTS:
    -saves dataframes into .tsv file
    -NO specific return to the script
    """

    for i in ls:

        # Extraction of the pairs of dataframes
        path_pre = os.path.join(path_ses, i[0])
        path_post = os.path.join(path_ses, i[1])

        file_ls_pre = os.listdir(path_pre)
        file_ls_pre.sort()
        file_ls_post = os.listdir(path_post)
        file_ls_post.sort()

        a = 0
        while a < len(file_ls_pre):
            if (file_ls_pre[a].find("DPGrowth") != -1
                    and file_ls_pre[a].endswith(".tsv")):
                a += 1
            else:
                file_ls_pre.pop(a)

        b = 0
        while b < len(file_ls_post):
            if (file_ls_post[b].find("DPGrowth") != -1
                    and file_ls_post[b].endswith(".tsv")):
                b += 1
            else:
                file_ls_post.pop(b)

        ls_df_pre = []

        for c in file_ls_pre:

            # path to each of the prescan session .tsv files
            tsv_filepath = os.path.join(path_pre, c)
            growth_df = pd.read_csv(tsv_filepath, sep="\t", na_filter=False)

            if growth_df["freq2"][0] == 2002:
                df_pre2 = growth_df
                ls_df_pre.append(df_pre2)
            elif growth_df["freq2"][0] == 4004:
                df_pre4 = growth_df
                ls_df_pre.append(df_pre4)
            elif growth_df["freq2"][0] == 6006:
                df_pre6 = growth_df
                ls_df_pre.append(df_pre6)

        ls_df_post = []

        for d in file_ls_post:

            # path to each of the postscan session .tsv files
            tsv_filepath = os.path.join(path_post, d)
            growth_df = pd.read_csv(tsv_filepath, sep="\t", na_filter=False)

            if growth_df["freq2"][0] == 2002:
                df_post2 = growth_df
                ls_df_post.append(df_post2)
            elif growth_df["freq2"][0] == 4004:
                df_post4 = growth_df
                ls_df_post.append(df_post4)
            elif growth_df["freq2"][0] == 6006:
                df_post6 = growth_df
                ls_df_post.append(df_post6)

        # Calculation of the [post - pre] differences
        for e in range(0, len(ls_df_pre)):
            if ls_df_pre[e].at[0, "freq2"] == 2002:
                ls_2 = list_builder(ls_df_pre[e], ls_df_post[e])
            elif ls_df_pre[e].at[0, "freq2"] == 4004:
                ls_4 = list_builder(ls_df_pre[e], ls_df_post[e])
            elif ls_df_pre[e].at[0, "freq2"] == 6006:
                ls_6 = list_builder(ls_df_pre[e], ls_df_post[e])

        ls_diff = [[ls_2[0], ls_2[5]],
                   [ls_4[0], ls_4[5]],
                   [ls_6[0], ls_6[5]]]

        #print(ls_diff)

        # Test data formating for the linear regression models
        ls_xpre = [[np.array(ls_2[1]), np.array(ls_2[6])],
                   [np.array(ls_4[1]), np.array(ls_4[6])],
                   [np.array(ls_6[1]), np.array(ls_6[6])]]

        ls_ypre = [[np.array(ls_2[3]), np.array(ls_2[8])],
                   [np.array(ls_4[3]), np.array(ls_4[8])],
                   [np.array(ls_6[3]), np.array(ls_6[8])]]

        ls_xpost = [[np.array(ls_2[2]), np.array(ls_2[7])],
                    [np.array(ls_4[2]), np.array(ls_4[7])],
                    [np.array(ls_6[2]), np.array(ls_6[7])]]

        ls_ypost = [[np.array(ls_2[4]), np.array(ls_2[9])],
                    [np.array(ls_4[4]), np.array(ls_4[9])],
                    [np.array(ls_6[4]), np.array(ls_6[9])]]

        ls_diff_tag = ["2", "4", "6"]

        # Dataframe generation
        for f in ls_diff_tag:
            if f == "2":
                df_report = report_df(ls_diff[0],
                                      ls_xpre[0], ls_ypre[0],
                                      ls_xpost[0], ls_ypost[0])
            elif f == "4":
                df_report = report_df(ls_diff[1],
                                      ls_xpre[1], ls_ypre[1],
                                      ls_xpost[1], ls_ypost[1])
            elif f == "6":
                df_report = report_df(ls_diff[2],
                                      ls_xpre[2], ls_ypre[2],
                                      ls_xpost[2], ls_ypost[2])

            # Save df_report to .tsv
            report_filename = (f"{sub}_report-Growth{f}"
                               + f"_{i[0]}_{i[1]}.tsv")
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
            if a.find("DPGrowth") != -1 and a.endswith(".tsv"):
                file_48 = os.path.join(path_48, a)
            else:
                pass

        df_48 = pd.read_csv(file_48, sep="\t", na_filter=False)

        # Calculation of the [post - pre] differences
        ls_4 = list_builder(df_ref, df_48)

        ls_diff = [ls_4[0], ls_4[5]]

        # Test data formating for the linear regression models
        ls_xpre = [np.array(ls_4[1]), np.array(ls_4[6])]

        ls_ypre = [np.array(ls_4[3]), np.array(ls_4[8])]

        ls_xpost = [np.array(ls_4[2]), np.array(ls_4[7])]

        ls_ypost = [np.array(ls_4[4]), np.array(ls_4[9])]

        # Dataframe generation
        df_report = report_df(ls_diff,
                              ls_xpre, ls_ypre,
                              ls_xpost, ls_ypost)

        # Save df_report to .tsv
        report_filename = (f"{sub}_report-Growth4_{ses_baseline}_{i}.tsv")
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
            if a.find("DPGrowth") != -1 and a.endswith(".tsv"):
                baseline_ref = a
            else:
                pass

        if baseline_ref is None:
            ses_baseline_retry = ses_ls_df.at[1, "session_id"]

            path_base_ses = os.path.join(path_ses, ses_baseline_retry)
            ls_folder_baseline = os.listdir(path_base_ses)

            for x in ls_folder_baseline:
                if x.find("DPGrowth") != -1 and x.endswith(".tsv"):
                    baseline_ref = x
                    print(color.Fore.YELLOW
                          + (f"WARNING: No DP-growth data file was found for "
                             f"{i} in the {ses_baseline} folder.\nThe "
                             f"DP-growth data file found in "
                             f"{ses_baseline_retry} was used as a "
                             f"replacement.\n"))
                else:
                    pass

            if baseline_ref is None:
                print(color.Fore.RED
                      + (f"ERROR: No DP-growth baseline file was found for "
                         f"{i} in the {ses_baseline} or the "
                         f"{ses_baseline_retry} folders.\nThe DP-growth "
                         f"data for the chronic phase of {i} will not be "
                         f"processed.\n"))
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

            # Path to the Baseline DPGrowth data file
            filepath_ref = os.path.join(path_base_ses, baseline_ref)
            df_ref = pd.read_csv(filepath_ref, sep="\t", na_filter=False)

            # Production of the report regarding the chronic phase effects
            report_48(ls_48, ses_baseline, i, df_ref, path_ses, path_reports)

        print(color.Fore.GREEN
              + (f"The DP Growth function reports for {i} have been "
                 f"generated.\n"))

if __name__ == "__main__":
    root_path = ".."
    result_path = os.path.join(root_path, "results")
    master_run(result_path)

else:
    pass
