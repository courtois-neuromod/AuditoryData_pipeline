import os
import pandas as pd
import json
from pathlib import Path

utf = "UTF-8-SIG"

long_order = "Order of acquisition"
long_side = "Side of ear tested"
lvl_order = {"1": "First sequence acquired",
             "2": "Second sequence acquired"}
lvl_side = {"R": "Right ear", "L": "Left ear"}

ls_task = ["Tymp", "Reflex", "PTA",
           "MTX", "TEOAE", "DPOAE",
           "Growth_2000", "Growth_4000", "Growth_6000"]

index = ["LongName", "Description", "Levels", "Units"]

keys_tymp = ["order", "side", "type", "tpp", "ecv", "sc", "tw"]

keys_reflex = ["order", "side",
               "500_hz", "1000_hz", "2000_hz", "4000_hz", 'noise']

keys_pta = ["order", "side", "250_hz", "500_hz", "1000_hz",
            "2000_hz", "3000_hz", "4000_hz", "6000_hz", "8000_hz",
            "9000_hz", "10000_hz", "11200_hz", "12500_hz",
            "14000_hz", "16000_hz", "18000_hz", "20000_hz"]

keys_mtx = ["order", "language", "practice", "sp_bin_no_bin",
            "sp_l_no_bin", "sp_r_no_bin", "sp_l_no_l", "sp_r_no_r"]

keys_teoae = ["freq", "oae", "noise", "snr", "confidence"]
# value unit for "Freq" = "Hz"
# value unit for "OAE" = "dB"
# value unit for "Noise" = "dB"
# value unit for "SNR" = "dB"
# value unit for "Confidence" = "%"

keys_dpoae = []

keys_growth = ["freq", "f1", "f2", "dp", "noise+2sd", "snr"]
# value unit for "Freq" = "Hz"
# value unit for "F1" = "dB"
# value unit for "F2" = "dB"
# value unit for "DP" = "dB"
# value unit for "Noise+2sd" = "dB"


# .json sidecar for the tympanometry
df_tymp = pd.DataFrame(index=index, columns=keys_tymp)

dict_longname_tymp = {keys_tymp[3]: "Tympanometric peak pressure/"\
                                    "Middle ear pressure",
                      keys_tymp[4]: "Equivalent ear canal volume",
                      keys_tymp[5]: "Static admittance/Compliance",
                      keys_tymp[6]: "Tympanometric width"}

dict_desc_tymp = {keys_tymp[3]: "Maximal acoustic energy absorbance "\
                                "capacity of the tympanic membrane.",
                  keys_tymp[4]: "Volume of the auditory canal between "\
                                "the probe and the tympanic membrane.",
                  keys_tymp[5]: "Maximal acoustic energy absorbance "\
                                "capacity of the middle ear ossicles.",
                  keys_tymp[6]: "Pressure level at 50% of the "\
                                "tympanogram's peak."}

dict_units_tymp = {keys_tymp[3]: "daPa",
                   keys_tymp[4]: "mL",
                   keys_tymp[5]: "mL",
                   keys_tymp[6]: "daPa"}

