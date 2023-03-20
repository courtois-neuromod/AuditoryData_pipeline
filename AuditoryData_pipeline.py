import os
import colorama as color

from src import report_PTA
from src import report_MTX
from src import report_DPOAE as report_DP
from src import report_DPGrowth as report_DPGr

from src import BIDS_formater as formater
from src import json_sidecar_generator as jsg
from src import MRI_session_design_generator as ses_design
from src import graph_generator_BIDS as graph


# Initialize colorama
color.init(autoreset=True)

# Available functions list
ls_fct = ["BIDS format's json sidecars creation",
          "BIDS format's auditory data exporter",
          "Pure Tone Audiometry interactive graph generator",
          "Matrix Speech-in-Noise Test interactive graph generator",
          "Transient-evoked OAE test graph generator",
          "Distortion product OAE test graph generator",
          "Distortion product growth function test graph generator",
          "Pure Tone Audiometry report generator",
          "Matrix Speech-in-Noise Test report generator",
          "Distortion product OAE report generator",
          "Distortion product growth function report generator",
          "MRI session design files generator (in development)",
          # "Dummy line",
          ]

# Prompt text generation
prompt_instruction = (color.Style.BRIGHT
                      + "Please enter the number of the pipeline "
                        "functionality you want to run:"
                      + color.Style.RESET_ALL)

prompt_options = ""

for i in range(0, len(ls_fct)):
    prompt_options += ("\n " + str(i+1) + "-" + ls_fct[i])

prompt_options += ("\n " + str(len(ls_fct)+1) + "-Exit\n")

prompt_txt = prompt_instruction + prompt_options

# While loop condition initialization
loop_value = True

# Show welcome message
print(color.Style.BRIGHT
      + color.Fore.YELLOW
      + "\nWelcome to the AuditoryData_pipeline.\n")

# function selection prompt
while loop_value:

    # Show options and save the user selection
    value = input(prompt_txt)
    print("\n")

    try:
        # Value validity verification
        # Is it a valid number?
        if value.isdigit():
            value = int(value)

            # Is it within the range of the options?
            if value > 0 and value <= len(ls_fct) + 1:

                # Loop breaks if the "Exit" option is selected
                if value == len(ls_fct) + 1:
                    break

    # The encased section contains the subscript calls.
    # If functionality are to be added, here is where to add them.
    # (Don't forget to also add them to the list of available functions:
    # ls_fct)
    ###########################################################################

                else:

                    # BIDS format functionalities
                    if ls_fct[value - 1].count("BIDS") == 1:

                        # json sidecar files generation
                        if ls_fct[value - 1] == ("BIDS format's json sidecars "
                                                 "creation"):
                            jsg.create_sidecars(os.path.join(".", "results"))
                            print("\n")

                        # BIDS compatible dataset formating
                        elif ls_fct[value - 1] == ("BIDS format's auditory "
                                                   "data exporter"):
                            formater.master_run(os.path.join(".", "data"),
                                                os.path.join(".", "results"))
                            print("\n")

                    # Graph generation functionalities
                    elif ls_fct[value - 1].count("graph") == 1:

                        # PTA graph plotting
                        if ls_fct[value - 1].count("Pure Tone") == 1:
                            graph.master_run(".", "PTA")
                            print("\n")

                        # MTX graph plotting
                        elif ls_fct[value - 1].count("Matrix") == 1:
                            graph.master_run(".", "MTX")
                            print("\n")

                        # TEOAE graph plotting
                        elif ls_fct[value - 1].count("Transient") == 1:
                            graph.master_run(".", "TEOAE")
                            print("\n")

                        # Distortion product (DPOAE and DP Growth) OAEs
                        elif ls_fct[value - 1].count("Distortion"):

                            # DPOAE graph plotting
                            if ls_fct[value - 1] == ("Distortion product OAE "
                                                     "test graph generator"):
                                graph.master_run(".", "DPOAE")
                                print("\n")

                            # DP Growth graph plotting
                            elif ls_fct[value - 1] == ("Distortion product "
                                                       "growth function test "
                                                       "graph generator"):
                                graph.master_run(".", "Growth")
                                print("\n")

                    # Report generation capabilities
                    elif ls_fct[value - 1].count("report") == 1:

                        # PTA report generation
                        if ls_fct[value - 1].count("Pure Tone") == 1:
                            report_PTA.master_run(os.path.join(".", "results"))
                            print("\n")

                        # MTX report generation
                        elif ls_fct[value - 1].count("Matrix") == 1:
                            report_MTX.master_run(os.path.join(".", "results"))
                            print("\n")

                        # Distortion product (DPOAE and DP Growth) OAEs
                        elif ls_fct[value - 1].count("Distortion"):

                            # DPOAE report generation
                            if ls_fct[value - 1] == ("Distortion product OAE "
                                                     "report generator"):
                                report_DP.master_run(os.path.join(".",
                                                                  "results"))
                                print("\n")

                            # DP Growth report generation
                            elif ls_fct[value - 1] == ("Distortion product "
                                                       "growth function "
                                                       "report generator"):
                                report_DPGr.master_run(os.path.join(".",
                                                                    "results"))
                                print("\n")

                    # MRI sessions design files generation functionalities
                    elif ls_fct[value - 1].count("design files") == 1:
                        ses_design.master_run(os.path.join(".", "data"))
                        print("\n")

                    # Test Dummy
                    elif ls_fct[value - 1].count("Dummy") == 1:
                        print("This is just a test line:",
                              ls_fct[value - 1],
                              "\n")
        
    ###########################################################################

            else:

                # If it is not within range, restart the loop
                print(color.Fore.RED
                      + "The provided value is not valid (out of bound).\n")
                continue

        else:

            # If it is not a number, restart the loop
            print(color.Fore.RED
                  + "The provided value is not valid (not a digit).\n")
            continue

    # If the submenu "Return to the main menu" option is selected
    except RuntimeError as error:
        if error.args[0] == "Return to the main menu":
            continue
        else:
            raise

# Exit message
print(color.Style.BRIGHT
      + color.Fore.YELLOW
      + "Thanks for using the AuditoryData_pipeline.\n")
