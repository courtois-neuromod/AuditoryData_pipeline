import os
import pandas as pd
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
        # path inside the subject's folder
        path_ses = os.path.join(bids_path, i)

        # content of the subject's folder (sessions + reference .tsv file)
        ls_ses = os.listdir(path_ses)
        ls_ses.sort()

        # retrieve the reference .tsv file
        filename_index = ls_ses.index(i + "_sessions.tsv")
        ref_filename = ls_ses.pop(filename_index)
        ref_df = pd.read_csv(os.path.join(path_ses, ref_filename), sep="\t")

        # extract reference data: ses-02 (Baseline #2)
        ses_baseline = ref_df.at[0, "session_id"]
        path_base_ses = os.path.join(path_ses, ses_baseline)
        ls_folder_baseline = os.listdir(path_base_ses)

        for a in ls_folder_baseline:
            if a.find("PTA") != -1 and a.endswith(".tsv"):
                baseline_ref = a
            else:
                pass

        filepath_ref = os.path.join(path_base_ses, baseline_ref)
        df_ref = pd.read_csv(filepath_ref, sep="\t", na_filter=False)

        # extract list of pre/post and 48h post scan session IDs
        ls_48 = []
        ls_prepost = []
        for b in range(0, len(ref_df)):
            prepost = []
            init_cond = ref_df.at[b, "condition"]

            if init_cond.startswith("Condition 1A"):
                prepost.append(ref_df.at[b, "session_id"])

                follow_ses = ref_df.at[b + 1, "session_id"]
                follow_cond = ref_df.at[b + 1, "condition"]

                if follow_cond.startswith("Condition 1B"):
                    prepost.append(follow_ses)
                    ls_prepost.append(prepost)
                    b += 1
                else:
                    print(f"MISSING SESSION ERROR:\nThe {follow_ses} session "
                          f"for {i} presents the following condition: "
                          f"{follow_cond}. Instead, it should be: Condition "
                          f"1B (right after the scan).\n")

            elif (init_cond.startswith("Suppl.")
                  and init_cond.find("before") != -1):
                prepost.append(ref_df.at[b, "session_id"])

                follow_ses = ref_df.at[b + 1, "session_id"]
                follow_cond = ref_df.at[b + 1, "condition"]

                if (follow_cond.startswith("Suppl.")
                        and follow_cond.find("after") != -1):
                    prepost.append(follow_ses)
                    ls_prepost.append(prepost)
                    b += 1
                else:
                    print(f"MISSING SESSION ERROR:\nThe {follow_ses} session "
                          f"for {i} presents the following condition: "
                          f"{follow_cond}. Instead, it should be: Suppl. PTA "
                          f"test (right after the scan).\n")

            elif init_cond.startswith("Condition 2"):
                ls_48.append(ref_df.at[b, "session_id"])

        # Production of the reports regarding the accute phase effects
        for c in ls_prepost:
            path_pre = os.path.join(path_ses, c[0])
            path_post = os.path.join(path_ses, c[1])

            file_ls_pre = os.listdir(path_pre)
            file_ls_pre.sort()
            file_ls_post = os.listdir(path_post)
            file_ls_post.sort()

            for p in file_ls_pre:
                if p.find("PTA") != -1 and p.endswith(".tsv"):
                    file_pre = os.path.join(path_pre, p)
                else:
                    pass

            for q in file_ls_post:
                if q.find("PTA") != -1 and q.endswith(".tsv"):
                    file_post = os.path.join(path_post, q)
                else:
                    pass

            df_pre = pd.read_csv(file_pre, sep="\t", na_filter=False)
            df_post = pd.read_csv(file_post, sep="\t", na_filter=False)

            df_pre.drop(columns=["order", "side"], inplace=True)
            df_post.drop(columns=["order", "side"], inplace=True)
            df_pre.astype(int, copy=False, errors="ignore")
            df_post.astype(int, copy=False, errors="ignore")

            columns = df_pre.columns
            #print(columns)

            for r in [0, 1]:
                ls_diff = []
                ls_freq = []

                for x in columns:
                    ls_freq.append(int(x.rstrip("_hz")))
                    
                    try:
                        float(df_post.at[r, x])
                    except:
                        pass
                    else:
                        df_post.at[r, x] = float(df_post.at[r, x])

                    try:
                        float(df_pre.at[r, x])
                    except:
                        pass
                    else:
                        df_pre.at[r, x] = float(df_pre.at[r, x])

                    if (df_post.at[r, x] == "n/a"
                            or df_pre.at[r, x] == "n/a"):
                        value = "n/a"
                        ls_diff.append(value)

                    elif (df_post.at[r, x] != "No response"
                          and df_pre.at[r, x] != "No response"):
                        value = df_post.at[r, x] - df_pre.at[r, x]
                        ls_diff.append(value)

                    elif (df_post.at[r, x] == "No response"
                          and df_pre.at[r, x] != "No response"):
                        value_pre = df_pre.at[r, x]
                        value = f"Post = NR ({value_pre} before scan)"
                        ls_diff.append(value)

                    elif (df_post.at[r, x] != "No response"
                          and df_pre.at[r, x] == "No response"):
                        value_post = df_post.at[r, x]
                        value = f"Pre = NR ({value_post} after scan)"
                        ls_diff.append(value)

                    elif (df_post.at[r, x] == "No response"
                          and df_pre.at[r, x] == "No response"):
                        value = "Both = NR"
                        ls_diff.append(value)

                if r == 0:
                    ls_diff_R = ls_diff
                elif r == 1:
                    ls_diff_L = ls_diff

            #print(ls_diff_R)
            #print(ls_diff_L)
            
            ls_threshold = []

            for s in ls_diff_L:
                if s in ls_threshold:
                    pass
                else:
                    try:
                        float(s)
                    except:
                        pass
                    else:
                        ls_threshold.append(float(s))

            for t in ls_diff_R:
                if t in ls_threshold:
                    pass
                else:
                    try:
                        float(t)
                    except:
                        pass
                    else:
                        ls_threshold.append(float(t))

            ls_threshold.sort()
            #print(ls_threshold)

            data = []
            for u in range(0, len(ls_threshold)):
                data.append([])

            #print(data)
            
            for v in range(0, len(data)):
                data[v].append(ls_threshold[v])
                data[v].append([])
                data[v].append([])
                for y in range(0, len(ls_diff_L)):
                    if ls_diff_L[y] == ls_threshold[v]:
                        data[v][1].append(columns[y])
                    else:
                        pass
                for z in range(0, len(ls_diff_R)):
                    if ls_diff_R[z] == ls_threshold[v]:
                        data[v][2].append(columns[z])
                    else:
                        pass

            names_columns = ["pre-post_diff", "freq_L", "freq_R"]
            df_data = pd.DataFrame(data=data, columns=names_columns)

            name_to_save = f"{i}_report-PTA_{c[0]}_{c[1]}.tsv"
            path_to_save = os.path.join(path_reports, name_to_save)
            df_data.to_csv(path_to_save, sep="\t")
            
            #print(ls_freq)
            delta_columns = ["freq", "diff_L", "diff_R"]