for k_tymp in keys_tymp:
    if k_tymp == keys_tymp[0]:
        df_tymp.at[index[0],
                   k_tymp] = long_order
        df_tymp.at[index[2],
                   k_tymp] = lvl_order

    elif k_tymp == keys_tymp[1]:
        df_tymp.at[index[0],
                   k_tymp] = long_side
        df_tymp.at[index[2],
                   k_tymp] = lvl_side

    elif k_tymp == keys_tymp[2]:
        df_tymp.at[index[0],
                   k_tymp] = "Type of curve"
        df_tymp.at[index[1],
                   k_tymp] = "The type parameter is a simplified "\
                             "representation of the actual tympanogram "\
                             "curve. It provides an indication on the "\
                             "shape of the response curve and a clinical "\
                             "judgement on the normality of the result."
        df_tymp.at[index[2],
                   k_tymp] = {"A": "Within normal mobility range",
                              "Ad": "Presents a higher than expected "\
                                    "mobility of the tympanic membrane",
                              "As": "Presents a lower than expected "\
                                    "mobility of the tympanic membrane",
                              "B": "Presents a very low mobility of the "\
                                   "tympanic membrane",
                              "C": "Presents a lower fluid pressure in "\
                                   "the middle ear than in the ear canal",
                              "D": " *** DESCRIPTION TO BE ADDED *** ",
                              "E": " *** DESCRIPTION TO BE ADDED *** "}

    else:
        df_tymp.at[index[0], k_tymp] = dict_longname_tymp[k_tymp]
        df_tymp.at[index[1], k_tymp] = dict_desc_tymp[k_tymp]
        df_tymp.at[index[3], k_tymp] = dict_units_tymp[k_tymp]


# .json sidecar for the stapedial reflex
df_reflex = pd.DataFrame(index=index, columns=keys_reflex)

dict_desc_reflex = {"500_hz": "",
                    "1000_hz": "",
                    "2000_hz": "",
                    "4000_hz": ""}

for k_ref in keys_reflex:
    if k_ref == keys_reflex[0]:
        df_reflex.at[index[0], k_ref] = long_order
        df_reflex.at[index[2], k_ref] = lvl_order

    elif k_ref == keys_reflex[1]:
        df_reflex.at[index[0], k_ref] = long_side
        df_reflex.at[index[2], k_ref] = lvl_side

    elif k_ref == keys_reflex[6]:
        df_reflex.at[index[0], k_ref] = f"Stapedial reflex threshold for "\
                                        f"broadband {k_ref}"
        df_reflex.at[index[1], k_ref] = ""
        df_reflex.at[index[3], k_ref] = "dB HL"

    else:
        keys_word_reflex = k_ref.replace("_", " ").title()
        df_reflex.at[index[0], k_ref] = f"Stapedial reflex threshold "\
                                        f"at {keys_word_reflex}"
        df_reflex.at[index[1], k_ref] = dict_desc_reflex[k_ref]
        df_reflex.at[index[3], k_ref] = "dB HL"


# .json sidecar for the pure-tone audiometry
df_pta = pd.DataFrame(index=index, columns=keys_pta)

for k_pta in keys_pta:
    if k_pta == keys_pta[0]:
        df_pta.at[index[0], k_pta] = long_order
        df_pta.at[index[2], k_pta] = lvl_order

    elif k_pta == keys_pta[1]:
        df_pta.at[index[0], k_pta] = long_side
        df_pta.at[index[2], k_pta] = lvl_side

    else:
        keys_word_pta = k_pta.replace("_", " ").title()
        df_pta.at[index[0], k_pta] = f"Threshold at {keys_word_pta}"
        df_pta.at[index[1],
                  k_pta] = f"The participants are asked to press a "\
                           f"button when they hear a sound. This value "\
                           f"represents the hearing threshold obtained "\
                           f"with a pure-tone at {keys_word_pta}."
        df_pta.at[index[3], k_pta] = "dB HL"

# .json sidecar for the matrix speech-in-noise perception test
df_mtx = pd.DataFrame(index=index, columns=keys_mtx)

dict_longname_mtx = {"practice": "First condition of the sequence "\
                                 "(see Description).",
                     "sp_bin_no_bin": "Second condition of the sequence "\
                                      "(see Description).",
                     "sp_l_no_bin": "Third condition of the sequence "\
                                    "(see Description).",
                     "sp_r_no_bin": "Fourth condition of the sequence "\
                                    "(see Description).",
                     "sp_l_no_l": "Fifth condition of the sequence "\
                                  "(see Description).",
                     "sp_r_no_r": "Sixth condition of the sequence "\
                                  "(see Description)."}

