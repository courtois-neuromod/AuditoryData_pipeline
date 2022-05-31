import os
import pandas as pd
#from src import BIDS_utils as utils
from src import graph_functions as gf
from src import graph_PTA_BIDS as pta
from src import graph_MTX_BIDS as mtx
from src import graph_TEOAE as teoae
from src import graph_DPOAE as dpoae
from src import graph_DPGrowth as growth
from src import common_functions as common


subjects = ["Sub01", "Sub02", "Sub03", "Sub04", "Sub05", "Sub06"]

#ls_columns_common = ["Participant_ID", "DATE", "Protocol name",
#                     "Protocol condition", "Scan type"]

#ls_columns_pta = ["RE_250", "RE_500", "RE_1000",
#                  "RE_2000", "RE_3000", "RE_4000",
#                  "RE_6000", "RE_8000", "RE_9000",
#                  "RE_10000", "RE_11200", "RE_12500",
#                  "RE_14000", "RE_16000", "RE_18000",
#                  "RE_20000", "LE_250", "LE_500",
#                  "LE_1000", "LE_2000", "LE_3000",
#                  "LE_4000", "LE_6000", "LE_8000",
#                  "LE_9000", "LE_10000", "LE_11200",
#                  "LE_12500", "LE_14000", "LE_16000",
#                  "LE_18000", "LE_20000"]

#ls_columns_MTX1 = ["MTX1_LANG", "MTX1_L_L", "MTX1_L_Bin",
#                   "MTX1_Bin_Bin", "MTX1_R_Bin", "MTX1_R_R"]
#ls_columns_MTX2 = ["MTX2_LANG", "MTX2_L_L", "MTX2_L_Bin",
#                   "MTX2_Bin_Bin", "MTX2_R_Bin", "MTX2_R_R"]


#def eliminate_row_mtx(data_mtx, language):
#    data_mtx = gf.eliminate_row(data_mtx,
#                                "Protocol name",
#                                "Baseline 1")
#    data_mtx = gf.eliminate_row(data_mtx,
#                                "Protocol condition",
#                                "Condition 3A (OAEs right before the scan)")
#    data_mtx = gf.eliminate_row(data_mtx,
#                                "Protocol condition",
#                                "Supplementary PTA test (Baseline)")
#    data_mtx = gf.eliminate_row(data_mtx,
#                                "Protocol condition",
#                                "Suppl. PTA test (right before the scan)")
#    data_mtx = gf.eliminate_row(data_mtx,
#                                "Protocol condition",
#                                "Suppl. PTA test (right after the scan)")
#    if language == 1:
#        pass

#    elif language == 2:
#        data_mtx = gf.eliminate_row(data_mtx,
#                                    "Protocol condition",
#                                    "Condition 1A (right before the scan)")
#        data_mtx = gf.eliminate_row(data_mtx,
#                                    "Protocol condition",
#                                    "Condition 1B (right after the scan)")

#    return data_mtx


