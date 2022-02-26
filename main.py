import os
from src import BIDS_formater as formater
from src import json_sidecar_generator as jsg
from src import MRI_session_design_generator as ses_design
from src import graph_generator as graph


# Available functions list
ls_fct = ["BIDS format's json sidecars (test level) creation",
          "BIDS format's auditory data exporter",
          "Pure-Tone Audiometry graph generator",
          "Matrix Speech-in-Noise Test graph generator",
          "Transient-evoked OAE test graph generator",
          "Distortion product OAE test graph generator",
          "Distortion product growth function test graph generator",
          "MRI session design files generator"]

# Prompt text generation
print("\nWelcome to the AuditoryData_pipeline.\n")
prompt_instruction = ("Please enter the number of the pipeline "
                      "functionality you want to run:")

prompt_options = ""

for i in range(0, len(ls_fct)):
    prompt_options += ("\n " + str(i+1) + "-" + ls_fct[i])

prompt_options += ("\n " + str(len(ls_fct)+1) + "-Exit\n")

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
        if value > 0 and value <= len(ls_fct) + 1:

            # Loop breaks if the "Exit" option is selected
            if value == len(ls_fct) + 1:
                break

# The encased section contains the subscript calls.
# If functionality are to be added, here is where to add them.
# (Don't forget to also add them to the list of available functions: ls_fct)
###############################################################################

            else:

                # BIDS format functionalities
                if ls_fct[value - 1].count("BIDS") == 1:

                    if ls_fct[value - 1] == ("BIDS format's json sidecars "
                                             "(test level) creation"):
                        jsg.create_sidecars(os.path.join(".", "results")
                        print("\n")

                    elif ls_fct[value - 1] == ("BIDS format's auditory "
                                               "data exporter"):
                        formater.master_run(os.path.join(".", "results")
                        print("\n")

                # Graph generation functionalities
                elif ls_fct[value - 1].count("graph") == 1:

                    # PTA graph plotting
                    if ls_fct[value - 1].count("Pure-Tone") == 1:
                        graph.master_run(os.path.join(".", "results"), "PTA")
                        print("\n")

                    # MTX graph plotting
                    elif ls_fct[value - 1].count("Matrix") == 1:
                        graph.master_run(os.path.join(".", "results"), "MTX")
                        print("\n")

                    # TEOAE graph plotting
                    elif ls_fct[value - 1].count("Transient") == 1:
                        print("TEOAE graph: This functionality is not "
                              "supported yet but will be added soon.\n")
                        # TEOAE graph plotting functionalities
                        print("\n")
                    
                    elif ls_fct[value - 1].count("Distortion"):
                        
                        # DPOAE graph plotting
                        if ls_fct[value - 1] == ("Distortion product OAE "
                                                 "test graph generator"):
                            print("DPOAE graph: This functionality is not "
                                  "supported yet but will be added soon.\n")
                            # DPOAE graph plotting functionalities
                            print("\n")
                        
                        # DP Growth graph plotting
                        elif ls_fct[value - 1] == ("Distortion product "
                                                   "growth function test "
                                                   "graph generator"):
                            print("DP growth graph: This functionality is not "
                                  "supported yet but will be added soon.\n")
                            # DP growth graph plotting functionalities
                            print("\n")
                            

                # MRI sessions design files generation functionalities
                elif ls_fct[value - 1].count("design files") == 1:
                    ses_design.master_run(os.path.join(".", "data")
                    print("\n")

                # Test Dummy
                elif ls_fct[value - 1].count("Dummy") == 1:
                    print("This is just a test line:", ls_fct[value - 1], "\n")

###############################################################################

        else:

            # If it is not within range, restart the loop
            print("The provided value is not valid (out of bound).")
            continue

    else:

        # If it is not a number, restart the loop
        print("The provided value is not valid (not a digit).")
        continue

# Exit message
print("Thanks for using the AuditoryData_pipeline.\n")
