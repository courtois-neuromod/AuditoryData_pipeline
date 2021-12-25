import os


# Available functions list
ls_fct = ["Pure-Tone Audiometry graph generator",
          "Matrix Speech-in-Noise Test graph generator",
          "BIDS format's json sidecars (test level)",
          "BIDS format's auditory data exporter"]

# Prompt text generation          
prompt_instruction = ("Please enter the number of the pipeline " +
                      "functionality you want to run:")

prompt_options = ""

for i in range(0, len(ls_fct)):
    prompt_options += ("\n " + str(i+1) + "-" + ls_fct[i])

prompt_options += ("\n " + str(len(ls_fct)+1) + "-Exit")

prompt_txt = prompt_instruction + prompt_options

# While loop condition initialization
loop_value = True

# function selection prompt
while loop_value:
    
    value = input(prompt_txt)

    # Value validity verification
    # Is it a number?
    if value.isdigit():
        value = int(value)

        # Is it within the range of the options?
        if value > 0 and value <= len(ls_fct) + 1:
#            print("value range = OK")

            if value == 5:
#                loop_value = False
                break

##########################
            else:
                print("!= 5 == True")
##########################
        else:
            #If it is not within range, restart the loop
            print("The provided value is not valid (out of bound).")
            continue
    else:
        # If it is not a number, restart the loop
        print("The provided value is not valid (not a digit).")
        continue
        
print("Thanks for using the AuditoryData_pipeline")
