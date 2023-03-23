import pandas as pd
import os
import colorama as color

from shutil import copyfile

from src import json_sidecar_generator as jsg

# Initialize colorama
color.init(autoreset=True)

"""
SCRIPT DESCRIPTION:

This script contains multiple functions that are used during the
transformation of the test data saved as .csv (OAE tests) or placed in a
spreadsheet (other tests).

It is not designed to be used as a standalone script, but rather as a slave to
the BIDS_formater.py script.
"""


def result_location(result_path):
    """
    This function makes sure that the destination for the formated file
    exists. If it doesn't, this function creates it.
    INPUTS:
    -result_path: path of the results folder
    OUTPUTS:
    -prints some feedback lines to the user
    -NO specific return to the script
    """

    # Results location existence verifications
    content_result_path = os.listdir(result_path)
    content_result_path.sort()

    # Verification of the existence of the "BIDS_data" folder
    # -> destination of the processed data from the database:
    #    "repository_root/results/BIDS_data/"
    if content_result_path.count("BIDS_data") == 1:
        print("The [repo_root]/results/BIDS_data folder is present.\n")
        pass
    else:
        os.mkdir(os.path.join(result_path, "BIDS_data"))
        print("The [repo_root]/results/BIDS_data folder was created.\n")

    # parent_path = os.path.join(result_path, "BIDS_data")

    # Verification of the existence of the "BIDS_sidecars_originals" folder
    # -> origin of the json files to be copied/pasted along with the
    #    processed data files:
    #    repository_root/results/BIDS_sidecars_originals/
    if content_result_path.count("BIDS_sidecars_originals") == 1:
        print("The [repo_root]/results/BIDS_sidecars_originals folder is "
              "present.\n")

        # Verification of the existence of the json sidecar originals
        sidecar_folder = os.path.join(result_path,
                                      "BIDS_sidecars_originals")
        sidecar_list = os.listdir(sidecar_folder)
        sidecar_list.sort()
        # Making sure that they are all present (tymp, reflex, PTA, MTX)
        if (sidecar_list.count("task-Tymp_beh.json") == 1
                and sidecar_list.count("task-Reflex_beh.json") == 1
                and sidecar_list.count("task-PTA_beh.json") == 1
                and sidecar_list.count("task-MTX_beh.json") == 1
                and sidecar_list.count("task-TEOAE_beh.json") == 1
                and sidecar_list.count("task-DPOAE_beh.json") == 1
                and sidecar_list.count("task-DPGrowth_beh.json") == 1
                and sidecar_list.count("sessions.json") == 1):

            print("The json sidecars for:\n - tymp\n - reflex\n"
                  " - PTA\n - MTX\n - TEOAE\n - DPOAE\n - DP Growth\n"
                  " - sessions\nare present.\n")
            pass
        else:
            # run json_sidecar_generator.py
            print("At least one of the target files is absent: we will "
                  "create it (them) for you.\n")
            jsg.create_sidecars(result_path)
            print("\n")
            print("The json sidecars for:\n - tymp\n - reflex\n - PTA\n"
                  " - MTX\n - TEOAE\n - DPOAE\n - DP Growth\n - sessions\n"
                  "were created in the [repo_root]/results/"
                  "BIDS_sidecars_originals/ folder.\n")
    else:
        # run json_sidecar_generator.py
        print("The BIDS_sidecars_originals folder is absent: we will "
              "create it for you.\n")
        jsg.create_sidecars(result_path)
        print("\n")
        print("The json sidecars for:\n - tymp\n - reflex\n"
              " - PTA\n - MTX\n - TEOAE\n - DPOAE\n - DP Growth\n"
              " - sessions\nwere created in the [repo_root]/results/"
              "BIDS_sidecars_originals folder.\n")


def retrieve_tests(subject_folder, ses_ID):
    """
    This function lists the test data available in a specified
    session folder.
    INPUTS:
    -subject_folder: path into the subject's folder:
                     [repo_root]/results/BIDS_data/sub-[XX]/
    -ses_ID: name of the session folder to explore
    OUTPUTS:
    -returns a list of the tests represented by the data in the
     session folder
    """

    ls_test = []

    path = os.path.join(subject_folder, ses_ID)
    ls_files = os.listdir(path)

    i = 0
    while i < len(ls_files):
        if ls_files[i].endswith(".tsv"):
            pass
        else:
            ls_files.pop(i)
            i -= 1
        i += 1

    for j in ls_files:
        if j.find("Tymp") != -1:
            ls_test.append("Tymp")

        elif j.find("Reflex") != -1:
            ls_test.append("Reflex")

        elif j.find("PTA") != -1:
            ls_test.append("PTA")

        elif j.find("MTX") != -1:
            ls_test.append("MTX")

        elif j.find("TEOAE") != -1:
            ls_test.append("TEOAE")

        elif j.find("DPOAE") != -1:
            ls_test.append("DPOAE")

        elif j.find("DPGrowth") != -1:
            filepath = os.path.join(path, j)
            df = pd.read_csv(filepath, sep="\t")
            value = df.at[0, "freq2"]

            if value == 2002:
                ls_test.append("Growth_2")
            elif value == 4004:
                ls_test.append("Growth_4")
            elif value == 6006:
                ls_test.append("Growth_6")

    return ls_test


