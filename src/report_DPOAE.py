import os
import pandas as pd
import statistics as stats
from src import report_common as common


def fct_1(result_path):
    # path to the BIDS formated dataset
    bids_path = os.path.join(result_path, "BIDS_data")

    # Content of the BIDS dataset: list of the subject folders
    try:
        os.listdir(bids_path)

    except FileNotFoundError:
        print("\nThe BIDS dataset folder is missing. Please verify that "
              "the folder is correctly located "
              "([repo_root]/results/BIDS_data/) or use the BIDS dataset "
              "formating function to regenarate the dataset.\n")
        exit()

    else:
        sub = os.listdir(bids_path)

    sub.sort()

    # Verification/Creation of the reports folder
    path_reports = common.report_file_verif(result_path)

    for i in sub:
        #print("\n")
        #print(i)
        # path inside the subject's folder
        path_ses = os.path.join(bids_path, i)

        # content of the subject's folder (sessions + reference .tsv file)
        ls_ses = os.listdir(path_ses)
        ls_ses.sort()
        #print(ls_ses)

        # retrieve the reference .tsv file
        filename_index = ls_ses.index(i + "_sessions.tsv")
        ref_filename = ls_ses.pop(filename_index)
        ref_df = pd.read_csv(os.path.join(path_ses, ref_filename), sep="\t")

        # extract reference data: ses-02 (Baseline #2)
        ses_baseline = ref_df.at[1, "session_id"]
        # path inside the baseline #2 folder
        path_base_ses = os.path.join(path_ses, ses_baseline)

        ls_folder_baseline = os.listdir(path_base_ses)

        for a in ls_folder_baseline:
            if a.find("DPOAE") != -1 and a.endswith(".tsv"):
                baseline_ref = a
            else:
                pass

        # path to the baseline #2 DPOAE data file
        filepath_ref = os.path.join(path_base_ses, baseline_ref)
        #print(filepath_ref)
        df_ref = pd.read_csv(filepath_ref, sep="\t", na_filter=False)
        #print(df_ref)

        # extract list of pre/post and 48h post scan session IDs
        ls_48 = []
        ls_prepost = []
        for b in range(0, len(ref_df)):
            prepost = []
            init_cond = ref_df.at[b, "condition"]

            if init_cond.startswith("Condition 3A"):
                prepost.append(ref_df.at[b, "session_id"])

                follow_ses = ref_df.at[b + 1, "session_id"]
                follow_cond = ref_df.at[b + 1, "condition"]

                if follow_cond.startswith("Condition 3B"):
                    prepost.append(follow_ses)
                    ls_prepost.append(prepost)
                    b += 1
                else:
                    print(f"MISSING SESSION ERROR:\nThe {follow_ses} session "
                          f"for {i} presents the following condition: "
                          f"{follow_cond}. Instead, it should be: Condition "
                          f"3B (right after the scan).\n")

            elif init_cond.startswith("Condition 2"):
                ls_48.append(ref_df.at[b, "session_id"])

        # extract the dataframes for each of the pre/post pairs
        for c in ls_prepost:
            #print("\n")
            #print(c)
            # path inside the prescan session folder
            path_pre = os.path.join(path_ses, c[0])
            #print(path_pre)
            # path inside the postscan session folder
            path_post = os.path.join(path_ses, c[1])

            file_ls_pre = os.listdir(path_pre)
            file_ls_pre.sort()
            file_ls_post = os.listdir(path_post)
            file_ls_post.sort()
            #print(file_ls_pre)

            for p in file_ls_pre:
                if p.find("DPOAE") != -1 and p.endswith(".tsv"):
                    file_pre = os.path.join(path_pre, p)
                else:
                    pass

            for q in file_ls_post:
                if q.find("DPOAE") != -1 and q.endswith(".tsv"):
                    file_post = os.path.join(path_post, q)
                else:
                    pass

            #print(file_ls_pre, "\n")
            #print(file_ls_post, "\n")
            #print(file_pre)
            #print(file_post)

#            ls_df_pre = []
#            for r in file_ls_pre:
#                # path to each of the prescan session tsv files
#                tsv_filepath = os.path.join(path_pre, r)
            df_pre = pd.read_csv(file_pre,
                                 sep="\t",
                                 na_filter=False)
                