def pta_graph(result_path, counter, save_error):
    """
    This function generates and save the PTA test figures
    INPUTS:
    -result_path: path to the results folder [repo_root]/results/
    -counter: variable tracking the amount of files produced by the script
    -save_error: variable tracking the amount of files that were not
                 properly saved
    OUTPUTS:
    -returns an updated value for the saved files counter and the save_error
     counter as well as the saved figures
    """

    print("Generating PTA graphs...\n")
    data_path = os.path.join(result_path, "BIDS_data")

    # extract the list of subject folders
    ls_folders_sub = os.listdir(data_path)
    ls_folders_sub.sort()
    #print("sub:", ls_folders_sub, "\n")
    
    for i in ls_folders_sub:
        path_sub = os.path.join(data_path, i)
        
        # extract the list of session folders within a subject folder
        ls_folders_ses = os.listdir(path_sub)
        ls_folders_ses.sort()
        ls_folders_ses.pop(-1)
        ls_folders_ses.pop(-1)
        #print("ses:", ls_folders_ses, "\n")
        
        for j in ls_folders_ses:
            path_ses = os.path.join(path_sub, j)
            
            # extract the list of data files within a session folder
            ls_files_test = os.listdir(path_ses)
            ls_files_test.sort()
            #print("tests:", ls_files_test, "\n")
            
            ls_pta = []
            
            for k in ls_files_test:
                if (k.find("PTA") != -1
                        and k.endswith(".tsv")):
                    ls_pta.append(k)
                else:
                    pass
            
            #print(ls_pta)
            
            if len(ls_pta) == 0:
                continue
            else:
                for m in ls_pta:
                    df = pd.read_csv(os.path.join(path_ses, m),
                                     sep="\t")
                    #print(df)
                    
                    # PTA, Right ear
                    mask_R = df["side"] == "R"
                    df_R = df[mask_R].reset_index(drop=True)
                    action_R = pta.plot_pta(result_path, df_R,
                                            m, "R")
                    if action_R is True:
                        counter = counter + 1
                    else:
                        save_error = save_error + 1
                   
                    # PTA, Left ear
                    mask_L = df["side"] == "L"
                    df_L = df[mask_L].reset_index(drop=True)
                    action_L = pta.plot_pta(result_path, df_L,
                                            m, "L")
                    if action_L is True:
                        counter = counter + 1
                    else:
                        save_error = save_error + 1

                    # PTA, Both ears
                    action_both = pta.plot_pta(result_path, df,
                                               m, "Both")
                    if action_both is True:
                        counter = counter + 1
                    else:
                        save_error = save_error + 1 
                    
                    #print(df, "\n", df_R, "\n", df_L, "\n")

    return counter, save_error

#    # PTA, All results for one participant in one graph
#    for k in subjects:
#        one_subject = gf.extract_subject(data_pta, k)
#        action_k = pta.plot_pta_subject(result_path, one_subject)
#        if action_k is True:
#            counter = counter + 1
#        else:
#            save_error = save_error + 1

#    # PTA, Box plot graph, Right ear
#    for r in subjects:
#        one_subject = gf.extract_subject(data_pta_R, r)
#        action_r = pta.plot_boxplot_pta(result_path, one_subject, "Right ear")
#        if action_r is True:
#            counter = counter + 1
#        else:
#            save_error = save_error + 1

#    # PTA, Box plot graph, Left ear
#    for s in subjects:
#        one_subject = gf.extract_subject(data_pta_L, s)
#        action_s = pta.plot_boxplot_pta(result_path, one_subject, "Left ear")
#        if action_s is True:
#            counter = counter + 1
#        else:
#            save_error = save_error + 1

#    return counter, save_error

###############################################################################

def mtx_graph(result_path, counter, save_error):
    """
    This function generates and save the MTX test figures
    INPUTS:
    -result_path: path to the results folder [repo_root]/results/
    -counter: variable tracking the amount of files produced by the script
    -save_error: variable tracking the amount of files that were not
                 properly saved
    OUTPUTS:
    -returns an updated value for the saved files counter and the save_error
     counter as well as the saved figures
    """

    print("Generating MTX graphs...\n")
    data_path = os.path.join(result_path, "BIDS_data")

    # extract the list of subject folders
    ls_folders_sub = os.listdir(data_path)
    ls_folders_sub.sort()
    #print("sub:", ls_folders_sub, "\n")

    for i in ls_folders_sub:
        path_sub = os.path.join(data_path, i)
        
        # extract the list of session folders within a subject folder
        ls_folders_ses = os.listdir(path_sub)
        ls_folders_ses.sort()
        ls_folders_ses.pop(-1)
        ls_folders_ses.pop(-1)
        #print("ses:", ls_folders_ses, "\n")
        
        ls_mtx_all = []
        
        for j in ls_folders_ses:
            path_ses = os.path.join(path_sub, j)

            # extract the list of data files within a session folder
            ls_files_test = os.listdir(path_ses)
            ls_files_test.sort()
            #print("tests:", ls_files_test, "\n")
            
            ls_mtx = []
            
            for k in ls_files_test:
                if (k.find("MTX") != -1
                        and k.endswith(".tsv")):
                    ls_mtx.append(k)
                    ls_mtx_all.append(k)
                else:
                    pass
            
            if len(ls_mtx) == 0:
                continue
            else:
                for m in ls_mtx:
                    df = pd.read_csv(os.path.join(path_ses, m),
                                     sep="\t")

                    if len(df) == 2:
                        # MTX, Language #1
                        mask_1 = df["order"] == 1
                        df_1 = df[mask_1].reset_index(drop=True)
                        action_1 = mtx.plot_mtx(result_path, df_1,
                                                m, 1)
                        if action_1 is True:
                            counter = counter + 1
                        else:
                            save_error = save_error + 1
                   
                        # MTX, Language #2
                        mask_2 = df["order"] == 2
                        df_2 = df[mask_2].reset_index(drop=True)
                        action_2 = mtx.plot_mtx(result_path, df_2,
                                                m, 2)
                        if action_2 is True:
                            counter = counter + 1
                        else:
                            save_error = save_error + 1

                    elif len(df) == 1:
                        # MTX, Language #1
                        mask_1 = df["order"] == 1
                        df_1 = df[mask_1].reset_index(drop=True)
                        action_1 = mtx.plot_mtx(result_path, df_1,
                                                m, 1)
                        if action_1 is True:
                            counter = counter + 1
                        else:
                            save_error = save_error + 1                        

                    #print(df, "\n", df_1, "\n", df_2, "\n")
        
        #TO BE ADDED: all tests graph generation
        ls_mtx_all.sort()
        #print(ls_mtx_all)

    return counter, save_error