# Single test sub-df extraction from each participant's sub-df
def eliminate_columns(sub_df, columns_conditions, test_columns):
    """
    This function removes the columns that are not required for a
    specific test.
    INPUTS:
    -sub_df: df containing only the lines linked to a single subject
    -columns_conditions: list of column names used for multiple tests
    -test_columns: list of column names specific to a test
    OUTPUTS:
    -returns a sub-df without the useless columns
    """

    to_keep = columns_conditions + test_columns
    df_test = sub_df[to_keep]

    return df_test


def save_df(data_tosave_df, single_test_df, index,
            test, result_path, run="01"):
    """
    This function is used to save the tsv files and json sidecars.
    INPUTS:
    -data_tosave_df: df to be saved in the tsv file
    -single_test_df: df containing the test columns for a single
                     participant
    -index: the line index (in single_test_df) linked with the data to save
            (data_tosave_df)
    -test: the selected test marker
    -result_path: path to results ([repo_root]/results/)
    -run: run indexer value (Default = 01)
    OUTPUTS:
    -saved tsv file
    -NO specific return to the script
    """

    # Folder where to put each participants' folder
    parent_path = os.path.join(result_path, "BIDS_data")

    sub = single_test_df['Participant_ID'][index]

    ses = single_test_df["Session_ID"][index]

    # The next variable ("ext") can take the value ".csv".
    # The last code section of BIDS_formater.py must then be activated
    ext = '.tsv'

    path = os.path.join(parent_path, sub, 'ses-' + ses)
    file_name = (sub + '_ses-' + ses + '_task-'
                 + test + '_run-' + run + "_beh")

    data_tosave_df.to_csv(os.path.join(path, file_name + ext), sep='\t')

#    json_origin = os.path.join(result_path, "BIDS_sidecars_originals")

#    if test == "Tymp":
#        copyfile(os.path.join(json_origin, "tymp_run_level.json"),
#                 os.path.join(path, file_name + ".json"))
#    elif test == "Reflex":
#        copyfile(os.path.join(json_origin, "reflex_run_level.json"),
#                 os.path.join(path, file_name + ".json"))
#    elif test == "PTA":
#        copyfile(os.path.join(json_origin, "pta_run_level.json"),
#                 os.path.join(path, file_name + ".json"))
#    elif test == "MTX":
#        copyfile(os.path.join(json_origin, "mtx_run_level.json"),
#                 os.path.join(path, file_name + ".json"))
#    elif test == "TEOAE":
#        copyfile(os.path.join(json_origin, "teoae_run_level.json"),
#                 os.path.join(path, file_name + ".json"))
#    elif test == "DPOAE":
#        copyfile(os.path.join(json_origin, "dpoae_run_level.json"),
#                 os.path.join(path, file_name + ".json"))
#    elif test == "DPGrowth":
#        copyfile(os.path.join(json_origin, "dpgrowth_run_level.json"),
#                 os.path.join(path, file_name + ".json"))


def extract_tymp(single_test_df, ls_columns_1,
                 ls_columns_2, x, path):
    """
    This function extracts every single tympanometry test and send the results
    to be saved by the save_df function.
    INPUTS:
    -single_test_df: df containing only the lines containing tympanometry tests
                     and from which the useless columns have been removed
    -ls_columns_1: list of right ear test data column names
    -ls_columns_2: list of left ear test data column names
    -x: list of column names to use in the reconstructed, BIDS formated df
    -path: path inside the results folder ([repo_root]/results/)
    OUTPUTS:
    -NO specific return to the script
    -activates the save_df function
    """

    for j in range(0, len(single_test_df)):
        y = [[], []]

        y[0].append("1")
        y[0].append("R")

        for k in ls_columns_1:
            y[0].append(single_test_df[k][j])

        y[1].append("2")
        y[1].append("L")

        for m in ls_columns_2:
            y[1].append(single_test_df[m][j])

        mask_0 = []
        mask_1 = []

        for n in range(2, len(y[0])):
            if y[0][n] == 'n/a':
                mask_0.append(True)
            else:
                mask_0.append(False)

        for p in range(2, len(y[1])):
            if y[1][p] == 'n/a':
                mask_1.append(True)
            else:
                mask_1.append(False)

        if False in mask_1:
            pass
        else:
            del y[1]

        if False in mask_0:
            pass
        else:
            del y[0]

        if len(y) > 0:
            z = pd.DataFrame(data=y, columns=x).set_index("order")
            save_df(z, single_test_df, j, 'Tymp', path)
        else:
            continue


