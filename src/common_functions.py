import os
import pandas as pd

if __name__ == "__main__":
    print("This script is not designed to be used as a standalone script.")

else:
    def retrieve_db(data_path):
        """
        This function gives the user a choice on how to retrieve the database.
        Available options are:
            -> The user supplies a URL to a properly formated
               Google Spreadsheet
            -> The user provides the URL in the URL.tsv file in the data folder
            -> The user provides a properly formated database in an .xlsx file
               in the data folder
        INPUTS:
        -data_path: path to the [repo_root]/data folder
        OUTPUTS:
        -returns the database in a pandas dataframe
        """

        # Available functions list
        ls_fct = ["Retrieve from a user supplied URL (Google Spreadsheet)",
                  "Use the URL listed in the [repo_root]/data/URL.tsv file",
                  "Retrieve from the [repo_root]/data/test_database.xlsx file"]

        # Prompt text generation
        prompt_instruction = ("Please specify the database retrieval "
                              "method you want to use:")

        prompt_options = ""

        for i in range(0, len(ls_fct)):
            prompt_options += ("\n " + str(i+1) + "-" + ls_fct[i])

        prompt_options += ("\n")

        prompt_txt = prompt_instruction + prompt_options

        # While loop condition initialization
        loop_value = True

        # function selection prompt
        while loop_value:

            value = input(prompt_txt)
            print("\n")

            # Value validity verification
            # Is it a valid number?
            if value.isdigit():
                value = int(value)

                # Is it within the range of the options?
                if value > 0 and value <= len(ls_fct):

                    # The encased section contains the subscript calls.
                    # If functionality are to be added, here is where to
                    # add them(Don't forget to also add them to the list
                    # of available functions: ls_fct).
                    ###########################################################

                    # User is to supply a URL
                    if ls_fct[value - 1].count("user supplied URL") == 1:
                        url_share = input("Enter the Google Spreadsheet URL: ")
                        print("\n")
                        url_csv = url_share.replace("/edit#gid=",
                                                    "/export?format=csv&gid=")
                        df = pd.read_csv(url_csv, sep=',', na_filter=True)
                        return df

                    # Use the URL.tsv file
                    elif ls_fct[value - 1].count("URL.tsv") == 1:
                        filename = os.path.join(data_path, "URL.tsv")
                        df_URL = pd.read_csv(filename, sep="\t")
                        url_share = df_URL["test_database"][0]
                        url_csv = url_share.replace("/edit#gid=",
                                                    "/export?format=csv&gid=")
                        df = pd.read_csv(url_csv, sep=',', na_filter=True)
                        return df

                    # MRI sessions design files generation functionalities
                    elif ls_fct[value - 1].count("test_database.xlsx") == 1:
                        filename = os.path.join(data_path,
                                                "test_database.xlsx")
                        df = pd.read_excel(filename, na_filter=True)
                        print(df)
                        return df

                    # Test Dummy
                    elif ls_fct[value - 1].count("Dummy") == 1:
                        print("This is just a test line:",
                              ls_fct[value - 1], "\n")

                    ###########################################################

                else:
                    # If it is not within range, restart the loop
                    print("The provided value is not valid (out of bound).\n")
                    continue

            else:
                # If it is not a number, restart the loop
                print("The provided value is not valid (not a digit).\n")
                continue

    def create_folder_subjects(subject, parent_path):
        """This function creates by-subject folders in a specified folder
        INPUTS:
        -subject: subject ID used by the script or the database's
                  dataframe (format: Sub0X)
        -parent_path: path to get inside the specified folder
        OUTPUTS:
        -folder for the provided subject ID in the BIDS_data/ folder
        -NO specific return to the script
        """

        dir_content = os.listdir(parent_path)
        dir_content.sort()
        sub_ID = subject.lstrip("Sub")

        if dir_content.count(f"sub-{sub_ID}") == 1:
            print(f"The subject's subfolder for sub-{sub_ID} is present.\n")
        else:
            os.mkdir(os.path.join(parent_path, f"sub-{sub_ID}"))
            print(f"The subject's subfolder for sub-{sub_ID} was created.\n")