#            for w in columns:
#                delta_columns.append(w)

            ls_delta = []

#            ls_delta = [["L"], ["R"]]
            for d in range(0, len(ls_freq)):
                row = []
                row.append(ls_freq[d])
                row.append(ls_diff_L[d])
                row.append(ls_diff_R[d])
#                ls_delta[0].append(ls_diff_L[d])
#                ls_delta[1].append(ls_diff_R[d])
#            #print(ls_delta)
                ls_delta.append(row)
            #print(ls_delta)
            df_delta = pd.DataFrame(data=ls_delta, columns=delta_columns)
            #df_delta.reset_index(drop=True, inplace=True)
            
            delta_filename = f"{i}_deltas-PTA_{c[0]}_{c[1]}.tsv"
            delta_path = os.path.join(path_reports, delta_filename)
            df_delta.to_csv(delta_path, sep="\t", index=False)

        # Production of the reports regarding the chronic phase effects
        df_ref.drop(columns=["order", "side"], inplace=True)
        df_ref.astype(int, copy=False, errors="ignore")

        for e in ls_48:
            #print(e)
            path_48 = os.path.join(path_ses, e)

            file_ls_48 = os.listdir(path_48)
            file_ls_48.sort()
            #print(file_ls_48)

            for k in file_ls_48:
                if k.find("PTA") != -1 and k.endswith(".tsv"):
                    file_48 = os.path.join(path_48, k)
                else:
                    pass

            #print(file_48)
            df_48 = pd.read_csv(file_48,
                                sep="\t",
                                na_filter=False)

            df_48.drop(columns=["order", "side"], inplace=True)
            df_48.astype(int, copy=False, errors="ignore")

            columns = df_ref.columns
            #print(columns)

            for m in [0, 1]:
                #print("line =", m)
                ls_diff = []
                for y in columns:
                    #print("freq =", y)
                    #if df_48.at[m, y] == "n/a":
                        #pass
                    try:
                        float(df_48.at[m, y])
                    except:
                        pass
                    else:
                        df_48.at[m, y] = float(df_48.at[m, y])

                    try:
                        float(df_ref.at[m, y])
                    except:
                        pass
                    else:
                        df_ref.at[m, y] = float(df_ref.at[m, y])

                    if (df_48.at[m, y] == "n/a"
                            or df_ref.at[m, y] == "n/a"):
                        value = "n/a"
                        ls_diff.append(value)

                    elif (df_48.at[m, y] != "No response"
                          and df_ref.at[m, y] != "No response"):
                        #print(df_48.at[m, y])
                        #print(df_ref.at[m, y])
                        value = df_48.at[m, y] - df_ref.at[m, y]
                        #print(value)
                        #print("\n")
                        ls_diff.append(value)

                    elif (df_48.at[m, y] == "No response"
                          and df_ref.at[m, y] != "No response"):
                        value_pre = df_ref.at[m, y]
                        #print("pre =", value_pre)
                        value = f"Post = NR ({value_pre} at baseline)"
                        ls_diff.append(value)

                    elif (df_48.at[m, y] != "No response"
                          and df_ref.at[m, y] == "No response"):
                        value_post = df_48.at[m, y]
                        #print("post =", value_post)
                        value = f"Pre = NR ({value_post} at exp. session)"
                        ls_diff.append(value)

                    elif (df_48.at[m, y] == "No response"
                          and df_ref.at[m, y] == "No response"):
                        value = "Both = NR"
                        #print(value)
                        ls_diff.append(value)

                #print(ls_diff)

                if m == 0:
                    ls_diff_R = ls_diff
                elif m == 1:
                    ls_diff_L = ls_diff

            #print(ls_diff_R)

            ls_threshold = []

            for n in ls_diff_L:
                if n in ls_threshold:
                    pass
                else:
                    try:
                        float(n)
                    except:
                        pass
                    else:
                        ls_threshold.append(float(n))

            for f in ls_diff_R:
                if f in ls_threshold:
                    pass
                else:
                    try:
                        float(f)
                    except:
                        pass
                    else:
                        ls_threshold.append(float(f))

            ls_threshold.sort()

            data = []
            for g in range(0, len(ls_threshold)):
                data.append([])

            for h in range(0, len(data)):
                data[h].append(ls_threshold[h])
                data[h].append([])
                data[h].append([])
                for j in range(0, len(ls_diff_L)):
                    if ls_diff_L[j] == ls_threshold[h]:
                        data[h][1].append(columns[j])
                    else:
                        pass
                for w in range(0, len(ls_diff_R)):
                    if ls_diff_R[w] == ls_threshold[h]:
                        data[h][2].append(columns[w])
                    else:
                        pass

            names_columns = ["48post-baseline_diff", "freq_L", "freq_R"]
            df_data = pd.DataFrame(data=data, columns=names_columns)

            name_to_save = f"{i}_report-PTA_Baseline1_{e}.tsv"
            path_to_save = os.path.join(path_reports, name_to_save)
            df_data.to_csv(path_to_save, sep="\t")

            #print(ls_freq)
            delta_columns_48 = ["freq", "diff_L", "diff_R"]

            ls_delta_48 = []

#            ls_delta_48 = [["L"], ["R"]]
            for d in range(0, len(ls_freq)):
                row = []
                row.append(ls_freq[d])
                row.append(ls_diff_L[d])
                row.append(ls_diff_R[d])
#                ls_delta[0].append(ls_diff_L[d])
#                ls_delta[1].append(ls_diff_R[d])
#            #print(ls_delta)
                ls_delta_48.append(row)
            #print(ls_delta_48)
            df_delta_48 = pd.DataFrame(data=ls_delta_48, columns=delta_columns)
            #print(df_delta_48)
            #df_delta.reset_index(drop=True, inplace=True)
            
            delta48_filename = f"{i}_deltas-PTA_{ses_baseline}_{e}.tsv"
            #print(delta48_filename)
            delta48_path = os.path.join(path_reports, delta48_filename)
            df_delta_48.to_csv(delta48_path, sep="\t", index=False)


fct_1(os.path.join("..", "results"))