def extract_reflex(single_test_df, ls_columns_1,
                   ls_columns_2, x, path):
    """
    This function extracts every single stapedial reflex test and send the
    results to be saved by the save_df function.
    INPUTS:
    -single_test_df: df containing only the lines containing reflex tests and
                     from which the useless columns have been removed
    -ls_columns_1: list of right ear test data column names
    -ls_columns_2: list of left ear test data column names
    -x: list of column names to use in the reconstructed, BIDS formated df
    -path: path inside the results folder ([repo_root]/results/)
    OUTPUTS:
    -NO specific return to the script
    -activates the save_df function
    """

    for j in range(0, len(single_test_df)):
        y = [[], []]

        y[0].append("1")
        y[0].append("R")

        for k in ls_columns_1:
            y[0].append(single_test_df[k][j])

        y[1].append("2")
        y[1].append("L")

        for m in ls_columns_2:
            y[1].append(single_test_df[m][j])

        mask_0 = []
        mask_1 = []

        for n in range(2, len(y[0])):
            if y[0][n] == 'n/a':
                mask_0.append(True)
            else:
                mask_0.append(False)

        for p in range(2, len(y[1])):
            if y[1][p] == 'n/a':
                mask_1.append(True)
            else:
                mask_1.append(False)

        if False in mask_1:
            pass
        else:
            del y[1]

        if False in mask_0:
            pass
        else:
            del y[0]

        if len(y) > 0:
            z = pd.DataFrame(data=y, columns=x).set_index("order")
            save_df(z, single_test_df, j, 'Reflex', path)
        else:
            continue


def extract_pta(single_test_df, ls_columns_1,
                ls_columns_2, x, path):
    """
    This function extracts every single pure-tone audiometry test and send the
    results to be saved by the save_df function.
    INPUTS:
    -single_test_df: df containing only the lines containing PTA tests and from
                     which the useless columns have been removed
    -ls_columns_1: list of right ear test data column names
    -ls_columns_2: list of left ear test data column names
    -x: list of column names to use in the reconstructed, BIDS formated df
    -path: path inside the results folder ([repo_root]/results/)
    OUTPUTS:
    -NO specific return to the script
    -activates the save_df function
    """

    for j in range(0, len(single_test_df)):
        y = [[], []]

        y[0].append("1")
        y[0].append("R")

        for k in ls_columns_1:
            y[0].append(single_test_df[k][j])

        y[1].append("2")
        y[1].append("L")

        for m in ls_columns_2:
            y[1].append(single_test_df[m][j])

        mask_0 = []
        mask_1 = []

        for n in range(2, len(y[0])):
            if y[0][n] == 'n/a':
                mask_0.append(True)
            else:
                mask_0.append(False)

        for p in range(2, len(y[1])):
            if y[1][p] == 'n/a':
                mask_1.append(True)
            else:
                mask_1.append(False)

        if False in mask_1:
            pass
        else:
            del y[1]

        if False in mask_0:
            pass
        else:
            del y[0]

        if len(y) > 0:
            z = pd.DataFrame(data=y, columns=x).set_index("order")
            save_df(z, single_test_df, j, 'PTA', path)
        else:
            continue


def extract_mtx(single_test_df, ls_columns_1,
                ls_columns_2, x, path):
    """
    This function extracts every single matrix speech-in-noise perception test
    and send the results to be saved by the save_df function.
    INPUTS:
    -single_test_df: df containing only the lines containing MTX tests and from
                     which the useless columns have been removed
    -ls_columns_1: list of right ear test data column names
    -ls_columns_2: list of left ear test data column names
    -x: list of column names to use in the reconstructed, BIDS formated df
    -path: path inside the results folder ([repo_root]/results/)
    OUTPUTS:
    -NO specific return to the script
    -activates the save_df function
    """

    for j in range(0, len(single_test_df)):
        y = [[], []]

        y[0].append("1")

        for k in ls_columns_1:
            value_1 = str(single_test_df[k][j].replace(",", "."))
            try:
                float(value_1)
            except ValueError:
                y[0].append(single_test_df[k][j])
            else:
                y[0].append(float(value_1))

        y[1].append("2")

        for m in ls_columns_2:
            value_2 = str(single_test_df[m][j].replace(",", "."))
            try:
                float(value_2)
            except ValueError:
                y[1].append(single_test_df[m][j])
            else:
                y[1].append(float(value_2))

        mask_0 = []
        mask_1 = []

        for n in range(2, len(y[0])):
            if y[0][n] == 'n/a':
                mask_0.append(True)
            else:
                mask_0.append(False)

        for p in range(2, len(y[1])):
            if y[1][p] == 'n/a':
                mask_1.append(True)
            else:
                mask_1.append(False)

        if False in mask_1:
            pass
        else:
            del y[1]

        if False in mask_0:
            pass
        else:
            del y[0]

        if len(y) > 0:
            z = pd.DataFrame(data=y, columns=x).set_index("order")
            save_df(z, single_test_df, j, 'MTX', path)
        else:
            continue


