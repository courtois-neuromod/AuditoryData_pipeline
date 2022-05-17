import os
import colorama as color

def report_file_verif(result_path):
    """
    This function verifies if the reports folder exists
    ([repo_root]/results/reports). If not, it creates it.
    INPUTS:
    -result_path: path to the result folder ([repo_root]/results/)
    OUTPUTS:
    -returns the path in the results folder ([repo_root]/results/reports/)
    """
    
    results_dir = os.listdir(result_path)

    if "reports" in results_dir:
        pass
    else:
        os.mkdir(os.path.join(result_path, "reports"))

    path_reports = os.path.join(result_path, "reports")
    
    return path_reports


def extract_ses_ls(ref_df, sub, test_type):
    """
    This function takes a [sub ID]_sessions.tsv file to generate lists of
    sessions corresponding to specific experimental conditions
    INPUTS:
    -ref_df: a dataframe extracted from a [sub ID]_sessions.tsv file
    -sub: subject ID
    -test_type: variable to keep track of the experimental conditions of
                interest depending on the type of test data processed by
                the report script
    OUTPUTS:
    -returns two lists: -one with the pre/post session couples
                        -one with the [48h, 7 days] post sessions
    """

    ls_prepost = []
    ls_48 = []

    for i in range(0, len(ref_df)):
        prepost = []
        init_cond = ref_df.at[i, "condition"]

        # Verification for the [48h, 7 days] condition
        if init_cond.startswith("Condition 2"):
            ls_48.append(ref_df.at[i, "session_id"])

        # Verification for pre/post conditions: PTA
        elif test_type == "PTA":
            if init_cond.startswith("Condition 1A"):
                prepost.append(ref_df.at[i, "session_id"])

                follow_ses = ref_df.at[i + 1, "session_id"]
                follow_cond = ref_df.at[i + 1, "condition"]

                if follow_cond.startswith("Condition 1B"):
                    prepost.append(follow_ses)
                    ls_prepost.append(prepost)
                    i += 1
                else:
                    print(color.Fore.RED
                          + (f"MISSING SESSION ERROR:\nThe {follow_ses} "
                             f"session for {sub} presents the following "
                             f"condition: {follow_cond}. Instead, it should "
                             f"be: Condition 1B (right after the scan).\n"))

            elif (init_cond.startswith("Suppl.")
                  and init_cond.find("before") != -1):
                prepost.append(ref_df.at[i, "session_id"])

                follow_ses = ref_df.at[i + 1, "session_id"]
                follow_cond = ref_df.at[i + 1, "condition"]

                if (follow_cond.startswith("Suppl.")
                        and follow_cond.find("after") != -1):
                    prepost.append(follow_ses)
                    ls_prepost.append(prepost)
                    i += 1
                else:
                    print(color.Fore.RED
                          + (f"MISSING SESSION ERROR:\nThe {follow_ses} "
                             f"session for {sub} presents the following "
                             f"condition: {follow_cond}. Instead, it should "
                             f"be: Suppl. PTA test (right after the scan).\n"))

        # Verification for pre/post conditions: OAE
        elif test_type == "OAE":
            if init_cond.startswith("Condition 3A"):
                prepost.append(ref_df.at[i, "session_id"])

                follow_ses = ref_df.at[i + 1, "session_id"]
                follow_cond = ref_df.at[i + 1, "condition"]

                if follow_cond.startswith("Condition 3B"):
                    prepost.append(follow_ses)
                    ls_prepost.append(prepost)
                    i += 1
                else:
                    print(color.Fore.RED
                          + (f"MISSING SESSION ERROR:\nThe {follow_ses} "
                             f"session for {sub} presents the following "
                             f"condition: {follow_cond}. Instead, it should "
                             f"be: Condition 3B (right after the scan).\n"))

    return ls_prepost, ls_48