###############################################################################

#    data_mtx_L1 = master_data[ls_columns_common + ls_columns_MTX1]

#    data_mtx_L2 = master_data[ls_columns_common + ls_columns_MTX2]

#    # Elimination of the lines that are irrelevant to each of the tests:
#    # Matrix speech perception test
#    # L1
#    data_mtx_L1 = eliminate_row_mtx(data_mtx_L1, 1)

#    # L2
#    data_mtx_L2 = eliminate_row_mtx(data_mtx_L2, 2)

#    # MTX, L1
#    for m in range(0, len(data_mtx_L1)):
#        action_m = mtx.plot_mtx(result_path, data_mtx_L1.loc[[m]], "L1")
#        if action_m is True:
#            counter = counter + 1
#        else:
#            save_error = save_error + 1

#    # MTX, L2
#    for n in range(0, len(data_mtx_L2)):
#        df_line = data_mtx_L2.loc[[n]]

#        # Participant Sub-06 can't do the second language test
#        if df_line["Participant_ID"][n] == "Sub06":
#            continue
#        else:
#            action_n = mtx.plot_mtx(result_path, data_mtx_L2.loc[[n]], "L2")
#            if action_n is True:
#                counter = counter + 1
#            else:
#                save_error = save_error + 1

#    # MTX, L1, All results for one participant in one graph
#    for p in subjects:
#        one_subject = gf.extract_subject(data_mtx_L1, p)
#        action_p = mtx.plot_mtx_subject(result_path, one_subject, "L1")
#        if action_p is True:
#            counter = counter + 1
#        else:
#            save_error = save_error + 1

#    # MTX, L2, All results for one participant in one graph
#    for q in subjects:
#        if q == "Sub06":
#            continue
#        else:
#            one_subject = gf.extract_subject(data_mtx_L2, q)
#            action_q = mtx.plot_mtx_subject(result_path, one_subject, "L2")
#            if action_q is True:
#                counter = counter + 1
#            else:
#                save_error = save_error + 1

#    return counter, save_error


