import pandas as pd
from src import graph_functions as gf


subjects = ["Sub01", "Sub02", "Sub03", "Sub04", "Sub05", "Sub06"]

ls_columns_common = ["Participant_ID", "DATE", "Protocol name",
                     "Protocol condition", "Scan type"]

ls_columns_pta = ["RE_250", "RE_500", "RE_1000",
                  "RE_2000", "RE_3000", "RE_4000",
                  "RE_6000", "RE_8000", "RE_9000",
                  "RE_10000", "RE_11200", "RE_12500",
                  "RE_14000", "RE_16000", "RE_18000",
                  "RE_20000", "LE_250", "LE_500",
                  "LE_1000", "LE_2000", "LE_3000",
                  "LE_4000", "LE_6000", "LE_8000",
                  "LE_9000", "LE_10000", "LE_11200",
                  "LE_12500", "LE_14000", "LE_16000",
                  "LE_18000", "LE_20000"]

ls_columns_MTX1 = ["MTX1_LANG", "MTX1_L_L", "MTX1_L_Bin",
                   "MTX1_Bin_Bin", "MTX1_R_Bin", "MTX1_R_R"]
ls_columns_MTX2 = ["MTX2_LANG", "MTX2_L_L", "MTX2_L_Bin",
                   "MTX2_Bin_Bin", "MTX2_R_Bin", "MTX2_R_R"]

def eliminate_row_mtx(data_mtx, language):
    data_mtx = gf.eliminate_row(data_mtx,
                                "Protocol name",
                                "Baseline 1")
    data_mtx = gf.eliminate_row(data_mtx,
                                "Protocol condition",
                                "Condition 3A (OAEs right before the scan)")
    data_mtx = gf.eliminate_row(data_mtx,
                                "Protocol condition",
                                "Supplementary PTA test (Baseline)")
    data_mtx = gf.eliminate_row(data_mtx,
                                "Protocol condition",
                                "Suppl. PTA test (right before the scan)")
    data_mtx = gf.eliminate_row(data_mtx,
                                "Protocol condition",
                                "Suppl. PTA test (right after the scan)")
    if language == 1:
        pass

    elif language == 2:
        data_mtx = gf.eliminate_row(data_mtx,
                                    "Protocol condition",
                                    "Condition 1A (right before the scan)")
        data_mtx = gf.eliminate_row(data_mtx,
                                    "Protocol condition",
                                    "Condition 1B (right after the scan)")

    return data_mtx


def pta_graph(master_data, counter, save_error):

    ls_columns_pta_R = []
    ls_columns_pta_L = []

    for i in ls_columns_pta:
        if i.startswith("RE_"):
            ls_columns_pta_R.append(i)
        elif i.startswith("LE_"):
            ls_columns_pta_L.append(i)

    data_pta = master_data[ls_columns_common + ls_columns_pta]

    data_pta_R = master_data[ls_columns_common + ls_columns_pta_R]

    data_pta_L = master_data[ls_columns_common + ls_columns_pta_L]

    # Pure-tone audiometry
    data_pta = gf.eliminate_row(data_pta,
                                "Protocol condition",
                                "Condition 3A (OAEs right before the scan)")
    data_pta_L = gf.eliminate_row(data_pta_L,
                                  "Protocol condition",
                                  "Condition 3A (OAEs right before the scan)")
    data_pta_R = gf.eliminate_row(data_pta_R,
                                  "Protocol condition",
                                  "Condition 3A (OAEs right before the scan)")

    # Generation of the interactive graphs (.html file format)
    # PTA, Left ear
    for i in range(0, len(data_pta_L)):
        action_i = gf.plot_pta_L(data_pta_L.loc[[i]])
        if action_i is True:
            counter = counter + 1
        else:
            save_error = save_error + 1

    # PTA, Right ear
    for j in range(0, len(data_pta_R)):
        action_j = gf.plot_pta_R(data_pta_R.loc[[j]])
        if action_j is True:
            counter = counter + 1
        else:
            save_error = save_error + 1

    # PTA, All results for one participant in one graph
    for k in subjects:
        one_subject = gf.extract_subject(data_pta, k)
        action_k = gf.plot_pta_subject(one_subject)
        if action_k is True:
            counter = counter + 1
        else:
            save_error = save_error + 1

    # PTA, Box plot graph, Right ear
    for r in subjects:
        one_subject = gf.extract_subject(data_pta_R, r)
        action_r = gf.plot_boxplot_pta(one_subject, "Right ear")
        if action_r is True:
            counter = counter + 1
        else:
            save_error = save_error + 1

    # PTA, Box plot graph, Left ear
    for s in subjects:
        one_subject = gf.extract_subject(data_pta_L, s)
        action_s = gf.plot_boxplot_pta(one_subject, "Left ear")
        if action_s is True:
            counter = counter + 1
        else:
            save_error = save_error + 1

    return counter, save_error


