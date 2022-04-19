import os

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