def teoae_graph(result_path, counter, save_error):
    """
    This function generates and save the TEOAE test figures
    INPUTS:
    -result_path: path to the results folder [repo_root]/results/
    -counter: variable tracking the amount of files produced by the script
    -save_error: variable tracking the amount of files that were not
                 properly saved
    OUTPUTS:
    -returns an updated value for the saved files counter and the save_error
     counter as well as the saved figures
    """

    print("Generating TEOAE graphs...\n")
    data_path = os.path.join(result_path, "BIDS_data")

    # extract the list of subject folders        
    ls_folders_sub = os.listdir(data_path)
    ls_folders_sub.sort()
    #print("sub:", ls_folders_sub, "\n")
    
    for i in ls_folders_sub:
        path_sub = os.path.join(data_path, i)

        # extract the list of session folders within a subject folder
        ls_folders_ses = os.listdir(path_sub)
        ls_folders_ses.sort()
        ls_folders_ses.pop(-1)
        ls_folders_ses.pop(-1)
        #print("ses:", ls_folders_ses, "\n")
        
        for j in ls_folders_ses:
            path_ses = os.path.join(path_sub, j)

            # extract the list of data files within a session folder
            ls_files_test = os.listdir(path_ses)
            ls_files_test.sort()
            #print("tests:", ls_files_test, "\n")
            
            ls_teoae = []
            
            for k in ls_files_test:
                if (k.find("TEOAE") != -1
                        and k.endswith(".tsv")):
                    ls_teoae.append(k)
                else:
                    pass
            
            #print(ls_teoae)
            
            if len(ls_teoae) == 0:
                continue
            else:
                for m in ls_teoae:
                    df = pd.read_csv(os.path.join(path_ses, m),
                                     sep="\t")
                    #print(df)
                    
                    # TEOAE, Right ear
                    mask_R = df["side"] == "R"
                    df_R = df[mask_R].reset_index(drop=True)
                    action_R = teoae.plot_teoae(result_path, df_R,
                                                "R", m)
                    if action_R is True:
                        counter = counter + 1
                    else:
                        save_error = save_error + 1
                   
                    # TEOAE, Left ear
                    mask_L = df["side"] == "L"
                    df_L = df[mask_L].reset_index(drop=True)
                    action_L = teoae.plot_teoae(result_path, df_L,
                                                "L", m)
                    if action_L is True:
                        counter = counter + 1
                    else:
                        save_error = save_error + 1                    
                    
                    #print(df, "\n", df_R, "\n", df_L, "\n")

    return counter, save_error


def dpoae_graph(result_path, counter, save_error):
    """
    This function generates and save the DPOAE test figures
    INPUTS:
    -result_path: path to the results folder [repo_root]/results/
    -counter: variable tracking the amount of files produced by the script
    -save_error: variable tracking the amount of files that were not
                 properly saved
    OUTPUTS:
    -returns an updated value for the saved files counter and the save_error
     counter as well as the saved figures
    """

    print("Generating DPOAE graphs...\n")
    data_path = os.path.join(result_path, "BIDS_data")

    # extract the list of subject folders
    ls_folders_sub = os.listdir(data_path)
    ls_folders_sub.sort()
    #print("sub:", ls_folders_sub, "\n")
    
    for i in ls_folders_sub:
        path_sub = os.path.join(data_path, i)

        # extract the list of session folders within a subject folder
        ls_folders_ses = os.listdir(path_sub)
        ls_folders_ses.sort()
        ls_folders_ses.pop(-1)
        ls_folders_ses.pop(-1)
        #print("ses:", ls_folders_ses, "\n")
        
        for j in ls_folders_ses:
            path_ses = os.path.join(path_sub, j)

            # extract the list of data files within a session folder
            ls_files_test = os.listdir(path_ses)
            ls_files_test.sort()
            #print("tests:", ls_files_test, "\n")
            
            ls_dpoae = []
            
            for k in ls_files_test:
                if (k.find("DPOAE") != -1
                        and k.endswith(".tsv")):
                    ls_dpoae.append(k)
                else:
                    pass
            
            #print(ls_dpoae)
            
            if len(ls_dpoae) == 0:
                continue
            else:
                for m in ls_dpoae:
                    df = pd.read_csv(os.path.join(path_ses, m),
                                     sep="\t")
                    #print(df)
                    
                    # DPOAE, Right ear
                    mask_R = df["side"] == "R"
                    df_R = df[mask_R].reset_index(drop=True)
                    action_R = dpoae.plot_dpoae(result_path, df_R,
                                                "R", m)
                    if action_R is True:
                        counter = counter + 1
                    else:
                        save_error = save_error + 1
                  
                    # DPOAE, Left ear
                    mask_L = df["side"] == "L"
                    df_L = df[mask_L].reset_index(drop=True)
                    action_L = dpoae.plot_dpoae(result_path, df_L,
                                                "L", m)
                    if action_L is True:
                        counter = counter + 1
                    else:
                        save_error = save_error + 1                    
                    
                    #print(df, "\n", df_R, "\n", df_L, "\n")

    return counter, save_error 