def mtx_graph(master_data, counter, save_error):
    data_mtx_L1 = master_data[ls_columns_common + ls_columns_MTX1]

    data_mtx_L2 = master_data[ls_columns_common + ls_columns_MTX2]

    # Elimination of the lines that are irrelevant to each of the tests:
    # Matrix speech perception test
    # L1
    data_mtx_L1 = eliminate_row_mtx(data_mtx_L1, 1)

    # L2
    data_mtx_L2 = eliminate_row_mtx(data_mtx_L2, 2)    

    # MTX, L1
    for m in range(0, len(data_mtx_L1)):
        action_m = gf.plot_mtx(data_mtx_L1.loc[[m]], "L1")
        if action_m is True:
            counter = counter + 1
        else:
            save_error = save_error + 1

    # MTX, L2
    for n in range(0, len(data_mtx_L2)):
        df_line = data_mtx_L2.loc[[n]]
        if df_line["Participant_ID"][n] == "Sub06":
            continue
        else:
            action_n = gf.plot_mtx(data_mtx_L2.loc[[n]], "L2")
            if action_n is True:
                counter = counter + 1
            else:
                save_error = save_error + 1

    # MTX, L1, All results for one participant in one graph
    for p in subjects:
        one_subject = gf.extract_subject(data_mtx_L1, p)
        action_p = gf.plot_mtx_subject(one_subject, "L1")
        if action_p is True:
            counter = counter + 1
        else:
            save_error = save_error + 1

    # MTX, L2, All results for one participant in one graph
    for q in subjects:
        if q == "Sub06":
            continue
        else:
            one_subject = gf.extract_subject(data_mtx_L2, q)
            action_q = gf.plot_mtx_subject(one_subject, "L2")
            if action_q is True:
                counter = counter + 1
            else:
                save_error = save_error + 1

    return counter, save_error


def master_run(test_type="all"):
    master_data = gf.retrieve_db()
    
    # Counter initialisation to keep track of the amount of files generated
    counter = 0
    save_error = 0

    if test_type == "PTA":
        counter, save_error = pta_graph(master_data, counter, save_error)
    
    elif test_type == "MTX":
        counter, save_error = mtx_graph(master_data, counter, save_error)

    elif test_type == "TEOAE":
        pass

    elif test_type == "DPOAE":
        pass
    
    elif test_type == "Growth":
        pass

    elif test_type == "all":
        x1, y1 = pta_graph(master_data, counter, save_error)
        x2, y2 = mtx_graph(master_data, counter, save_error)
        counter = x1 + x2
        save_error = y1 + y2

    # Return a feedback to the user regarding the number of files created
    if counter <= 1:
        print(counter, ".html file was saved.")
        print(save_error, "file(s) was/were not properly saved")
    else:
        print(counter, ".html files were saved.")
        print(save_error, "file(s) was/were not properly saved")    


if __name__ == "__main__":
    master_run()

else:
    pass

