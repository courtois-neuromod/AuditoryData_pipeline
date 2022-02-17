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

keys_teoae = ["order", "side", "freq1", "freq2",
              "oae", "noise", "snr", "confidence"]

keys_dpoae = ["order", "side", "freq1", "freq2", "l1",
              "l2", "dp", "snr", "noise+2sd", "noise+1sd",
              "2f2-f1", "3f1-2f2", "3f2-2f1", "4f1-3f2"]

keys_growth = ["order", "side", "freq1", "freq2", "l1",
               "l2", "dp", "snr", "noise+2sd", "noise+1sd",
               "2f2-f1", "3f1-2f2", "3f2-2f1", "4f1-3f2"]
# value unit for "freq1" and "freq2" = "Hz"
# value unit for "l1" and "l2" = "dB SPL"
# value unit for "dp" = "dB"
# value unit for "noise+2sd", "noise+1sd" = "dB"
# value unit for "2f2-f1", "3f1-2f2", "3f2-2f1", "4f1-3f2" = "dB"


# .json sidecar for the tympanometry test (Tymp)
df_tymp = pd.DataFrame(index=index, columns=keys_tymp)
#print("df_tymp\n", df_tymp)

dict_longname_tymp = {keys_tymp[3]: "Tympanometric peak pressure/"\
                                    "Middle ear pressure",
                      keys_tymp[4]: "Equivalent ear canal volume",
                      keys_tymp[5]: "Static admittance/Compliance",
                      keys_tymp[6]: "Tympanometric width"}
#print("dict_longname_tymp\n", dict_longname_tymp)

dict_desc_tymp = {keys_tymp[3]: "Maximal acoustic energy absorbance "\
                                "capacity of the tympanic membrane.",
                  keys_tymp[4]: "Volume of the auditory canal between "\
                                "the probe and the tympanic membrane.",
                  keys_tymp[5]: "Maximal acoustic energy absorbance "\
                                "capacity of the middle ear ossicles.",
                  keys_tymp[6]: "Pressure level at 50% of the "\
                                "tympanogram's peak."}
#print("dict_desc_tymp\n", dict_desc_tymp)

dict_units_tymp = {keys_tymp[3]: "daPa",
                   keys_tymp[4]: "mL",
                   keys_tymp[5]: "mL",
                   keys_tymp[6]: "daPa"}
#print("dict_units_tymp\n", dict_units_tymp)

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
#print("df_tymp filled\n", df_tymp)


# .json sidecar for the stapedial reflex test (Reflex)
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


# .json sidecar for the pure-tone audiometry test (PTA)
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


# .json sidecar for the matrix speech-in-noise perception test (MTX)
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


# .json sidecar for the transient-evoked otoacoustic emissions test (TEOAE)
df_teoae = pd.DataFrame(index=index, columns=keys_teoae)

dict_longname_teoae = {keys_teoae[2]: "Frequency #1",
                       keys_teoae[3]: "Frequency #2",
                       keys_teoae[4]: "Otoacoustic emissions response",
                       keys_teoae[5]: "Noise relative strength",
                       keys_teoae[6]: "Signal-to-noise ratio",
                       keys_teoae[7]: "Confidence level"}

dict_desc_teoae = {keys_teoae[2]: "Lower frequency (F1) used to produce "\
                                  "transient-evoked otoacoustic emissions. "\
                                  "The F2/F1 ratio = 1,22.",
                   keys_teoae[3]: "Higher frequency (F2) used to produce "\
                                  "transient-evoked otoacoustic emissions. "\
                                  "The F2/F1 ratio = 1,22.",
                   keys_teoae[4]: "Measured level of the transient-evoked "\
                                  "otoacoustic emissions.",
                   keys_teoae[5]: "Measured level of the noise relative "\
                                  "strength.",
                   keys_teoae[6]: "Difference between the measured level of "\
                                  "the transient-level otoacoustic emissions "\
                                  "and the measured noise relative strength "\
                                  "(TEOAE level - Noise level).",
                   keys_teoae[7]: "Level of confidence linked to the "\
                                  "obtained signal-to-noise ratio."}

