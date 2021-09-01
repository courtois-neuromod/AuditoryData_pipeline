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
# values' unit = "dB HL" for all

keys_mtx = ["LANGUAGE", "Practice", "Sp_Bin_No_Bin",
            "Sp_L_No_Bin", "Sp_R_No_Bin", "Sp_L_No_L", "Sp_R_No_R"]
# value levels for LANGUAGE = "French" or "English"
# other values' unit = "dB"

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

index = np.arange(0, len(keys_pta)).tolist()
print(index)
columns = ["test", "key", "description", "unit", "levels"]
print(columns)
df_pta = pd.DataFrame(index=index, columns=columns)
print(df_pta)

for i in range(0, len(df_pta)):
    df_pta.at[i, "test"] = "PTA"
    df_pta.at[i, "key"] = keys_pta[i]
    keys_word_pta = keys_pta[i].replace("_", " ")
    df_pta.at[i, "description"] = f"Threshold obtained during a pure-tone audiometry test for {keys_word_pta}."
    df_pta.at[i, "unit"] = "dB HL"

df_pta.drop(labels="levels", axis=1, inplace=True)
df_pta

