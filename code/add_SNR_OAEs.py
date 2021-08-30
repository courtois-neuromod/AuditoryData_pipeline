import pandas as pd
# import numpy as np
import os

path_origine = "../../OAEs/"
path_results = "../results/OAEs/"
subjects = ["sub-01", "sub-02", "sub-03", "sub-04", "sub-05", "sub-06"]

def extract_csv(ls_of_files):
    csv = []

    for j in range(0, len(ls_of_files)):
        if ls_of_files[j].endswith(".csv") is True:
            csv.append(ls_of_files[j])
        else:
            continue

    # print(csv)
    # print(len(csv))
    return csv


def SNR_TE(df):
    ls_columns = df.columns

    for m in ls_columns:
        for n in range(0, len(df)):
            a = df[m][n]
            a = str(a)
            # print(a)
            if a.count(",") > 0:
                a = a.replace(",", ".")
            else:
                pass
            df.at[n, m] = float(a)

    # print(df)
    df["SNR (dB)"] = df["OAE (dB)"].subtract(df["Noise (dB)"])
    # print(df)

    df = df[["Freq (Hz)",
             "OAE (dB)",
             "Noise (dB)",
             "SNR (dB)",
             "Confidence (%)"]]
    # print(df)

    return df


"""
def SNR_DPOAE(df):
    ls_columns = df.columns

    for m in ls_columns:
        for n in range(0, len(df)):
            a = df[m][n]
            try:
                str(a)
            except ValueError:
                print(a)
                df[m][n] = "NaN"
            else:
                a = str(a)
                print(type(a))
                if a.endswith(" *") == True:
                    print(a)
                    a = a.rstrip(" *")
                    print(a)
                else:
                    pass
                if a.count(",") > 0:
                    a = a.replace(",", ".")
                else:
                    pass
                df.at[n, m] = float(a)

    #df["SNR (dB)"] = df["OAE (dB)"].subtract(df["Noise (dB)"])
    print(df)

    #df = df[["Freq (Hz)",
              "OAE (dB)",
              "Noise (dB)",
              "SNR (dB)",
              "Confidence (%)"]]
    #print(df)

    return df"""


def SNR_DPGrowth(df):
    ls_columns = df.columns
    # print(ls_columns)
    for m in ls_columns:
        for n in range(0, len(df)):
            a = df[m][n]
            a = str(a)
            # print(a)
            if a.count(",") > 0:
                # print("True")
                a = a.replace(",", ".")
            else:
                # print("False")
                pass
            # print(a)
            df.at[n, m] = float(a)

    # print(df)
    df["SNR (dB)"] = df["DP (dB)"].subtract(df["Noise+2sd (dB)"])
    # print(df)

    df = df[["Freq (Hz)", "F1 (dB)",
             "F2 (dB)", "DP (dB)",
             "Noise+2sd (dB)", "SNR (dB)",
             "Noise+1sd (dB)", "2F2-F1 (dB)",
             "3F1-2F2 (dB)", "3F2-2F1 (dB)",
             "4F1-3F2 (dB)"]]
    # print(df)

    return df


def manip_csv(loop_index, location, ls_csv):
    path = location + "/" + ls_csv[loop_index]
    # print(path)
    df = pd.read_csv(path, delimiter=";")
    ls_columns = df.columns
    # print(ls_columns)

    for k in range(0, len(ls_columns)):
        if ls_columns[k].startswith("Unnamed"):
            # var1 = ls_columns[k]
            # print(var1 + " = True")
            # print(df)
            df = df.drop(ls_columns[k], axis=1)
            # print(df)
        else:
            # print(ls_columns[k] + " = False")
            continue
    # print(csv[j])
    # print(df)

    if (ls_csv[loop_index].endswith("TE_L.csv") is True
       or ls_csv[loop_index].endswith("TE_R.csv") is True):
        return(SNR_TE(df))

    elif (ls_csv[loop_index].endswith("DPOAE6655_L.csv") is True
          or ls_csv[loop_index].endswith("DPOAE6655_R.csv") is True):
        print("DPOAE6655: THIS TYPE OF FILE IS NOT SUPPORTED YET.")
        return(pd.DataFrame(["DPOAE6655:",
                             "THIS TYPE OF FILE IS NOT SUPPORTED YET."]))
        # return(SNR_DPOAE(df))

    elif (ls_csv[loop_index].endswith("DPGrowth-2000_L.csv") is True
          or ls_csv[loop_index].endswith("DPGrowth-2000_R.csv") is True
          or ls_csv[loop_index].endswith("DPGrowth-4000_L.csv") is True
          or ls_csv[loop_index].endswith("DPGrowth-4000_R.csv") is True
          or ls_csv[loop_index].endswith("DPGrowth-6000_L.csv") is True
          or ls_csv[loop_index].endswith("DPGrowth-6000_R.csv") is True):
        return(SNR_DPGrowth(df))

    else:
        print("THERE IS AN ERROR IN THIS FILE NAME: "
              + ls_csv[loop_index])


def master_function(subject):
    fetch_location = path_origine + subject
    save_location = path_results + subject
    # print(fetch_location)
    # print(save_location)
    x = os.listdir(fetch_location)
    if os.path.exists(save_location + "/xlsx_SNR_" + subject) is False:
        if os.path.exists(save_location) is False:
            os.mkdir(save_location)
        else:
            pass
        os.mkdir(save_location + "/xlsx_SNR_" + subject)
    else:
        pass
    path_save = save_location + "/xlsx_SNR_" + subject + "/"
    ls_csv = extract_csv(x)
    # print(ls_csv)
    for i in range(0, len(ls_csv)):
        data = manip_csv(i, fetch_location, ls_csv)
        # print(ls_csv[0])
        # data = manip_csv(0, fetch_location, ["test1.csv"])
        # print(ls_csv[0])
        # print(data)
        file_name = ls_csv[i].rstrip(".csv")
        # print(file_name)
        data.to_excel(path_save + file_name + ".xlsx", engine="openpyxl")
        print(ls_csv[i])


for i in subjects:
    master_function(i)