dict_units_teoae = {keys_teoae[2]: "Hz",
                    keys_teoae[3]: "Hz",
                    keys_teoae[4]: "dB SPL",
                    keys_teoae[5]: "dB",
                    keys_teoae[6]: "dB",
                    keys_teoae[7]: "%"}

for k_teoae in keys_teoae:
    if k_teoae == keys_teoae[0]:
        df_teoae.at[index[0],
                    k_teoae] = long_order
        df_teoae.at[index[2],
                    k_teoae] = lvl_order

    elif k_teoae == keys_teoae[1]:
        df_teoae.at[index[0],
                    k_teoae] = long_side
        df_teoae.at[index[2],
                    k_teoae] = lvl_side

    else:
        df_teoae.at[index[0], k_teoae] = dict_longname_teoae[k_teoae]
        df_teoae.at[index[1], k_teoae] = dict_desc_teoae[k_teoae]
        df_teoae.at[index[3], k_teoae] = dict_units_teoae[k_teoae]


# .json sidecar for the distortion product otoacoustic emissions test (DPOAE)
df_dpoae = pd.DataFrame(index=index, columns=keys_dpoae)

dict_longname_dpoae = {keys_dpoae[2]: "Frequency #1",
                       keys_dpoae[3]: "Frequency #2",
                       keys_dpoae[4]: "Level for frequency #1",
                       keys_dpoae[5]: "Level for frequency #2",
                       keys_dpoae[6]: "Distortion product",
                       keys_dpoae[7]: "Signal-to-noise ratio",
                       keys_dpoae[8]: "Noise level plus two standard "\
                                      "deviations",
                       keys_dpoae[9]: "Noise level plus standard deviation",
                       keys_dpoae[10]: "Frequency #2 times two minus "\
                                       "frequency #1",
                       keys_dpoae[11]: "Frequency #1 times three minus "\
                                       "frequency #2 times two",
                       keys_dpoae[12]: "Frequency #2 times three minus "\
                                       "frequency #1 times two",
                       keys_dpoae[13]: "Frequency #1 times four minus "\
                                       "frequency #2 times three"}

dict_desc_dpoae = {keys_dpoae[2]: "Lower frequency (F1) used to produce "\
                                  "distortion product otoacoustic emissions. "\
                                  "The F2/F1 ratio = 1,22.",
                   keys_dpoae[3]: "Higher frequency (F2) used to produce "\
                                  "distortion product otoacoustic emissions. "\
                                  "The F2/F1 ratio = 1,22.",
                   keys_dpoae[4]: "Frequency #1's presentation level.",
                   keys_dpoae[5]: "Frequency #2's presentation level.",
                   keys_dpoae[6]: "Measured level of the distortion product "\
                                  "otoacoustic emissions.",
                   keys_dpoae[7]: "Difference between the measured level of "\
                                  "the distortion product otoacoustic "\
                                  "emissions and the measured noise relative "\
                                  "strength plus two standard deviations "\
                                  "(TEOAE level - (Noise level + 2 * SD)).",
                   keys_dpoae[8]: "Measured noise relative strength level "\
                                  "plus two standard deviations.",
                   keys_dpoae[9]: "Measured noise relative strength level "\
                                  "plus one standard deviation.",
                   keys_dpoae[10]: "Frequency #2 intensity times two minus "\
                                   "frequency #1 intensity (2 * F2 - F1).",
                   keys_dpoae[11]: "Frequency #1 intensity times three "\
                                   "minus frequency #2 times two "\
                                   "(3 * F1 - 2 * F2).",
                   keys_dpoae[12]: "Frequency #2 intensity times three "\
                                   "minus frequency #1 times two "\
                                   "(3 * F2 - 2 * F1).",
                   keys_dpoae[13]: "Frequency #1 intensity times four "\
                                   "minus frequency #2 times three "\
                                   "(4 * F1 - 3 * F2)."}

