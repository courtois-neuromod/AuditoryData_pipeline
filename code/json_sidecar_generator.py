import pandas as pd
import numpy as np
import json
import os
from pathlib import Path

ls_task = ["Tymp", "Reflex", "PTA",
           "MTX", "TEOAE", "DPOAE",
           "Growth_2000", "Growth_4000", "Growth_6000"]

index = ["LongName", "Description", "Levels", "Units"]

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
# print(columns)
# print(index_pta)

df_pta = pd.DataFrame(index=index, columns=keys_pta)
# print(df_pta)

for a in keys_pta:
    if a == "order":
        df_pta.at["LongName", a] = "Order of acquisition"
        df_pta.at["Levels", a] = {"1": "First sequence acquired",
                                  "2": "Second sequence acquired"}
    elif a == "side":
        df_pta.at["LongName", a] = "Side of ear tested"
        df_pta.at["Levels", a] = {"R": "Right ear",
                                  "L": "Left ear"}
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

# index_mtx = np.arange(0, len(keys_mtx)).tolist()
# print(index_mtx)
df_mtx = pd.DataFrame(index=index, columns=keys_mtx)
print(df_mtx)
dict_LongName_mtx = {"Practice": "First condition of the sequence (see Description).",
                     "Sp_Bin_No_Bin": "Second condition of the sequence (see Description).",
                     "Sp_L_No_Bin": "Third condition of the sequence (see Description).",
                     "Sp_R_No_Bin": "Fourth condition of the sequence (see Description).",
                     "Sp_L_No_L": "Fifth condition of the sequence (see Description).",
                     "Sp_R_No_R": "Sixth condition of the sequence (see Description)."}

dict_Desc_mtx = {"Practice": "Speech presentation = Binaural/Noise presentation = Binaural. This condition is used as a practice/warm-up condition",
                 "Sp_Bin_No_Bin": "Speech presentation = Binaural/Noise presentation = Binaural",
                 "Sp_L_No_Bin": "Speech presentation = Left ear/Noise presentation = Binaural",
                 "Sp_R_No_Bin": "Speech presentation = Right ear/Noise presentation = Binaural",
                 "Sp_L_No_L": "Speech presentation = Left ear/Noise presentation = Left ear",
                 "Sp_R_No_R": "Speech presentation = Right ear/Noise presentation = Right ear"}

for d in keys_mtx:
    if d == "order":
        df_mtx.at["LongName", d] = "Order of acquisition"
        df_mtx.at["Levels", d] = {"1": "First sequence acquired",
                                  "2": "Second sequence acquired"}
    elif d == "LANGUAGE":
        df_mtx.at["LongName", d] = "Language used for this sequence of acquisition"
        df_mtx.at["Levels", d] = {"French": "French",
                                  "English": "English"}
    else:
        # keys_word_pta = a.replace("_", " ")
        df_mtx.at["LongName", d] = dict_LongName_mtx[d]
        df_mtx.at["Description", d] = f"The participants are asked to repeat out loud the sentences that are presented to them. This value represents the hearing threshold for a 50% rate of correct answers with these conditions: {dict_Desc_mtx[d]}."
        df_mtx.at["Units", d] = "dB"

print(df_mtx)

df_mtx.to_json("../results/BIDS_sidecars_originals/mtx_run_level.json", indent=2)

with open("../results/BIDS_sidecars_originals/mtx_run_level.json", "r") as origin:
    json_mtx = json.load(origin)
origin.close()

print(json_mtx)

for e in list(json_mtx.keys()):
    for f in list(json_mtx[e].keys()):
        if json_mtx[e][f] == None:
            del json_mtx[e][f]

print(json_pta)

Path("../results/BIDS_sidecars_originals/mtx_run_level.json").write_text(json.dumps(json_mtx,
                                                                                    indent=2,
                                                                                    ensure_ascii=False),
                                                                         encoding="UTF-8-SIG")


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