#                if dpoae_df["freq2"][0] == 2002:
#                    df_pre2 = dpoae_df
#                    ls_df_pre.append(df_pre2)
#                elif dpoae_df["freq2"][0] == 4004:
#                    df_pre4 = dpoae_df
#                    ls_df_pre.append(df_pre4)
#                elif dpoae_df["freq2"][0] == 6006:
#                    df_pre6 = dpoae_df
#                    ls_df_pre.append(df_pre6)

#            ls_df_post = []
#            for s in file_ls_post:
#                # path to each of the postscan session tsv files
#                tsv_filepath = os.path.join(path_post, s)
            df_post = pd.read_csv(file_post,
                                  sep="\t",
                                  na_filter=False)
                
#                if growth_df["freq2"][0] == 2002:
#                    df_post2 = growth_df
#                    ls_df_post.append(df_post2)
#                elif growth_df["freq2"][0] == 4004:
#                    df_post4 = growth_df
#                    ls_df_post.append(df_post4)
#                elif growth_df["freq2"][0] == 6006:
#                    df_post6 = growth_df
#                    ls_df_post.append(df_post6)

#            print(ls_df_pre)
#            print(ls_df_post)
#            #mega_ls = []

#            ls_diff_2L = []
#            ls_diff_2R = []
#            ls_diff_4L = []
#            ls_diff_4R = []
#            ls_diff_6L = []
#            ls_diff_6R = []
            ls_diff_R = []
            ls_diff_L = []
            ls_f2 = []
            
            for t in range(0, len(df_pre)):
                value = df_post.at[t, "dp"] - df_pre.at[t, "dp"]
                
                if df_pre.at[t, "side"] == "R":
                    ls_diff_R.append(value)
                elif df_pre.at[t, "side"] == "L":
                    ls_diff_L.append(value)

                if df_pre.at[t, "freq2"] in ls_f2:
                    pass
                else:
                    ls_f2.append(df_pre.at[t, "freq2"])
            
            ls_f2.append("Mean")
            ls_f2.append("Standard Deviation")
            #print(len(ls_diff_R))
            #print(len(ls_diff_L))
            #print(ls_f2)

#                for x in range(0, len(ls_df_pre[t])):
#                    value = (ls_df_post[t].at[x, "dp"]
#                             - ls_df_pre[t].at[x, "dp"])

#                    if ls_df_pre[t].at[x, "freq2"] == 2002:
#                        if ls_df_pre[t].at[x, "side"] == "L":
#                            ls_diff_2L.append(value)
#                        elif ls_df_pre[t].at[x, "side"] == "R":
#                            ls_diff_2R.append(value)

#                    elif ls_df_pre[t].at[x, "freq2"] == 4004:
#                        if ls_df_pre[t].at[x, "side"] == "L":
#                            ls_diff_4L.append(value)
#                        elif ls_df_pre[t].at[x, "side"] == "R":
#                            ls_diff_4R.append(value)

#                    elif ls_df_pre[t].at[x, "freq2"] == 6006:
#                        if ls_df_pre[t].at[x, "side"] == "L":
#                            ls_diff_6L.append(value)
#                        elif ls_df_pre[t].at[x, "side"] == "R":
#                            ls_diff_6R.append(value)                        

#            ls_diff = [[ls_diff_2L, ls_diff_2R],
#                       [ls_diff_4L, ls_diff_4R],
#                       [ls_diff_6L, ls_diff_6R]]
            
#            ls_diff_tag = ["2", "4", "6"]

            names_columns = ["freq2", "diff_L", "diff_R"]

#            intensity_column = [65, 60, 55, 50, 45, 40, 35,
#                                "Mean", "Standard Deviation"]

#            for u in range(0, len(ls_diff)):
            ls2df = []

#                #print(ls_diff[u])
            for y in range(0, len(ls_f2)):
                row = []
                row.append(ls_f2[y])
                try:
                    float(ls_f2[y])
                except:
                    if ls_f2[y] == "Mean":
                        row.append(stats.mean(ls_diff_L))
                        row.append(stats.mean(ls_diff_R))
                    elif ls_f2[y] == "Standard Deviation":
                        row.append(stats.pstdev(ls_diff_L))
                        row.append(stats.pstdev(ls_diff_R))
                else:
                    row.append(ls_diff_L[y])
                    row.append(ls_diff_R[y])
                ls2df.append(row)
             
            df_delta = pd.DataFrame(data=ls2df, columns=names_columns)
            #print(df_delta)

            delta_filename = (f"{i}_deltas-DPOAE_{c[0]}_{c[1]}.tsv")
            #print(name_to_save)
            delta_path = os.path.join(path_reports, delta_filename)
            df_delta.to_csv(delta_path, sep="\t", index=False)