dict_units_dpoae = {keys_dpoae[2]: "Hz",
                    keys_dpoae[3]: "Hz",
                    keys_dpoae[4]: "dB SPL",
                    keys_dpoae[5]: "dB sPL",
                    keys_dpoae[6]: "dB",
                    keys_dpoae[7]: "dB",
                    keys_dpoae[8]: "dB",
                    keys_dpoae[9]: "dB",
                    keys_dpoae[10]: "dB",
                    keys_dpoae[11]: "dB",
                    keys_dpoae[12]: "dB",
                    keys_dpoae[13]: "dB"}

for k_dpoae in keys_dpoae:
    if k_dpoae == keys_dpoae[0]:
        df_dpoae.at[index[0],
                    k_dpoae] = long_order
        df_dpoae.at[index[2],
                    k_dpoae] = lvl_order

    elif k_dpoae == keys_dpoae[1]:
        df_dpoae.at[index[0],
                    k_dpoae] = long_side
        df_dpoae.at[index[2],
                    k_dpoae] = lvl_side

    else:
        df_dpoae.at[index[0], k_dpoae] = dict_longname_dpoae[k_dpoae]
        df_dpoae.at[index[1], k_dpoae] = dict_desc_dpoae[k_dpoae]
        df_dpoae.at[index[3], k_dpoae] = dict_units_dpoae[k_dpoae]


# .json sidecar for the distortion product growth function test (DP-Growth)
df_growth = pd.DataFrame(index=index, columns=keys_growth)
#print("df_growth\n", df_growth)

dict_longname_growth = {keys_growth[2]: "Frequency #1",
                        keys_growth[3]: "Frequency #2",
                        keys_growth[4]: "Level for frequency #1",
                        keys_growth[5]: "Level for frequency #2",
                        keys_growth[6]: "Distortion product",
                        keys_growth[7]: "Signal-to-noise ratio",
                        keys_growth[8]: "Noise level plus two standard "\
                                        "deviations",
                        keys_growth[9]: "Noise level plus standard deviation",
                        keys_growth[10]: "Frequency #2 times two minus "\
                                         "frequency #1",
                        keys_growth[11]: "Frequency #1 times three minus "\
                                         "frequency #2 times two",
                        keys_growth[12]: "Frequency #2 times three minus "\
                                         "frequency #1 times two",
                        keys_growth[13]: "Frequency #1 times four minus "\
                                         "frequency #2 times three"}
#print("dict_longname_growth\n", dict_longname_growth)

dict_desc_growth = {keys_growth[2]: "Lower frequency (F1) used to produce "\
                                    "distortion product otoacoustic "\
                                    "emissions. The F2/F1 ratio = 1,22.",
                    keys_growth[3]: "Higher frequency (F2) used to produce "\
                                    "distortion product otoacoustic "\
                                    "emissions. The F2/F1 ratio = 1,22.",
                    keys_growth[4]: "Frequency #1's presentation level.",
                    keys_growth[5]: "Frequency #2's presentation level.",
                    keys_growth[6]: "Measured level of the distortion "\
                                    "product otoacoustic emissions.",
                    keys_growth[7]: "Difference between the measured level "\
                                    "of the distortion product otoacoustic "\
                                    "emissions and the measured noise "\
                                    "relative strength plus two standard "\
                                    "deviations (TEOAE level - (Noise level "\
                                    "+ 2 * SD)).",
                    keys_growth[8]: "Measured noise relative strength level "\
                                    "plus two standard deviations.",
                    keys_growth[9]: "Measured noise relative strength level "\
                                    "plus one standard deviation.",
                    keys_growth[10]: "Frequency #2 intensity times two minus "\
                                     "frequency #1 intensity (2 * F2 - F1).",
                    keys_growth[11]: "Frequency #1 intensity times three "\
                                     "minus frequency #2 times two "\
                                     "(3 * F1 - 2 * F2).",
                    keys_growth[12]: "Frequency #2 intensity times three "\
                                     "minus frequency #1 times two "\
                                     "(3 * F2 - 2 * F1).",
                    keys_growth[13]: "Frequency #1 intensity times four "\
                                     "minus frequency #2 times three "\
                                     "(4 * F1 - 3 * F2)."}