def extract_teoae(data_sub, data_oae_sub, oae_file_list,
                  x_teoae, data_path, result_path):
    """
    This function extracts every single transient-evoked otoacoustic emissions
    test and send the results to be saved by the save_df function.
    INPUTS:
    -data_sub: df containing the subject-specific session informations (from
               the db spreadsheet)
    -data_oae_sub: df containing the subject-specific available test data files
                   breakdown informations
    -oae_file_list: list of all the available OAE test filenames
    -x_teoae: list of column names to use in the reconstructed, BIDS formated
              df
    -data_path: path inside the auditory_tests data folder
                ([repo_root]/data/auditory_tests/)
    -result_path: path inside the results folder ([repo_root]/results/)
    OUTPUTS:
    -NO specific return to the script
    -activates the save_df function
    """

    data_path = os.path.join(data_path, "OAE")

    no_oae = ["Condition 1A (right before the scan)",
              "Condition 1B (right after the scan)",
              "Supplementary PTA test (Baseline)",
              "Suppl. PTA test (right before the scan)",
              "Suppl. PTA test (right after the scan)"]

    post = "Condition 3B (OAEs right after the scan)"

    for j in range(0, len(data_sub)):
        subject = data_sub["Participant_ID"][j]
        date = data_sub["Date"][j]
        condition = data_sub["Protocol condition"][j]

        if condition in no_oae:
            continue

        else:
            teoae_R_file = None
            teoae_L_file = None

            if data_sub.iloc[j]["Protocol condition"] == post:

                for k in range(0, len(oae_file_list)):
                    if (oae_file_list[k].startswith(subject)
                            and oae_file_list[k].find(date) != -1
                            and oae_file_list[k].find("PostScan") != -1):

                        if oae_file_list[k].endswith("TE_R.csv"):
                            teoae_R_file = oae_file_list[k]

                        elif oae_file_list[k].endswith("TE_L.csv"):
                            teoae_L_file = oae_file_list[k]

                        else:
                            pass

                    else:
                        pass

            else:
                for m in range(0, len(oae_file_list)):
                    if oae_file_list[m].find("PostScan") != -1:
                        continue

                    elif (oae_file_list[m].startswith(subject) and
                          oae_file_list[m].find(date) != -1):

                        if oae_file_list[m].endswith("TE_R.csv"):
                            teoae_R_file = oae_file_list[m]

                        elif oae_file_list[m].endswith("TE_L.csv"):
                            teoae_L_file = oae_file_list[m]

                        else:
                            pass

                    else:
                        pass

        if (teoae_R_file is None or teoae_L_file is None):
            print(color.Fore.RED
                  + (f"ERROR: At least one of {subject}'s DP-growth csv "
                     f"files for the {date} session ({condition}) "
                     f"is missing.\n"))
            continue

        else:
            df_L = pd.read_csv(os.path.join(data_path, teoae_L_file),
                               sep=";")
            df_R = pd.read_csv(os.path.join(data_path, teoae_R_file),
                               sep=";")

            for a in df_L.columns.tolist():
                for b in range(0, len(df_L)):
                    value_L = str(df_L.iloc[b][a]).replace(",", ".")
                    df_L.at[b, a] = float(value_L)

            for c in df_R.columns.tolist():
                for d in range(0, len(df_R)):
                    value_R = str(df_R.iloc[d][c]).replace(",", ".")
                    df_R.at[d, c] = float(value_R)

            order_R = []
            order_L = []
            side_R = []
            side_L = []
            snr_R = []
            snr_L = []

            for q in range(0, len(df_R)):
                order_R.append(1)
                side_R.append("R")
                snr_R.append(df_R["OAE (dB)"][q] - df_R["Noise (dB)"][q])

            for r in range(0, len(df_L)):
                order_L.append(2)
                side_L.append("L")
                snr_L.append(df_L["OAE (dB)"][r] - df_L["Noise (dB)"][r])

            df_R["order"] = order_R
            df_R["side"] = side_R
            df_R["snr"] = snr_R
            df_L["order"] = order_L
            df_L["side"] = side_L
            df_L["snr"] = snr_L

            df_teoae = pd.concat([df_R, df_L])
            df_teoae.reset_index(inplace=True, drop=True)

            ls_columns = df_teoae.columns.tolist()

            if any("Unnamed" in n for n in ls_columns):
                column_to_drop = [p for p in ls_columns if "Unnamed" in p]
                df_teoae.drop(labels=column_to_drop.pop(),
                              axis=1, inplace=True)
            else:
                pass

            df_teoae = df_teoae[["order", "side", "Freq (Hz)",
                                 "OAE (dB)", "Noise (dB)", "snr",
                                 "Confidence (%)"]]

            df_teoae = df_teoae.set_axis(x_teoae, axis=1, copy=False)
            df_teoae.set_index("order", inplace=True)

            save_df(df_teoae, data_sub, j, 'TEOAE', result_path)


