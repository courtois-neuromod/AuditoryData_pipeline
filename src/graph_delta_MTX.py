import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Create a dataframe with values for the categorical variable "x"
x_ticks = pd.DataFrame(["Noise: Left\nSpeech: Left",
                        "Noise: Binaural\nSpeech: Left",
                        "Noise: Binaural\nSpeech: Binaural",
                        "Noise: Binaural\nSpeech: Right",
                        "Noise: Right\nSpeech: Right"],
                       columns=["x_ticks"])

dict_x_ticks = {"sp_bin_no_bin": "Noise: Binaural\nSpeech: Binaural",
                "sp_l_no_bin": "Noise: Binaural\nSpeech: Left",
                "sp_r_no_bin": "Noise: Binaural\nSpeech: Right",
                "sp_l_no_l": "Noise: Left\nSpeech: Left",
                "sp_r_no_r": "Noise: Right\nSpeech: Right"}

print(dict_x_ticks)

def trace_list(report_path, sub):
    """
    This function [...]
    INPUTS:
    -report_path: 
    -sub:
    OUTPUTS:
    -returns [...]
    """

    path = os.path.join(report_path, sub)

    ls_doc = os.listdir(path)
    
    ls = []
    for i in ls_doc:
        if (i.startswith(sub)
                and i.find("report") != -1
                and i.find("MTX") != -1):
            ls.append(i)
        else:
            pass
    
    ls.sort()
    
    return ls


#def file_name(sub, ear):
#    """
#    This function [...]
#    INPUTS:
#    -sub:
#    -ear:
#    OUTPUTS:
#    -returns [...]
#    """
#
#    filename = sub + "_PTA-deltas_" + ear + ".html"
#
#    return filename


#def savefile(result_path, fig, sub, ear):
#    """
#    This function [...]
#    INPUTS:
#    -result_path:
#    -fig:
#    -sub:
#    -ear:
#    OUTPUTS:
#    -returns [...]
#    """
#
#    filename = file_name(sub, ear)
#    save_path = os.path.join(result_path, "graphs", sub, filename)
#    #print(save_path)
#    fig.write_html(save_path)

    
def graph_title(sub):
    """
    This function [...]
    INPUTS:
    -sub:
    -condition:
    OUTPUTS:
    -returns [...]
    """

    title = sub + ", test-retest difference, Matrix Speech-in-Noise test"

    return title