#print("dict_desc_growth\n", dict_desc_growth)

dict_units_growth = {keys_growth[2]: "Hz",
                     keys_growth[3]: "Hz",
                     keys_growth[4]: "dB SPL",
                     keys_growth[5]: "dB sPL",
                     keys_growth[6]: "dB",
                     keys_growth[7]: "dB",
                     keys_growth[8]: "dB",
                     keys_growth[9]: "dB",
                     keys_growth[10]: "dB",
                     keys_growth[11]: "dB",
                     keys_growth[12]: "dB",
                     keys_growth[13]: "dB"}
#print("dict_units_growth\n", dict_units_growth)

for k_growth in keys_growth:
    if k_growth == keys_growth[0]:
        df_growth.at[index[0],
                     k_growth] = long_order
        df_growth.at[index[2],
                     k_growth] = lvl_order

    elif k_growth == keys_growth[1]:
        df_growth.at[index[0],
                     k_growth] = long_side
        df_growth.at[index[2],
                     k_growth] = lvl_side

    else:
        df_growth.at[index[0], k_growth] = dict_longname_growth[k_growth]
        df_growth.at[index[1], k_growth] = dict_desc_growth[k_growth]
        df_growth.at[index[3], k_growth] = dict_units_growth[k_growth]
#print("df_growth filled\n", df_growth)


if __name__ == "__main__":

    parent_path = os.path.join("..", "results")
    content_parent_path = os.listdir(parent_path)
    content_parent_path.sort()

    if content_parent_path.count("BIDS_sidecars_originals") == 1:
        pass
    else:
        os.mkdir(os.path.join(parent_path, "BIDS_sidecars_originals"))

    save_folder = os.path.join(parent_path, "BIDS_sidecars_originals")

    
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

# Save the TEOAE .json sidecar
df_teoae.to_json(os.path.join(save_folder, "teoae_run_level.json"),
                 indent=2)

with open(os.path.join(save_folder, "teoae_run_level.json"),
          "r") as origin:
    json_teoae = json.load(origin)
origin.close()

for i in list(json_teoae.keys()):
    for j in list(json_teoae[i].keys()):
        if json_teoae[i][j] == None:
            del json_teoae[i][j]

to_write = Path(os.path.join(save_folder, "teoae_run_level.json"))
to_write.write_text(json.dumps(json_teoae,
                               indent=2,
                               ensure_ascii=False),
                    encoding=utf)

# Save the DPOAE .json sidecar
df_dpoae.to_json(os.path.join(save_folder, "dpoae_run_level.json"),
                 indent=2)

with open(os.path.join(save_folder, "dpoae_run_level.json"),
          "r") as origin:
    json_dpoae = json.load(origin)
origin.close()

for i in list(json_dpoae.keys()):
    for j in list(json_dpoae[i].keys()):
        if json_dpoae[i][j] == None:
            del json_dpoae[i][j]

to_write = Path(os.path.join(save_folder, "dpoae_run_level.json"))
to_write.write_text(json.dumps(json_dpoae,
                               indent=2,
                               ensure_ascii=False),
                    encoding=utf)

# Save the DP-Growth .json sidecar
df_growth.to_json(os.path.join(save_folder, "growth_run_level.json"),
                  indent=2)

with open(os.path.join(save_folder, "growth_run_level.json"),
          "r") as origin:
    json_growth = json.load(origin)
origin.close()

for i in list(json_growth.keys()):
    for j in list(json_growth[i].keys()):
        if json_growth[i][j] == None:
            del json_growth[i][j]

to_write = Path(os.path.join(save_folder, "growth_run_level.json"))
to_write.write_text(json.dumps(json_growth,
                               indent=2,
                               ensure_ascii=False),
                    encoding=utf)