def extract_dpoae(data_sub, data_oae_sub, oae_file_list,
                  x_dpoae, data_path, result_path):
    """
    This function extracts every single distortion product otoacoustic
    emissions test and send the results to be saved by the save_df function.
    INPUTS:
    -data_sub: df containing the subject-specific session informations (from
               the db spreadsheet)
    -data_oae_sub: df containing the subject-specific available test data files
                   breakdown informations
    -oae_file_list: list of all the available OAE test filenames
    -x_dpoae: list of column names to use in the reconstructed, BIDS formated
              df
    -data_path: path inside the auditory_tests data folder
                ([repo_root]/data/auditory_tests/)
    -result_path: path inside the results folder ([repo_root]/results/)
    OUTPUTS:
    -NO specific return to the script
    -activates the save_df function
    """

    data_path = os.path.join(data_path, "OAE")

    no_oae = ["Condition 1A (right before the scan)",
              "Condition 1B (right after the scan)",
              "Supplementary PTA test (Baseline)",
              "Suppl. PTA test (right before the scan)",
              "Suppl. PTA test (right after the scan)"]

    post = "Condition 3B (OAEs right after the scan)"

    for j in range(0, len(data_sub)):
        subject = data_sub["Participant_ID"][j]
        date = data_sub["Date"][j]
        condition = data_sub["Protocol condition"][j]

        if condition in no_oae:
            continue

        else:
            dpoae_R_file = None
            dpoae_L_file = None

            if data_sub.iloc[j]["Protocol condition"] == post:

                for k in range(0, len(oae_file_list)):
                    if (oae_file_list[k].startswith(subject)
                            and oae_file_list[k].find(date) != -1
                            and oae_file_list[k].find("PostScan") != -1):

                        if oae_file_list[k].endswith("DPOAE6555_R.csv"):
                            dpoae_R_file = oae_file_list[k]

                        elif oae_file_list[k].endswith("DPOAE6555_L.csv"):
                            dpoae_L_file = oae_file_list[k]

                        else:
                            pass

                    else:
                        pass

            else:
                for m in range(0, len(oae_file_list)):
                    if oae_file_list[m].find("PostScan") != -1:
                        continue

                    elif (oae_file_list[m].startswith(subject) and
                          oae_file_list[m].find(date) != -1):

                        if oae_file_list[m].endswith("DPOAE6555_R.csv"):
                            dpoae_R_file = oae_file_list[m]

                        elif oae_file_list[m].endswith("DPOAE6555_L.csv"):
                            dpoae_L_file = oae_file_list[m]

                        else:
                            pass

                    else:
                        pass

        if (dpoae_R_file is None or dpoae_L_file is None):
            print(color.Fore.RED
                  + (f"ERROR: At least one of {subject}'s DPOAE csv "
                     f"files for the {date} session ({condition}) "
                     f"is missing.\n"))
            continue

        else:
            df_L = pd.read_csv(os.path.join(data_path, dpoae_L_file),
                               sep=";")
            df_R = pd.read_csv(os.path.join(data_path, dpoae_R_file),
                               sep=";")

            for a in df_L.columns.tolist():
                for b in range(0, len(df_L)):
                    if str(df_L.iloc[b][a]).endswith(" *"):
                        value_L = str(df_L.iloc[b][a].rstrip(" *"))
                        value_L = value_L.replace(",", ".")
                        df_L.at[b, a] = value_L + " *"
                    elif str(df_L.iloc[b][a]) == "-":
                        df_L.at[b, a] = "n/a"
                    else:
                        value_L = str(df_L.iloc[b][a]).replace(",", ".")
                        df_L.at[b, a] = float(value_L)

            for c in df_R.columns.tolist():
                for d in range(0, len(df_R)):
                    if str(df_R.iloc[d][c]).endswith(" *"):
                        value_R = str(df_R.iloc[d][c].rstrip(" *"))
                        value_R = value_R.replace(",", ".")
                        df_R.at[d, c] = value_R + " *"
                    elif str(df_R.iloc[d][c]) == "-":
                        df_R.at[d, c] = "n/a"
                    else:
                        value_R = str(df_R.iloc[d][c]).replace(",", ".")
                        df_R.at[d, c] = float(value_R)

            order_R = []
            order_L = []
            side_R = []
            side_L = []
            freq1_R = []
            freq1_L = []
            snr_R = []
            snr_L = []

            for q in range(0, len(df_R)):
                order_R.append(1)
                side_R.append("R")
                freq1_R.append(df_R["Freq (Hz)"][q] / 1.22)

                snr_R.append(df_R["DP (dB)"][q]
                             - df_R["Noise+2sd (dB)"][q])

            for r in range(0, len(df_L)):
                order_L.append(2)
                side_L.append("L")
                freq1_L.append(df_L["Freq (Hz)"][r] / 1.22)
                snr_L.append(df_L["DP (dB)"][r]
                             - df_L["Noise+2sd (dB)"][r])

            df_R["order"] = order_R
            df_R["side"] = side_R
            df_R["freq1"] = freq1_R
            df_R["snr"] = snr_R
            df_L["order"] = order_L
            df_L["side"] = side_L
            df_L["freq1"] = freq1_L
            df_L["snr"] = snr_L

            df_dpoae = pd.concat([df_R, df_L])
            df_dpoae.reset_index(inplace=True, drop=True)

            ls_columns = df_dpoae.columns.tolist()

            if any("Unnamed" in n for n in ls_columns):
                column_to_drop = [p for p in ls_columns if "Unnamed" in p]
                df_dpoae.drop(labels=column_to_drop.pop(),
                              axis=1, inplace=True)
            else:
                pass

            df_dpoae = df_dpoae[["order", "side", "freq1", "Freq (Hz)",
                                 "F1 (dB)", "F2 (dB)", "DP (dB)", "snr",
                                 "Noise+2sd (dB)", "Noise+1sd (dB)",
                                 "2F2-F1 (dB)", "3F1-2F2 (dB)",
                                 "3F2-2F1 (dB)", "4F1-3F2 (dB)"]]

            df_dpoae = df_dpoae.set_axis(x_dpoae, axis=1, copy=False)
            df_dpoae.set_index("order", inplace=True)

            save_df(df_dpoae, data_sub, j, 'DPOAE', result_path)