dict_desc_mtx = {"practice": "Speech presentation = Binaural/"\
                             "Noise presentation = Binaural. "\
                             "This condition is used as a practice/"\
                             "warm-up condition",
                 "sp_bin_no_bin": "Speech presentation = Binaural/"\
                                  "Noise presentation = Binaural",
                 "sp_l_no_bin": "Speech presentation = Left ear/"\
                                "Noise presentation = Binaural",
                 "sp_r_no_bin": "Speech presentation = Right ear/"\
                                "Noise presentation = Binaural",
                 "sp_l_no_l": "Speech presentation = Left ear/"\
                              "Noise presentation = Left ear",
                 "sp_r_no_r": "Speech presentation = Right ear/"\
                              "Noise presentation = Right ear"}

for k_mtx in keys_mtx:
    if k_mtx == keys_mtx[0]:
        df_mtx.at[index[0], k_mtx] = long_order
        df_mtx.at[index[2], k_mtx] = lvl_order

    elif k_mtx == keys_mtx[1]:
        df_mtx.at[index[0],
                  k_mtx] = "Language used for this sequence of acquisition"
        df_mtx.at[index[2], k_mtx] = {"French": "French",
                                      "English": "English"}

    else:
        df_mtx.at[index[0], k_mtx] = dict_longname_mtx[k_mtx]
        df_mtx.at[index[1],
                  k_mtx] = f"The participants are asked to repeat out "\
                           f"loud the sentences that are presented to "\
                           f"them. This value represents the hearing "\
                           f"threshold for a 50% rate of correct "\
                           f"answers with these conditions: "\
                           f"{dict_desc_mtx[k_mtx]}."
        df_mtx.at[index[3], k_mtx] = "dB"


if __name__ == "__main__":

    parent_path = os.path.join("..", "results")
    content_parent_path = os.listdir(parent_path)
    content_parent_path.sort()

    if content_parent_path.count("BIDS_sidecars_originals") == 1:
        pass
    else:
        os.mkdir(os.path.join(parent_path, "BIDS_sidecars_originals"))

    save_folder = os.path.join(parent_path, "BIDS_sidecars_originals")

    # Save the tympanometry .json sidecar
    df_tymp.to_json(os.path.join(save_folder, "tymp_run_level.json"), indent=2)

    with open(os.path.join(save_folder, "tymp_run_level.json"), "r") as origin:
        json_tymp = json.load(origin)
    origin.close()

    for i in list(json_tymp.keys()):
        for j in list(json_tymp[i].keys()):
            if json_tymp[i][j] == None:
                del json_tymp[i][j]

    to_write = Path(os.path.join(save_folder, "tymp_run_level.json"))
    to_write.write_text(json.dumps(json_tymp,
                                   indent=2,
                                   ensure_ascii=False),
                        encoding=utf)

    # Save the stapedial reflex .json sidecar
    df_reflex.to_json(os.path.join(save_folder,
                                   "reflex_run_level.json"),
                                   indent=2)

    with open(os.path.join(save_folder, "reflex_run_level.json"),
              "r") as origin:
        json_reflex = json.load(origin)
    origin.close()

    for i in list(json_reflex.keys()):
        for j in list(json_reflex[i].keys()):
            if json_reflex[i][j] == None:
                del json_reflex[i][j]

    to_write = Path(os.path.join(save_folder, "reflex_run_level.json"))
    to_write.write_text(json.dumps(json_reflex,
                                   indent=2,
                                   ensure_ascii=False),
                        encoding=utf)

    # Save the PTA .json sidecar
    df_pta.to_json(os.path.join(save_folder, "pta_run_level.json"), indent=2)

    with open(os.path.join(save_folder, "pta_run_level.json"), "r") as origin:
        json_pta = json.load(origin)
    origin.close()

    for i in list(json_pta.keys()):
        for j in list(json_pta[i].keys()):
            if json_pta[i][j] == None:
                del json_pta[i][j]

    to_write = Path(os.path.join(save_folder, "pta_run_level.json"))
    to_write.write_text(json.dumps(json_pta,
                                   indent=2,
                                   ensure_ascii=False),
                        encoding=utf)

    # Save the MTX .json sidecar
    df_mtx.to_json(os.path.join(save_folder, "mtx_run_level.json"), indent=2)

    with open(os.path.join(save_folder, "mtx_run_level.json"), "r") as origin:
        json_mtx = json.load(origin)
    origin.close()

    for i in list(json_mtx.keys()):
        for j in list(json_mtx[i].keys()):
            if json_mtx[i][j] == None:
                del json_mtx[i][j]

    to_write = Path(os.path.join(save_folder, "mtx_run_level.json"))
    to_write.write_text(json.dumps(json_mtx,
                                   indent=2,
                                   ensure_ascii=False),
                        encoding=utf)


