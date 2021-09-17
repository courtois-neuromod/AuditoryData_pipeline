import pandas as pd
import os
from shutil import copyfile
# import glob

# Retrieve the database
url_share = "https://docs.google.com/spreadsheets/d/1UQsU6FNr7ovVjLRIMIt"\
            "gtYWr1zN7UHpMjfHtdGa1myc/edit#gid=0"
url_csv = url_share.replace("/edit#gid=", "/export?format=csv&gid=")
df = pd.read_csv(url_csv, sep=',', na_filter=True)

# Manage the empty boxes
df.fillna(value='n/a', inplace=True)

# Create a list of the subjects and a reference path for the results
subjects = ['Sub01', 'Sub02', 'Sub03', 'Sub04', 'Sub05', 'Sub06']
parent_path = os.path.join("..", "results", "BIDS_data")

# Specify the columns to be used for each test
# Subject and session settings data
columns_conditions = ['Participant_ID', 'DATE',
                      'Protocol name', 'Protocol condition',
                      'Scan type']

# Initialize empty lists to be filed with the proper column titles
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

# Generate the column titles to be used in the tsv files
x_tymp = ["order", "side", 'type', 'tpp', 'ecv', 'sc', 'tw']
x_reflex = ["order", "side", "500_hz", "1000_hz", "2000_hz", "4000_hz", 'noise']
x_PTA = ["order", "side", "250_hz", "500_hz", "1000_hz",
         "2000_hz", "3000_hz", "4000_hz", "6000_hz", "8000_hz",
         "9000_hz", "10000_hz", "11200_hz", "12500_hz",
         "14000_hz", "16000_hz", "18000_hz", "20000_hz"]
x_MTX = ["order", "language", "practice", "sp_bin_no_bin",
         "sp_l_no_bin", "sp_r_no_bin", "sp_l_no_l", "sp_r_no_r"]


# Single participant sub-df extraction
def subject_extractor(df, subject_ID):
    mask = df['Participant_ID'] == subject_ID
    sub_df = df[mask].reset_index(drop=True)

    return sub_df


# Single test sub-df extraction from each participant's sub-df
def eliminate_columns(sub_df, test_columns):
    to_keep = columns_conditions + test_columns
    df_test = sub_df[to_keep]

    return df_test


# Check if the subject-level folders exist
# If not, create them
def create_folder_subjects(subject, parent_path):
    dir_content = os.listdir(parent_path)
    dir_content.sort()
    sub_ID = subject.lstrip("Sub")

    if dir_content.count(f"sub-{sub_ID}") == 1:
        pass
    else:
        os.mkdir(os.path.join(parent_path, f"sub-{sub_ID}"))


# Check if the session-level folders exist for each participant
# If not, create them
def create_folder_session(subject, session_count):
    sub_ID = subject.lstrip("Sub")
    children_path = os.path.join(parent_path, f"sub-{sub_ID}")
    dir_content = os.listdir(children_path)

    for j in range(1, session_count + 1):
        if dir_content.count(f"ses-{j:02d}") == 1:
            pass
        else:
            os.mkdir(os.path.join(children_path, f"ses-{j:02d}"))


# Function used to save the tsv files and json sidecars
# This function is called by the following functions and saves the data they
# provide with the specified path
def save_df(data_tosave_df, single_test_df, index, test, run="01"):
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
        copyfile(os.path.join(json_origin, "tymp_run_level.json"), os.path.join(path, file_name + ".json"))
    elif test == "Reflex":
        copyfile(os.path.join(json_origin, "reflex_run_level.json"), os.path.join(path, file_name + ".json"))
    elif test == "PTA":
        copyfile(os.path.join(json_origin, "pta_run_level.json"), os.path.join(path, file_name + ".json"))
    elif test == "MTX":
        copyfile(os.path.join(json_origin, "mtx_run_level.json"), os.path.join(path, file_name + ".json"))