def growth_prepost(data_sub, i, oae_file_list,
                   x_growth, data_path, result_path):
    """
    This function extracts the conditions 3A (pre-scan) and 3B (post-scan)
    distortion product otoacoustic emissions' growth function tests and send
    the results to be saved by the save_df function.
    INPUTS:
    -data_sub: df containing the subject-specific session informations (from
               the db spreadsheet)
    -i: index of the line to use in data_sub
    -oae_file_list: list of all the available OAE test filenames
    -x_growth: list of column names to use in the reconstructed, BIDS formated
               df
    -data_path: path inside the OAE test data folder
                ([repo_root]/data/auditory_tests/OAE/)
    -result_path: path inside the results folder ([repo_root]/results/)
    OUTPUTS:
    -NO specific return to the script
    -activates the save_df function
    """

    subject = data_sub["Participant_ID"][i]
    date = data_sub["Date"][i]
    condition = data_sub["Protocol condition"][i]

    if condition.find("Condition 3A") != -1:
        prepost = "PreScan"
    elif condition.find("Condition 3B") != -1:
        prepost = "PostScan"

    g2k_R_file = None
    g4k_R_file = None
    g6k_R_file = None
    g2k_L_file = None
    g4k_L_file = None
    g6k_L_file = None

    for n in range(0, len(oae_file_list)):

        if oae_file_list[n].find(prepost) == -1:
            continue

        elif (oae_file_list[n].startswith(subject) and
              oae_file_list[n].find(date) != -1 and
              oae_file_list[n].find(prepost) != -1):

            if oae_file_list[n].endswith("R.csv"):

                if oae_file_list[n].find("2000") != -1:
                    g2k_R_file = oae_file_list[n]

                elif oae_file_list[n].find("4000") != -1:
                    g4k_R_file = oae_file_list[n]

                elif oae_file_list[n].find("6000") != -1:
                    g6k_R_file = oae_file_list[n]

                else:
                    pass

            elif oae_file_list[n].endswith("L.csv"):

                if oae_file_list[n].find("2000") != -1:
                    g2k_L_file = oae_file_list[n]

                elif oae_file_list[n].find("4000") != -1:
                    g4k_L_file = oae_file_list[n]

                elif oae_file_list[n].find("6000") != -1:
                    g6k_L_file = oae_file_list[n]

                else:
                    pass

            else:
                pass

        else:
            pass

    if (g2k_R_file is None or g4k_R_file is None
            or g6k_R_file is None or g2k_L_file is None
            or g4k_L_file is None or g6k_L_file is None):
        print(color.Fore.RED
              + (f"ERROR: At least one of {subject}'s DP-growth csv files "
                 f"for the {date} session ({condition}) is missing.\n"))
        pass

    else:
        df_2k_L = pd.read_csv(os.path.join(data_path, g2k_L_file),
                              sep=";")
        df_4k_L = pd.read_csv(os.path.join(data_path, g4k_L_file),
                              sep=";")
        df_6k_L = pd.read_csv(os.path.join(data_path, g6k_L_file),
                              sep=";")
        df_2k_R = pd.read_csv(os.path.join(data_path, g2k_R_file),
                              sep=";")
        df_4k_R = pd.read_csv(os.path.join(data_path, g4k_R_file),
                              sep=";")
        df_6k_R = pd.read_csv(os.path.join(data_path, g6k_R_file),
                              sep=";")

        ls_1df = [df_2k_L, df_4k_L, df_6k_L,
                  df_2k_R, df_4k_R, df_6k_R]
        ls_2df = [[df_2k_L, df_2k_R],
                  [df_4k_L, df_4k_R],
                  [df_6k_L, df_6k_R]]

        for a in ls_1df:
            for b in a.columns.tolist():
                for c in range(0, len(a)):
                    value_L = str(a.iloc[c][b]).replace(",", ".")
                    a.at[c, b] = float(value_L)

        for d in range(0, len(ls_2df)):

            order_R = []
            order_L = []
            side_R = []
            side_L = []
            freq1_R = []
            freq1_L = []
            snr_R = []
            snr_L = []

            for q in range(0, len(ls_2df[d][1])):
                order_R.append(1)
                side_R.append("R")
                freq1_R.append(ls_2df[d][1]["Freq (Hz)"][q] / 1.22)
                snr_R.append(ls_2df[d][1]["DP (dB)"][q]
                             - ls_2df[d][1]["Noise+2sd (dB)"][q])

            for r in range(0, len(ls_2df[d][0])):
                order_L.append(2)
                side_L.append("L")
                freq1_L.append(ls_2df[d][0]["Freq (Hz)"][r] / 1.22)
                snr_L.append(ls_2df[d][0]["DP (dB)"][r]
                             - ls_2df[d][0]["Noise+2sd (dB)"][r])

            ls_2df[d][1]["order"] = order_R
            ls_2df[d][1]["side"] = side_R
            ls_2df[d][1]["freq1"] = freq1_R
            ls_2df[d][1]["snr"] = snr_R
            ls_2df[d][0]["order"] = order_L
            ls_2df[d][0]["side"] = side_L
            ls_2df[d][0]["freq1"] = freq1_L
            ls_2df[d][0]["snr"] = snr_L

            df_growth = pd.concat([ls_2df[d][1], ls_2df[d][0]])
            df_growth.reset_index(inplace=True, drop=True)

            ls_columns = df_growth.columns.tolist()

            if any("Unnamed" in n for n in ls_columns):
                column_to_drop = [p for p in ls_columns if "Unnamed" in p]
                df_growth.drop(labels=column_to_drop.pop(),
                               axis=1, inplace=True)
            else:
                pass

            df_growth = df_growth[["order", "side", "freq1", "Freq (Hz)",
                                   "F1 (dB)", "F2 (dB)", "DP (dB)", "snr",
                                   "Noise+2sd (dB)", "Noise+1sd (dB)",
                                   "2F2-F1 (dB)", "3F1-2F2 (dB)",
                                   "3F2-2F1 (dB)", "4F1-3F2 (dB)"]]

            df_growth = df_growth.set_axis(x_growth, axis=1, copy=False)
            df_growth.set_index("order", inplace=True)

            if d == 0:
                run = "01"
            elif d == 1:
                run = "02"
            elif d == 2:
                run = "03"
            else:
                print("ERROR: counter value out of bound")

            save_df(df_growth, data_sub, i,
                    'DPGrowth', result_path, run=run)


