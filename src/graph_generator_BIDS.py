import os
import pandas as pd
#from src import BIDS_utils as utils
from src import graph_functions as gf
from src import graph_PTA_BIDS as pta
from src import graph_MTX_BIDS as mtx
from src import graph_TEOAE_BIDS as teoae
from src import graph_DPOAE_BIDS as dpoae
from src import graph_DPGrowth_BIDS as growth


subjects = ["sub-01", "sub-02", "sub-03", "sub-04", "sub-05", "sub-06"]


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

    for i in ls_folders_sub:
        path_i = os.path.join(data_path, i)
        
        if os.path.isdir(path_i):
            path_sub = path_i
            
            # extract the list of session folders within a subject folder
            ls_folders_ses = os.listdir(path_sub)
            ls_folders_ses.sort()
            ls_folders_ses.pop(-1)
            ls_folders_ses.pop(-1)
            
            for j in ls_folders_ses:
                path_ses = os.path.join(path_sub, j)

                # extract the list of data files within a session folder
                ls_files_test = os.listdir(path_ses)
                ls_files_test.sort()

                ls_pta = []

                for k in ls_files_test:
                    if (k.find("PTA") != -1
                            and k.endswith(".tsv")):
                        ls_pta.append(k)
                    else:
                        pass

                if len(ls_pta) == 0:
                    continue
                else:
                    for m in ls_pta:
                        df = pd.read_csv(os.path.join(path_ses, m),
                                         sep="\t")

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

        else:
            continue
                    
    return counter, save_error


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
        path_i = os.path.join(data_path, i)

        if os.path.isdir(path_i):
            path_sub = path_i

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

        else:
            continue

    return counter, save_error


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
        path_i = os.path.join(data_path, i)
        
        if os.path.isdir(path_i):
            path_sub = path_i

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
        else:
            continue

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
        path_i = os.path.join(data_path, i)
        
        if os.path.isdir(path_i):
            path_sub = path_i

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

                if len(ls_dpoae) == 0:
                    continue
                else:
                    for m in ls_dpoae:
                        df = pd.read_csv(os.path.join(path_ses, m),
                                         sep="\t")

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
        else:
            continue
                    
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
        path_i = os.path.join(data_path, i)
        
        if os.path.isdir(path_i):
            path_sub = path_i

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
        else:
            continue

    return counter, save_error 


def master_run(root_path, test_type="all"):
    result_path = os.path.join(root_path, "results")
    
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