def growth_graph(result_path, counter, save_error):
    """
    This function generates and save the DP Growth test figures
    INPUTS:
    -result_path: path to the results folder [repo_root]/results/
    -counter: variable tracking the amount of files produced by the script
    -save_error: variable tracking the amount of files that were not
                 properly saved
    OUTPUTS:
    -returns an updated value for the saved files counter and the save_error
     counter as well as the saved figures
    """

    print("Generating Growth function graphs...\n")
    data_path = os.path.join(result_path, "BIDS_data")
        
    # extract the list of subject folders
    ls_folders_sub = os.listdir(data_path)
    ls_folders_sub.sort()
    #print("sub:", ls_folders_sub, "\n")
    
    for i in ls_folders_sub:
        path_sub = os.path.join(data_path, i)

        # extract the list of session folders within a subject folder
        ls_folders_ses = os.listdir(path_sub)
        ls_folders_ses.sort()
        ls_folders_ses.pop(-1)
        ls_folders_ses.pop(-1)
        #print("ses:", ls_folders_ses, "\n")
        
        for j in ls_folders_ses:
            path_ses = os.path.join(path_sub, j)

            # extract the list of data files within a session folder
            ls_files_test = os.listdir(path_ses)
            ls_files_test.sort()
            #print("tests:", ls_files_test, "\n")
            
            ls_growth = []
            
            for k in ls_files_test:
                if (k.find("DPGrowth") != -1
                        and k.endswith(".tsv")):
                    ls_growth.append(k)
                else:
                    pass
            
            #print(ls_growth)
            
            if len(ls_growth) == 0:
                continue
            else:
                for m in ls_growth:
                    df = pd.read_csv(os.path.join(path_ses, m),
                                     sep="\t")
                    #print(df)
                    
                    # DP Growth, Right ear
                    mask_R = df["side"] == "R"
                    df_R = df[mask_R].reset_index(drop=True)
                    action_R = growth.plot_growth(result_path, df_R,
                                                  "R", m)
                    if action_R is True:
                        counter = counter + 1
                    else:
                        save_error = save_error + 1
                    
                    # DP Growth, Left ear
                    mask_L = df["side"] == "L"
                    df_L = df[mask_L].reset_index(drop=True)
                    action_L = growth.plot_growth(result_path, df_L,
                                                  "L", m)
                    if action_L is True:
                        counter = counter + 1
                    else:
                        save_error = save_error + 1                    
                    
                    #print(df, "\n", df_R, "\n", df_L, "\n")

    return counter, save_error 


def master_run(root_path, test_type="all"):
    result_path = os.path.join(root_path, "results")
    data_path = os.path.join(root_path, "data")
    
    #master_data = common.retrieve_db(data_path)
    
    # Verifications:
    # - existence of the "graphs" folder
    # - existence of the subjects' sub-folders
    # If not, creates them.
    gf.result_location(result_path, subjects)

    # Counter initialisation to keep track of the amount of files generated
    counter = 0
    save_error = 0

    if test_type == "PTA":
        counter, save_error = pta_graph(result_path,
                                        counter,
                                        save_error)

    elif test_type == "MTX":
        counter, save_error = mtx_graph(result_path,
                                        counter,
                                        save_error)

    elif test_type == "TEOAE":
        counter, save_error = teoae_graph(result_path,
                                          counter,
                                          save_error)

    elif test_type == "DPOAE":
        counter, save_error = dpoae_graph(result_path,
                                          counter,
                                          save_error)

    elif test_type == "Growth":
        counter, save_error = growth_graph(result_path,
                                           counter,
                                           save_error)

    elif test_type == "all":
        x1, y1 = pta_graph(result_path, counter, save_error)
        x2, y2 = mtx_graph(result_path, counter, save_error)
        x3, y3 = teoae_graph(result_path, counter, save_error)
        x4, y4 = dpoae_graph(result_path, counter, save_error)
        x5, y5 = growth_graph(result_path, counter, save_error)
        counter = x1 + x2 + x3 + x4 + x5
        save_error = y1 + y2 + y3 + y4 + y5

    # Return a feedback to the user regarding the number of files created
    if counter <= 1:
        print(counter, "file was saved.")
        print(save_error, "file(s) was/were not properly saved")
    else:
        print(counter, "files were saved.")
        print(save_error, "file(s) was/were not properly saved")


if __name__ == "__main__":
    master_run("..")

else:
    pass