def growth_others(data_sub, i, oae_file_list,
                  x_growth, data_path, result_path):
    """
    This function extracts the baseline and condition 2 sessions' distortion
    product otoacoustic emissions' growth function tests and send the results
    to be saved by the save_df function.
    INPUTS:
    -data_sub: df containing the subject-specific session informations (from
               the db spreadsheet)
    -i: index of the line to use in data_sub
    -oae_file_list: list of all the available OAE test filenames
    -x_growth: list of column names to use in the reconstructed, BIDS formated
               df
    -data_path: path inside the OAE test data folder
                ([repo_root]/data/auditory_tests/OAE/)
    -result_path: path inside the results folder ([repo_root]/results/)
    OUTPUTS:
    -NO specific return to the script
    -activates the save_df function
    """

    subject = data_sub["Participant_ID"][i]
    date = data_sub["Date"][i]
    condition = data_sub["Protocol condition"][i]

    growth_R_file = None
    growth_L_file = None

    for m in range(0, len(oae_file_list)):
        if oae_file_list[m].find("PostScan") != -1:
            pass

        elif (oae_file_list[m].startswith(subject) and
              oae_file_list[m].find(date) != -1):

            if oae_file_list[m].endswith("4000_R.csv"):
                growth_R_file = oae_file_list[m]

            elif oae_file_list[m].endswith("4000_L.csv"):
                growth_L_file = oae_file_list[m]

            else:
                pass

        else:
            pass

    if (growth_R_file is None or growth_L_file is None):
        print(color.Fore.RED
              + (f"ERROR: At least one of {subject}'s DP-growth csv files "
                 f"for the {date} session ({condition}) is missing.\n"))
        pass

    else:
        df_L = pd.read_csv(os.path.join(data_path, growth_L_file),
                           sep=";")
        df_R = pd.read_csv(os.path.join(data_path, growth_R_file),
                           sep=";")

        for a in df_L.columns.tolist():
            for b in range(0, len(df_L)):
                value_L = str(df_L.iloc[b][a]).replace(",", ".")
                df_L.at[b, a] = float(value_L)

        for c in df_R.columns.tolist():
            for d in range(0, len(df_R)):
                value_R = str(df_R.iloc[d][c]).replace(",", ".")
                df_R.at[d, c] = float(value_R)

        order_R = []
        order_L = []
        side_R = []
        side_L = []
        freq1_R = []
        freq1_L = []
        snr_R = []
        snr_L = []

        for q in range(0, len(df_R)):
            order_R.append(1)
            side_R.append("R")
            freq1_R.append(df_R["Freq (Hz)"][q] / 1.22)
            snr_R.append(df_R["DP (dB)"][q]
                         - df_R["Noise+2sd (dB)"][q])

        for r in range(0, len(df_L)):
            order_L.append(2)
            side_L.append("L")
            freq1_L.append(df_L["Freq (Hz)"][r] / 1.22)
            snr_L.append(df_L["DP (dB)"][r]
                         - df_L["Noise+2sd (dB)"][r])

        df_R["order"] = order_R
        df_R["side"] = side_R
        df_R["freq1"] = freq1_R
        df_R["snr"] = snr_R
        df_L["order"] = order_L
        df_L["side"] = side_L
        df_L["freq1"] = freq1_L
        df_L["snr"] = snr_L

        df_growth = pd.concat([df_R, df_L])
        df_growth.reset_index(inplace=True, drop=True)

        ls_columns = df_growth.columns.tolist()

        if any("Unnamed" in n for n in ls_columns):
            column_to_drop = [p for p in ls_columns if "Unnamed" in p]
            df_growth.drop(labels=column_to_drop.pop(),
                           axis=1, inplace=True)
        else:
            pass

        df_growth = df_growth[["order", "side", "freq1", "Freq (Hz)",
                               "F1 (dB)", "F2 (dB)", "DP (dB)", "snr",
                               "Noise+2sd (dB)", "Noise+1sd (dB)",
                               "2F2-F1 (dB)", "3F1-2F2 (dB)",
                               "3F2-2F1 (dB)", "4F1-3F2 (dB)"]]

        df_growth = df_growth.set_axis(x_growth, axis=1, copy=False)
        df_growth.set_index("order", inplace=True)

        save_df(df_growth, data_sub, i, 'DPGrowth', result_path)