def fig_generation(result_path):
    """
    This function [...]
    INPUTS:
    -result_path: path inside the results folder ([repo_root]/results/)
    OUTPUTS:
    -returns [...]
    """

    # Path inside the reports folder
    report_path = os.path.join(result_path, "reports")
    
    # Build lists of all the reports to plot
    files_01 = trace_list(report_path, "sub-01")
    files_02 = trace_list(report_path, "sub-02")
    files_03 = trace_list(report_path, "sub-03")
    files_04 = trace_list(report_path, "sub-04")
    files_05 = trace_list(report_path, "sub-05")
    files_06 = trace_list(report_path, "sub-06")
    
    ls2do = [files_01, files_02,
             files_03, files_04,
             files_05, files_06]

    #print(ls2do)
    
    for i in range(0, len(ls2do)):
        #print(ls2do[i])
        decomp_sub = ls2do[i][0].split("_")
        sub = decomp_sub[0]
        #print(sub)

        ls_ses = []
        for a in range(0, len(ls2do[i])):
            #ls_ses_pair = []
            split_underscore = ls2do[i][a].split("_")
            #ses_pre = split_underscore[2]
            #print(ses_pre)
            #ls_ses_pair.append(ses_pre)
            ses_post = split_underscore[3].split(".")
            #print(ses_post[0])
            #ls_ses_pair.append(ses_post[0])
            #ls_ses.append(ls_ses_pair)
            ls_ses.append(ses_post[0])

        ls_ses.sort()
        #print(ls_ses)
        
        # Figure titles and axis informations
        title = graph_title(sub)
        labels = {"title": title,
                  "x": "Test Condition",
                  "y": "\u0394 50% Comprehension Threshold (dB)"}

        # Figures initialization and general parameters definition
        fig_L1 = go.Figure()
        fig_L2 = go.Figure()

        fig_L1.update_layout(title=labels["title"] + ", L1",
                             xaxis_title=labels["x"],
                             yaxis_title=labels["y"],
                             showlegend=True,
                             #xaxis_type="log",
                             #xaxis_range=[np.log10(100), np.log10(20000)],
                             yaxis_range=[-5, 5],
                             yaxis_dtick=1,
                             xaxis_showline=True,
                             xaxis_linecolor="black",
                             yaxis_showline=True,
                             yaxis_linecolor="black",
                             yaxis_zeroline=True,
                             yaxis_zerolinewidth=1,
                             yaxis_zerolinecolor="black")
        
        fig_L2.update_layout(title=labels["title"] + ", L2",
                             xaxis_title=labels["x"],
                             yaxis_title=labels["y"],
                             showlegend=True,
                             #xaxis_type="log",
                             #xaxis_range=[np.log10(100), np.log10(20000)],
                             yaxis_range=[-5, 5],
                             yaxis_dtick=1,
                             xaxis_showline=True,
                             xaxis_linecolor="black",
                             yaxis_showline=True,
                             yaxis_linecolor="black",
                             yaxis_zeroline=True,
                             yaxis_zerolinewidth=1,
                             yaxis_zerolinecolor="black")
        
        # Trace generations
        for b in range(0, len(ls2do[i])):
            path_df = os.path.join(report_path, sub, ls2do[i][b])
            df = pd.read_csv(path_df, sep="\t")
            #print(df)
            columns = list(df.columns)

            decomp_ses = ls2do[i][b].split("_")
            #print(decomp_ses)
            ses_type = decomp_ses[2]
            #print(ses_type)
            decomp_scan = decomp_ses[3].split(".")
            ses_scan = decomp_scan[0]
            
            file_ref = f"{sub}_sessions.tsv"
            path_df_ref = os.path.join(result_path, "BIDS_data", sub, file_ref)
            df_ref = pd.read_csv(path_df_ref, sep="\t")

            scan = df_ref.loc[df_ref["session_id"] == ses_scan,
                              "scan_type"].iloc[0].lower()[0:4]
            #print(scan)

            if ses_type == "ses-02":
                ses_name = (f"48Post - Bsl_2 "
                            f"(ses_{ls_ses.index(ses_scan)+1:02d}, {scan})")
            else:
                ses_name = (f"Post - Pre "
                            f"(ses_{ls_ses.index(ses_scan)+1:02d}, {scan})")

            #print(ses_name)

            #df.drop(["Mean", "Standard Deviation"], axis=0, inplace=True)
            #print(df)
            
            x_L1 = []
            x_L2 = []
            data_L1 = []
            data_L2 = []
            lang_L1 = None
            lang_L2 = None
            
            for x in range(0, len(df)):
                if (df.at[x, "condition"] == "Mean" or
                        df.at[x, "condition"] == "Standard Deviation"):
                    pass
                else:            
                    try:
                        float(df.at[x, "diff_L1"])
                    except:
                        if df.at[x, "condition"] == "Language":
                            lang_L1 = df.at[x, "diff_L1"]
                        else:
                            pass
                    else:
                        x_L1.append(df.at[x, "condition"])
                        data_L1.append(float(df.at[x, "diff_L1"]))
           
            #print(x_L1)
            #print(data_L1)

            fig_L1.add_trace(go.Scatter(x=x_L1,
                                        y=data_L1,
                                        mode='lines+markers',
                                        name=ses_name,
                                        hovertemplate="%{x}<br>" +
                                                      "%{y:1.1f} dB SPL"))

            print(columns)

            if "diff_L2" in columns:
                print(True)

                for p in range(0, len(df)):
                    if (df.at[p, "condition"] == "Mean" or
                            df.at[p, "condition"] == "Standard Deviation"):
                        pass
                    else:
                        try:
                            float(df.at[p, "diff_L2"])
                        except:
                            if df.at[p, "condition"] == "Language":
                                lang_L2 = df.at[p, "diff_L2"]
                            else:
                                pass
                        else:
                            x_L2.append(df.at[p, "condition"])
                            data_L2.append(float(df.at[p, "diff_L2"]))
    
                fig_L2.add_trace(go.Scatter(x=x_L2,
                                            y=data_L2,
                                            mode='lines+markers',
                                            name=ses_name,
                                            hovertemplate="%{x}<br>" +
                                                          "%{y:1.2f} dB SPL"))
                #print(x_L2)
                #print(data_L2)

            else:
                pass

        #fig_L1.show()
        fig_L2.show()
#        
#        savefile(result_path, fig_L, sub, "L")
#        savefile(result_path, fig_R, sub, "R")
#
#
if __name__ == "__main__":
    root_path = ".."
    result_path = os.path.join(root_path, "results")

    fig_generation(result_path)
    print("\n")

else:
    pass