###############################################################################

#        df_ref.drop(columns=["order", "side"], inplace=True)
#        df_ref.astype(int, copy=False, errors="ignore")

#        for e in ls_48:
#            path_48 = os.path.join(path_ses, e)

#            file_ls_48 = os.listdir(path_48)
#            file_ls_48.sort()

#            for k in file_ls_48:
#                if k.find("PTA") != -1 and k.endswith(".tsv"):
#                    print(k)
#                    file_48 = os.path.join(path_48, k)
#                else:
#                    pass

#            df_48 = pd.read_csv(file_48,
#                                sep="\t",
#                                na_filter=False)

#            df_48.drop(columns=["order", "side"], inplace=True)
#            df_48.astype(int, copy=False, errors="ignore")

#            columns = df_ref.columns

#            for m in [0, 1]:
#                ls_diff = []
#                for y in columns:
#                    if df_48.at[m, y] == "n/a":
#                        pass
#                    try:
#                        float(df_48.at[m, y])
#                    except:
#                        pass
#                    else:
#                        df_48.at[m, y] = float(df_48.at[m, y])

#                    try:
#                        float(df_ref.at[m, y])
#                    except:
#                        pass
#                    else:
#                        df_ref.at[m, y] = float(df_ref.at[m, y])

#                    if (df_48.at[m, y] == "n/a"
#                            or df_48.at[m, y] == "n/a"):
#                        value = "n/a"
#                        ls_diff.append(value)

#                    elif (df_48.at[m, y] != "No response"
#                          and df_ref.at[m, y] != "No response"):
#                        value = df_48.at[m, y] - df_ref.at[m, y]
#                        ls_diff.append(value)

#                    elif (df_48.at[m, y] == "No response"
#                          and df_ref.at[m, y] != "No response"):
#                        value_pre = df_ref.at[m, y]
#                        value = f"Post = NR ({value_pre} before scan)"
#                        ls_diff.append(value)

#                    elif (df_48.at[m, y] != "No response"
#                          and df_ref.at[m, y] == "No response"):
#                        value_post = df_48.at[m, y]
#                        value = f"Pre = NR ({value_post} after scan)"
#                        ls_diff.append(value)

#                    elif (df_48.at[m, y] == "No response"
#                          and df_ref.at[m, y] == "No response"):
#                        value = "Both = NR"
#                        ls_diff.append(value)

#                if r == 0:
#                    ls_diff_R = ls_diff
#                elif r == 1:
#                    ls_diff_L = ls_diff

#            ls_threshold = []

#            for n in ls_diff_L:
#                if n in ls_threshold:
#                    pass
#                else:
#                    try:
#                        float(n)
#                    except:
#                        pass
#                    else:
#                        ls_threshold.append(float(n))

#            for f in ls_diff_R:
#                if f in ls_threshold:
#                    pass
#                else:
#                    try:
#                        float(f)
#                    except:
#                        pass
#                    else:
#                        ls_threshold.append(float(f))

#            ls_threshold.sort()

#            data = []
#            for g in range(0, len(ls_threshold)):
#                data.append([])

#            for h in range(0, len(data)):
#                data[h].append(ls_threshold[h])
#                data[h].append([])
#                data[h].append([])
#                for j in range(0, len(ls_diff_L)):
#                    if ls_diff_L[j] == ls_threshold[h]:
#                        data[h][1].append(columns[j])
#                    else:
#                        pass
#                for w in range(0, len(ls_diff_R)):
#                    if ls_diff_R[w] == ls_threshold[h]:
#                        data[h][2].append(columns[w])
#                    else:
#                        pass

#            names_columns = ["48post-baseline_diff", "freq_L", "freq_R"]
#            df_data = pd.DataFrame(data=data, columns=names_columns)

#            name_to_save = f"{i}_report-PTA_Baseline2_{e}.tsv"
#            path_to_save = os.path.join(path_reports, name_to_save)
#            df_data.to_csv(path_to_save, sep="\t")


fct_1(os.path.join("..", "results"))