def extract_growth(data_sub, data_oae_sub, oae_file_list,
                   x_growth, data_path, result_path):
    """
    This function extracts every DP growth function OAE test and separate them
    according to the experimental condition in which they were acquired.
    It then calls the proper function for processing.
    INPUTS:
    -data_sub: df containing the subject-specific session informations (from
               the db spreadsheet)
    -data_oae_sub: df containing the subject-specific available test data files
                   breakdown informations
    -oae_file_list: list of all the available OAE test filenames
    -x_growth: list of column names to use in the reconstructed, BIDS formated
               df
    -data_path: path inside the auditory_tests data folder
                ([repo_root]/data/auditory_tests/)
    -result_path: path inside the results folder ([repo_root]/results/)
    OUTPUTS:
    -NO specific return to the script
    -activates the growth_prepost and growth_others functions
    """

    data_path = os.path.join(data_path, "OAE")

    no_oae = ["Condition 1A (right before the scan)",
              "Condition 1B (right after the scan)",
              "Supplementary PTA test (Baseline)",
              "Suppl. PTA test (right before the scan)",
              "Suppl. PTA test (right after the scan)"]

    just_4k = ["Baseline", "Condition 2 (2-7 days post-scan)"]

    prepost = ["Condition 3A (OAEs right before the scan)",
               "Condition 3B (OAEs right after the scan)"]

    for j in range(0, len(data_sub)):
        condition = data_sub["Protocol condition"][j]

        if condition in no_oae:
            continue

        elif condition in just_4k:
            growth_others(data_sub, j, oae_file_list,
                          x_growth, data_path, result_path)

        elif condition in prepost:
            growth_prepost(data_sub, j, oae_file_list,
                           x_growth, data_path, result_path)


if __name__ == "__main__":
    print(color.Fore.RED
          + ("ERROR: This script is not designed to be used as a standalone "
             "script.\nPlease use main.py functionalities or "
             "BIDS_formater.py to call it."))

else:
    pass