# Extraction of every single tympanometry test
# The results are then sent to the save_df function to be saved
def extract_tymp(single_test_df, ls_columns_1, ls_columns_2):
    x = x_tymp

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

        mask = []

        for n in range(0, len(y)):
            for p in range(2, len(y[n])):
                if y[n][p] == 'n/a':
                    mask.append(True)
                else:
                    mask.append(False)

        z = pd.DataFrame(data=y, columns=x).set_index("order")

        if False in mask:
            save_df(z, single_test_df, j, 'Tymp')
        else:
            continue


# Extraction of every single stapedial reflex test
# The results are then sent to the save_df function to be saved
def extract_reflex(single_test_df, ls_columns_1, ls_columns_2):
    x = x_reflex

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

        mask = []

        for n in range(0, len(y)):
            for p in range(2, len(y[n])):
                if y[n][p] == 'n/a':
                    mask.append(True)
                else:
                    mask.append(False)

        z = pd.DataFrame(data=y, columns=x).set_index("order")

        if False in mask:
            save_df(z, single_test_df, j, 'Reflex')
        else:
            continue


# Extraction of every single pure-tone audiometry test
# The results are then sent to the save_df function to be saved
def extract_pta(single_test_df, ls_columns_1, ls_columns_2):
    x = x_PTA

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

        mask = []

        for n in range(0, len(y)):
            for p in range(2, len(y[n])):
                if y[n][p] == 'n/a':
                    mask.append(True)
                else:
                    mask.append(False)

        z = pd.DataFrame(data=y, columns=x).set_index("order")

        if False in mask:
            z.replace(to_replace=130, value="n/a", inplace=True)
            save_df(z, single_test_df, j, 'PTA')
        else:
            continue


# Extraction of every single matrix speech-in-noise perception test
# The results are then sent to the save_df function to be saved
def extract_mtx(single_test_df, ls_columns_1, ls_columns_2):
    x = x_MTX

    for j in range(0, len(single_test_df)):
        y = [[], []]

        y[0].append("1")

        for k in ls_columns_1:
            y[0].append(single_test_df[k][j])

        y[1].append("2")

        for m in ls_columns_2:
            y[1].append(single_test_df[m][j])

        mask = []

        for n in range(0, len(y)):
            for p in range(1, len(y[n])):
                if y[n][p] == 'n/a':
                    mask.append(True)
                else:
                    mask.append(False)

        z = pd.DataFrame(data=y, columns=x).set_index("order")

        if False in mask:
            save_df(z, single_test_df, j, 'MTX')
        else:
            continue


for i in subjects:
    # Creation of the subject folder
    create_folder_subjects(i, parent_path)

    # Extraction of all the session for the subject
    data_sub = subject_extractor(df, i)

    # Creation of a folder for each session
    create_folder_session(i, len(data_sub))

    # Extraction of the test columns
    tymp = eliminate_columns(data_sub, columns_tymp)
    reflex = eliminate_columns(data_sub, columns_reflex)
    pta = eliminate_columns(data_sub, columns_PTA)
    mtx = eliminate_columns(data_sub, columns_MTX)

    # Dataframe reconstruction
    extract_tymp(tymp, columns_tymp_R, columns_tymp_L)
    extract_reflex(reflex, columns_reflex_R, columns_reflex_L)
    extract_pta(pta, columns_PTA_R, columns_PTA_L)
    extract_mtx(mtx, columns_MTX_L1, columns_MTX_L2)


# This code section is present if, for any reason, the .tsv files are not
# properly saved. You will first need to activate the "import glob" line
# (line 2). It is then possible to replace the variable "ext"'s value in
# the save_df function with ".csv" and rerun the script with this section
# to rename all the files with the correct ".tsv" file extansion.

# file_list = glob.glob("../results/BIDS_data/sub-*/ses-*/*.csv")

# for path in file_list:
#     new_path = os.path.splitext(path)[0]+".tsv"
#     os.system(f"mv {path} {new_path}")
