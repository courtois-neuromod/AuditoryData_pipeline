import pandas as pd
import os
from shutil import copyfile
import glob
import BIDS_utils as utils

# Extraction of every single pure-tone audiometry test
# The results are then sent to the save_df function to be saved
def extract_pta(single_test_df, ls_columns_1, ls_columns_2, x):

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

        #print(y[0])
        for n in range(2, len(y[0])):
            if y[0][n] == 'n/a':
                #print(y[0][n], True)
                mask_0.append(True)
            else:
                #print(y[0][n], False)
                mask_0.append(False)

        #print(y[1])
        for p in range(2, len(y[1])):
            if y[1][p] == 'n/a':
                #print(y[1][p], True)
                mask_1.append(True)
            else:
                #print(y[1][p], False)
                mask_1.append(False)

        #print(single_test_df)
        #print(j, y)
        #print(mask_0, mask_1)

        if False in mask_1:
            #print("Keep 2nd line", y)
            pass
        else:
            #print("Delete 2nd line", y)
            del y[1]

        if False in mask_0:
            #print("Keep 1st line", y)
            pass
        else:
            #print("Delete 1st line", y)
            del y[0]

        #print(y.index)
        #print(len(y))
        if len(y) > 0:
            z = pd.DataFrame(data=y, columns=x).set_index("order")
            utils.save_df(z, single_test_df, j, 'PTA')
        else:
            continue
