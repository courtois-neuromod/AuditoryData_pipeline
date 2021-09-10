import pandas as pd
import numpy as np
import json
import os
from pathlib import Path

ls_task = ["Tymp", "Reflex", "PTA",
           "MTX", "TEOAE", "DPOAE",
           "Growth_2000", "Growth_4000", "Growth_6000"]

keys_tymp = ["order", "side", "Type", "TPP", "ECV", "SC", "TW"]
# value unit for "Type" = ""
# other values' unit = "?"

keys_reflex = ["order", "side", "500_Hz", "1000_Hz", "2000_Hz", "4000_Hz", 'NOISE']
# values' unit = "dB" for all

keys_pta = ["order", "side", "250_Hz", "500_Hz", "1000_Hz",
            "2000_Hz", "3000_Hz", "4000_Hz", "6000_Hz", "8000_Hz",
            "9000_Hz", "10000_Hz", "11200_Hz", "12500_Hz",
            "14000_Hz", "16000_Hz", "18000_Hz", "20000_Hz"]

keys_mtx = ["order", "LANGUAGE", "Practice", "Sp_Bin_No_Bin",
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

# columns = ["test", "key", "description", "unit", "levels"]
index_pta = ["LongName", "Description", "Levels", "Units"]
# print(columns)
# print(index_pta)

df_pta = pd.DataFrame(index=index_pta, columns=keys_pta)
# print(df_pta)

for a in keys_pta:
    if a == "order":
        df_pta.at["LongName", a] = "Order of acquisition"
        df_pta.at["Levels", a] = {"1":"First sequence acquired",
                                  "2":"Second sequence acquired"}
    elif a == "side":
        df_pta.at["LongName", a] = "Side of ear tested"
        df_pta.at["Levels", a] = {"R":"Right ear",
                                  "L":"Left ear"}
    else:
        keys_word_pta = a.replace("_", " ")
        df_pta.at["LongName", a] = f"Threshold at {keys_word_pta}"
        df_pta.at["Description", a] = f"The participants are asked to press a button when they hear a sound. This value represents the hearing threshold obtained with a pure-tone at {keys_word_pta}."
        df_pta.at["Units", a] = "dB HL"

df_pta.to_json("../results/BIDS_sidecars_originals/pta_run_level.json", indent=2)

with open("../results/BIDS_sidecars_originals/pta_run_level.json", "r") as origin:
    json_pta = json.load(origin)
origin.close()

# print(json_pta)

for b in list(json_pta.keys()):
    for c in list(json_pta[b].keys()):
        if json_pta[b][c] == None:
            del json_pta[b][c]

#print(json_pta)

Path("../results/BIDS_sidecars_originals/pta_run_level.json").write_text(json.dumps(json_pta,
                                                                                    indent=2,
                                                                                    ensure_ascii=False),
                                                                         encoding="UTF-8-SIG")







test_pta = pd.DataFrame({"order": {"LongName": "Order of acquisition",
                                   "Levels": {"1": "First sequence acquired",
                                              "2": "Second sequence acquired"}},
                         "Side": {"LongName": "Side of ear tested",
                                  "Levels": {"R": "Right ear",
                                             "L": "Left ear"}},
                         "250_Hz": {"LongName": "Threshold at 250 Hz",
                                    "Description": "The participants are asked to press a button when they hear a sound. This value represents the hearing threshold obtained with a pure-tone at 250 Hz.",
                                    "Unit": "dB HL"},
                         "500_Hz": {"LongName": "Threshold at 500 Hz",
                                    "Description": "The participants are asked to press a button when they hear a sound. This value represents the hearing threshold obtained with a pure-tone at 500 Hz.",
                                    "Unit": "dB HL"},
                         "1000_Hz": {"LongName": "Threshold at 1 kHz",
                                     "Description": "The participants are asked to press a button when they hear a sound. This value represents the hearing threshold obtained with a pure-tone at 1 kHz.",
                                     "Unit": "dB HL"},
                         "2000_Hz": {"LongName": "Threshold at 2 kHz",
                                     "Description": "The participants are asked to press a button when they hear a sound. This value represents the hearing threshold obtained with a pure-tone at 2 kHz.",
                                     "Unit": "dB HL"},
                         "3000_Hz": {"LongName": "Threshold at 3 kHz",
                                     "Description": "The participants are asked to press a button when they hear a sound. This value represents the hearing threshold obtained with a pure-tone at 3 kHz.",
                                     "Unit": "dB HL"},
                         "4000_Hz": {"LongName": "Threshold at 4 kHz",
                                     "Description": "The participants are asked to press a button when they hear a sound. This value represents the hearing threshold obtained with a pure-tone at 4 kHz.",
                                     "Unit": "dB HL"},
                         "6000_Hz": {"LongName": "Threshold at 6 kHz",
                                     "Description": "The participants are asked to press a button when they hear a sound. This value represents the hearing threshold obtained with a pure-tone at 6 kHz.",
                                     "Unit": "dB HL"},
                         "8000_Hz": {"LongName": "Threshold at 8 kHz",
                                     "Description": "The participants are asked to press a button when they hear a sound. This value represents the hearing threshold obtained with a pure-tone at 8 kHz.",
                                     "Unit": "dB HL"},
                         "9000_Hz": {"LongName": "Threshold at 9 kHz",
                                     "Description": "The participants are asked to press a button when they hear a sound. This value represents the hearing threshold obtained with a pure-tone at 9 kHz.",
                                     "Unit": "dB HL"},
                         "10000_Hz": {"LongName": "Threshold at 10 kHz",
                                      "Description": "The participants are asked to press a button when they hear a sound. This value represents the hearing threshold obtained with a pure-tone at 10 kHz.",
                                      "Unit": "dB HL"},
                         "11200_Hz": {"LongName": "Threshold at 11.2 kHz",
                                      "Description": "The participants are asked to press a button when they hear a sound. This value represents the hearing threshold obtained with a pure-tone at 11.2 kHz.",
                                      "Unit": "dB HL"},
                         "12500_Hz": {"LongName": "Threshold at 12.5 kHz",
                                      "Description": "The participants are asked to press a button when they hear a sound. This value represents the hearing threshold obtained with a pure-tone at 12.5 kHz.",
                                      "Unit": "dB HL"},
                         "14000_Hz": {"LongName": "Threshold at 14 kHz",
                                      "Description": "The participants are asked to press a button when they hear a sound. This value represents the hearing threshold obtained with a pure-tone at 14 kHz.",
                                      "Unit": "dB HL"},
                         "16000_Hz": {"LongName": "Threshold at 16 kHz",
                                      "Description": "The participants are asked to press a button when they hear a sound. This value represents the hearing threshold obtained with a pure-tone at 16 kHz.",
                                      "Unit": "dB HL"},
                         "18000_Hz": {"LongName": "Threshold at 18 kHz",
                                      "Description": "The participants are asked to press a button when they hear a sound. This value represents the hearing threshold obtained with a pure-tone at 18 kHz.",
                                      "Unit": "dB HL"},
                         "20000_Hz": {"LongName": "Threshold at 20 kHz",
                                      "Description": "The participants are asked to press a button when they hear a sound. This value represents the hearing threshold obtained with a pure-tone at 20 kHz.",
                                      "Unit": "dB HL"}})

# print(test_pta)

# test_pta.to_json("../results/BIDS_sidecars_originals/test_pta.json", indent=2)






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

#print(df_mtx)

index_tymp = np.arange(0, len(keys_tymp)).tolist()
#print(index_tymp)
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

#print(df_tymp)

index_reflex = np.arange(0, len(keys_reflex)).tolist()
# print(index_reflex)
df_reflex = pd.DataFrame(index=index_reflex, columns=columns)
# print(df_reflex)

for m in range(0, len(df_reflex)):
    df_reflex.at[m, "test"] = "Reflex"
    df_reflex.at[m, "key"] = keys_reflex[m]
    keys_word_reflex = keys_reflex[m].replace("_", " ")
    df_reflex.at[m, "description"] = f"Intensity level to obtain the stapedial reflex with {keys_word_reflex}."
    df_reflex.at[m, "unit"] = "dB"

#print(df_reflex)

# df_tymp = df_tymp.T

df_tymp.to_json("../results/BIDS_sidecars_originals/tymp_run_level.json", indent=2)
df_reflex.to_json("../results/BIDS_sidecars_originals/reflex_run_level.json", indent=2)
df_pta.to_json("../results/BIDS_sidecars_originals/pta_run_level.json", indent=2)
df_mtx.to_json("../results/BIDS_sidecars_originals/mtx_run_level.json", indent=2)


