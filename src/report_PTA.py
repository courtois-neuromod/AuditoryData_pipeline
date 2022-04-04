import os
import pandas as pd


def fct_1(result_path):
    # path to the BIDS formated dataset
    bids_path = os.path.join(result_path, "BIDS_data")

    # Content of the BIDS dataset: list of the subject folders
    sub = os.listdir(bids_path)
    sub.sort()
    #print(sub)
    
    for i in sub:
        print(i)
        # path inside the subject's folder
        path_ses = os.path.join(bids_path, i)

        # content of the subject's folder (sessions + reference .tsv file)
        ls_ses = os.listdir(path_ses)
        ls_ses.sort()

        # retrieve the reference .tsv file
        filename_index = ls_ses.index(i + ".tsv")
        ref_filename = ls_ses.pop(filename_index)
        ref_df = pd.read_csv(os.path.join(path_ses, ref_filename), sep="\t")
        #print(ref_df)

        # extract reference data: ses-02 (Baseline #2)
        ses_baseline = ref_df.at[1, "session"]
        path_base_ses = os.path.join(path_ses, ses_baseline)
        ls_folder_baseline = os.listdir(path_base_ses)

        for a in ls_folder_baseline:
            if a.find("PTA") != -1 and a.endswith(".tsv"):
                baseline_ref = a
            else:
                pass
        
        filepath_ref = os.path.join(path_base_ses, baseline_ref)
        df_ref = pd.read_csv(filepath_ref, sep="\t")
        #print(df_ref)
        
        # extract list of pre/post and 48h post scan session IDs
        ls_48 = []
        ls_prepost = []
        for b in range(0, len(ref_df)):
            prepost = []
            init_cond = ref_df.at[b, "condition"]

            if init_cond.startswith("Condition 1A"):
                prepost.append(ref_df.at[b, "session"])

                follow_ses = ref_df.at[b + 1, "session"]
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
                prepost.append(ref_df.at[b, "session"])

                follow_ses = ref_df.at[b + 1, "session"]
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
                ls_48.append(ref_df.at[b, "session"])

        print(ls_prepost, ls_48)
        
        for c in ls_prepost:
            path_pre = os.path.join(path_ses, c[0])
            path_post = os.path.join(path_ses, c[1])

            file_ls_pre = os.listdir(path_pre)
            file_ls_pre.sort()
            file_ls_post = os.listdir(path_post)
            file_ls_post.sort()
            
            for p in file_ls_pre:
                if p.find("PTA") != -1 and p.endswith(".tsv"):
                    #print(p)
                    file_pre = os.path.join(path_pre, p)
                else:
                    pass

            for q in file_ls_post:
                if q.find("PTA") != -1 and q.endswith(".tsv"):
                    #print(q)
                    file_post = os.path.join(path_post, q)
                else:
                    pass

            df_pre = pd.read_csv(file_pre, sep="\t")
            df_post = pd.read_csv(file_post, sep="\t")
            
            df_pre.drop(columns=["order", "side"], inplace=True)
            df_post.drop(columns=["order", "side"], inplace=True)
            df_pre.astype(int, copy=False, errors="ignore")
            df_post.astype(int, copy=False, errors="ignore")
            #print(df_pre)
            #print(df_post)
            
            columns = df_pre.columns
            
            for r in [0, 1]:
                #print(r)
                ls_diff = []
                for x in columns:
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

#                    print(x)

#                    print(df_post.at[r, x])
#                    print(type(df_post.at[r, x]))
#                    print(df_post.at[r, x] != "No response")

#                    print(df_pre.at[r, x])
#                    print(type(df_pre.at[r, x]))
#                    print(df_pre.at[r, x] != "No response")

                    if (df_post.at[r, x] != "No response"
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
                    #print(ls_diff)
                    
                if r == 0:
                    ls_diff_R = ls_diff
                elif r == 1:
                    ls_diff_L = ls_diff
                    
            print(ls_diff_R, "\n", ls_diff_L, "\n")    

fct_1(os.path.join("..", "results"))
