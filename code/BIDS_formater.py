import pandas as pd
import os
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
parent_path = '../results/BIDS_data/'

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
x_tymp = ['Type', 'TPP', 'ECV', 'SC', 'TW']
x_reflex = [500, 1000, 2000, 4000, 'NOISE']
x_PTA = [250, 500, 1000, 2000, 3000, 4000, 6000, 8000,
         9000, 10000, 11200, 12500, 14000, 16000, 18000, 20000]
x_MTX = ['LANGUAGE', "Practice", "Sp_Bin_No_Bin",
         "Sp_L_No_Bin", "Sp_R_No_Bin", "Sp_L_No_L", "Sp_R_No_R"]


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
        os.mkdir(f"{parent_path}sub-{sub_ID}")


# Check if the session-level folders exist for each participant
# If not, create them
def create_folder_session(subject, session_count):
    sub_ID = subject.lstrip("Sub")
    children_path = f"{parent_path}sub-{sub_ID}/"
    dir_content = os.listdir(children_path)

    for j in range(1, session_count + 1):
        if dir_content.count(f"ses-{j:02d}") == 1:
            pass
        else:
            os.mkdir(f"{children_path}ses-{j:02d}")


# Function used to save the tsv files
# This function is called by the following functions and saves the data they
# provide with the specified path
def save_df(data_tosave_df, single_test_df, index, test, run):
    sub = single_test_df['Participant_ID'][index].lstrip('Sub_')

    if (index + 1) < 10:
        ses = '0' + str(index + 1)
    else:
        ses = str(index + 1)

    # The next variable ("ext") can take the value ".csv".
    # The last code section must then be activated
    ext = '.tsv'

    path = parent_path + 'sub-' + sub + '/' + 'ses-' + ses + '/'
    file_name = ('sub-' + sub + '_ses-' + ses + '_task-' + test + '_run-'
                 + run + ext)

    data_tosave_df.to_csv(path + file_name, sep='\t')


# Extraction of every single tympanometry test
# The results are then sent to the save_df function to be saved
def extract_tymp(single_test_df, ls_columns):
    x = x_tymp

    for j in range(0, len(single_test_df)):
        y = [[]]

        for k in ls_columns:
            y[0].append(single_test_df[k][j])

            if ls_columns == columns_tymp_R:
                run = '01'
            elif ls_columns == columns_tymp_L:
                run = '02'

        mask = []

        for m in range(0, len(y[0])):
            if y[0][m] == 'None':
                mask.append(True)
            else:
                mask.append(False)

        z = pd.DataFrame(data=y, columns=x)

        if False in mask:
            save_df(z, single_test_df, j, 'Tymp', run)
        else:
            continue


# Extraction of every single stapedial reflex test
# The results are then sent to the save_df function to be saved
def extract_reflex(single_test_df, ls_columns):
    x = x_reflex

    for j in range(0, len(single_test_df)):
        y = [[]]

        for k in ls_columns:
            y[0].append(single_test_df[k][j])

            if ls_columns == columns_reflex_R:
                run = '01'
            elif ls_columns == columns_reflex_L:
                run = '02'

        mask = []

        for m in range(0, len(y[0])):
            if y[0][m] == 'None':
                mask.append(True)
            else:
                mask.append(False)

        z = pd.DataFrame(data=y, columns=x)

        if False in mask:
            save_df(z, single_test_df, j, 'Reflex', run)
        else:
            continue


# Extraction of every single pure-tone audiometry test
# The results are then sent to the save_df function to be saved
def extract_pta(single_test_df, ls_columns):
    x = x_PTA

    for j in range(0, len(single_test_df)):
        y = [[]]

        for k in ls_columns:
            y[0].append(single_test_df[k][j])

            if ls_columns == columns_PTA_R:
                run = '01'
            elif ls_columns == columns_PTA_L:
                run = '02'

        mask = []

        for m in range(0, len(y[0])):
            if y[0][m] == 'None':
                mask.append(True)
            else:
                mask.append(False)

        z = pd.DataFrame(data=y, columns=x)

        if False in mask:
            z.replace(to_replace=130, value="None", inplace=True)
            save_df(z, single_test_df, j, 'PTA', run)
        else:
            continue


# Extraction of every single matrix speech-in-noise perception test
# The results are then sent to the save_df function to be saved
def extract_mtx(single_test_df, ls_columns):
    x = x_MTX

    for j in range(0, len(single_test_df)):
        y = [[]]

        for k in ls_columns:
            y[0].append(single_test_df[k][j])

            if ls_columns == columns_MTX_L1:
                run = '01'
            elif ls_columns == columns_MTX_L2:
                run = '02'

        mask = []

        for m in range(0, len(y[0])):
            if y[0][m] == 'None':
                mask.append(True)
            else:
                mask.append(False)

        z = pd.DataFrame(data=y, columns=x)

        if False in mask:
            save_df(z, single_test_df, j, 'MTX', run)
        else:
            continue


for i in subjects:
    create_folder_subjects(i, parent_path)
    data_sub = subject_extractor(df, i)
    create_folder_session(i, len(data_sub))
    tymp = eliminate_columns(data_sub, columns_tymp)
    reflex = eliminate_columns(data_sub, columns_reflex)
    pta = eliminate_columns(data_sub, columns_PTA)
    mtx = eliminate_columns(data_sub, columns_MTX)
    extract_tymp(tymp, columns_tymp_R)
    extract_tymp(tymp, columns_tymp_L)
    extract_reflex(reflex, columns_reflex_R)
    extract_reflex(reflex, columns_reflex_L)
    extract_pta(pta, columns_PTA_R)
    extract_pta(pta, columns_PTA_L)
    extract_mtx(mtx, columns_MTX_L1)
    extract_mtx(mtx, columns_MTX_L2)


# This code section is present if, for any reason, the .tsv files are not
# properly saved. You will first need to activate the "import glob" line
# (line 2). It is then possible to replace the variable "ext"'s value in
# the save_df function with ".csv" and rerun the script with this section
# to rename all the files with the correct ".tsv" file extansion.

# file_list = glob.glob("../results/BIDS_data/sub-*/ses-*/*.csv")

# for path in file_list:
#     new_path = os.path.splitext(path)[0]+".tsv"
#     os.system(f"mv {path} {new_path}")