else:

    parent_path = os.path.join("results")
    content_parent_path = os.listdir(parent_path)
    content_parent_path.sort()

    if content_parent_path.count("BIDS_sidecars_originals") == 1:
        pass
    else:
        os.mkdir(os.path.join(parent_path, "BIDS_sidecars_originals"))

    save_folder = os.path.join(parent_path, "BIDS_sidecars_originals")

    # Save the tympanometry .json sidecar
    df_tymp.to_json(os.path.join(save_folder, "tymp_run_level.json"), indent=2)

    with open(os.path.join(save_folder, "tymp_run_level.json"), "r") as origin:
        json_tymp = json.load(origin)
    origin.close()

    for i in list(json_tymp.keys()):
        for j in list(json_tymp[i].keys()):
            if json_tymp[i][j] == None:
                del json_tymp[i][j]

    to_write = Path(os.path.join(save_folder, "tymp_run_level.json"))
    to_write.write_text(json.dumps(json_tymp,
                                   indent=2,
                                   ensure_ascii=False),
                        encoding=utf)

    # Save the stapedial reflex .json sidecar
    df_reflex.to_json(os.path.join(save_folder,
                                   "reflex_run_level.json"),
                                   indent=2)

    with open(os.path.join(save_folder, "reflex_run_level.json"),
              "r") as origin:
        json_reflex = json.load(origin)
    origin.close()

    for i in list(json_reflex.keys()):
        for j in list(json_reflex[i].keys()):
            if json_reflex[i][j] == None:
                del json_reflex[i][j]

    to_write = Path(os.path.join(save_folder, "reflex_run_level.json"))
    to_write.write_text(json.dumps(json_reflex,
                                   indent=2,
                                   ensure_ascii=False),
                        encoding=utf)

    # Save the PTA .json sidecar
    df_pta.to_json(os.path.join(save_folder, "pta_run_level.json"), indent=2)

    with open(os.path.join(save_folder, "pta_run_level.json"), "r") as origin:
        json_pta = json.load(origin)
    origin.close()

    for i in list(json_pta.keys()):
        for j in list(json_pta[i].keys()):
            if json_pta[i][j] == None:
                del json_pta[i][j]

    to_write = Path(os.path.join(save_folder, "pta_run_level.json"))
    to_write.write_text(json.dumps(json_pta,
                                   indent=2,
                                   ensure_ascii=False),
                        encoding=utf)

    # Save the MTX .json sidecar
    df_mtx.to_json(os.path.join(save_folder, "mtx_run_level.json"), indent=2)

    with open(os.path.join(save_folder, "mtx_run_level.json"), "r") as origin:
        json_mtx = json.load(origin)
    origin.close()

    for i in list(json_mtx.keys()):
        for j in list(json_mtx[i].keys()):
            if json_mtx[i][j] == None:
                del json_mtx[i][j]

    to_write = Path(os.path.join(save_folder, "mtx_run_level.json"))
    to_write.write_text(json.dumps(json_mtx,
                                   indent=2,
                                   ensure_ascii=False),
                        encoding=utf)
