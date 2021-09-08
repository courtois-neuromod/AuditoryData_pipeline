import pandas as pd
import numpy as np

ls_task = ["Tymp", "Reflex", "PTA",
           "MTX", "TEOAE", "DPOAE",
           "Growth_2000", "Growth_4000", "Growth_6000"]

keys_tymp = ["Type", "TPP", "ECV", "SC", "TW"]
# value unit for "Type" = ""
# other values' unit = "?"

keys_reflex = ["500_Hz", "1000_Hz", "2000_Hz", "4000_Hz", 'NOISE']
# values' unit = "dB" for all

keys_pta = ["250_Hz", "500_Hz", "1000_Hz", "2000_Hz",
            "3000_Hz", "4000_Hz", "6000_Hz", "8000_Hz",
            "9000_Hz", "10000_Hz", "11200_Hz", "12500_Hz",
            "14000_Hz", "16000_Hz", "18000_Hz", "20000_Hz"]

keys_mtx = ["LANGUAGE", "Practice", "Sp_Bin_No_Bin",
            "Sp_L_No_Bin", "Sp_R_No_Bin", "Sp_L_No_L", "Sp_R_No_R"]

keys_teoae = ["Freq", "OAE", "Noise", "SNR", "Confidence"]
# value unit for "Freq" = "Hz"
# value unit for "OAE" = "dB"
# value unit for "Noise" = "dB"
# value unit for "SNR" = "dB"
# value unit for "Confidence" = "%"

keys_dpoae = []


keys_growth = ["Freq", "F1", "F2", "DP", "Noise+2sd", "SNR"]
# value unit for "Freq" = "Hz"
# value unit for "F1" = "dB"
# value unit for "F2" = "dB"
# value unit for "DP" = "dB"
# value unit for "Noise+2sd" = "dB"

columns = ["test", "key", "description", "unit", "levels"]
# print(columns)

index_pta = np.arange(0, len(keys_pta)).tolist()
# print(index_pta)
df_pta = pd.DataFrame(index=index_pta, columns=columns)
# print(df_pta)

for i in range(0, len(df_pta)):
    df_pta.at[i, "test"] = "PTA"
    df_pta.at[i, "key"] = keys_pta[i]
    keys_word_pta = keys_pta[i].replace("_", " ")
    df_pta.at[i, "description"] = f"Threshold obtained during a pure-tone audiometry test for {keys_word_pta}."
    df_pta.at[i, "unit"] = "dB HL"

df_pta.drop(labels="levels", axis=1, inplace=True)
print(df_pta)

index_mtx = np.arange(0, len(keys_mtx)).tolist()
# print(index_mtx)
df_mtx = pd.DataFrame(index=index_mtx, columns=columns)
# print(df_mtx)
dict_keys_mtx = {"LANGUAGE": "Language used for this run of the Matrix speech-in-noise perception test.",
                 "Practice": "First sequence of the run, used as a practice sequence. Speech presentation: Binaural/Noise presentation: Binaural",
                 "Sp_Bin_No_Bin": "Second sequence of the run. Speech presentation: Binaural/Noise presentation: Binaural",
                 "Sp_L_No_Bin": "Third sequence of the run. Speech presentation: Left ear/Noise presentation: Binaural",
                 "Sp_R_No_Bin": "Fourth sequence of the run. Speech presentation: Right ear/Noise presentation: Binaural",
                 "Sp_L_No_L": "Fifth sequence of the run. Speech presentation: Left ear/Noise presentation: Left ear",
                 "Sp_R_No_R": "Sixth sequence of the run. Speech presentation: Right ear/Noise presentation: Right ear"}

for j in range(0, len(df_mtx)):
    df_mtx.at[j, "test"] = "MTX"
    df_mtx.at[j, "key"] = keys_mtx[j]
    df_mtx.at[j, "description"] = dict_keys_mtx[keys_mtx[j]]

    if j == 0:
        df_mtx.at[j, "unit"] = "n/a"
        df_mtx.at[j, "levels"] = {"French": "French", "English": "English"}
    else:
        df_mtx.at[j, "unit"] = "dB"
        df_mtx.at[j, "levels"] = "n/a"

print(df_mtx)

index_tymp = np.arange(0, len(keys_tymp)).tolist()
print(index_tymp)
df_tymp = pd.DataFrame(index=index_tymp, columns=columns)
# print(df_tymp)

for k in range(0, len(df_tymp)):
    df_tymp.at[k, "test"] = "Tymp"
    df_tymp.at[k, "key"] = keys_tymp[k]
    keys_word_tymp = keys_tymp[k]

    if k == 0:
        df_tymp.at[k, "description"] = f"Value representing the shape type of the tympanometry response."
        df_tymp.at[k, "unit"] = "n/a"
        df_tymp.at[k, "levels"] = {"A": "Response within normal range", "As": "-", "Ad": "-"}
    else:
        df_tymp.at[k, "description"] = f"Value obtained for the parameter {keys_word_tymp}."
        df_tymp.at[k, "unit"] = "TBD"
        df_tymp.at[k, "levels"] = "n/a"

print(df_tymp)

index_reflex = np.arange(0, len(keys_reflex)).tolist()
# print(index_reflex)
df_reflex = pd.DataFrame(index=index_reflex, columns=columns)
# print(df_reflex)

for m in range(0, len(df_reflex)):
    df_reflex.at[m, "test"] = "Reflex"
    df_reflex.at[m, "key"] = keys_reflex[m]
    keys_word_reflex = keys_reflex[m].replace("_", " ")
    df_reflex.at[m, "description"] = f"Intensity level to obtain the stapedial reflex at/with {keys_word_reflex}."
    df_reflex.at[m, "unit"] = "dB"

print(df_reflex)
