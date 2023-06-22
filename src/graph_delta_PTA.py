import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go


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
                and i.find("PTA") != -1):
            ls.append(i)
        else:
            pass
    
    ls.sort()
    
    return ls


def file_name(sub, ear):
    """
    This function [...]
    INPUTS:
    -sub:
    -ear:
    OUTPUTS:
    -returns [...]
    """

    filename = sub + "_PTA-deltas_" + ear + ".html"

    return filename


def savefile(result_path, fig, sub, ear):
    """
    This function [...]
    INPUTS:
    -result_path:
    -fig:
    -sub:
    -ear:
    OUTPUTS:
    -returns [...]
    """

    filename = file_name(sub, ear)
    save_path = os.path.join(result_path, "graphs", sub, filename)
    #print(save_path)
    fig.write_html(save_path)

    
def graph_title(sub):
    """
    This function [...]
    INPUTS:
    -sub:
    -condition:
    OUTPUTS:
    -returns [...]
    """

    title = sub + ", Différences test-retest, Audiométrie par sons purs"

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

    for i in range(0, len(ls2do)):
        decomp_sub = ls2do[i][0].split("_")
        sub = decomp_sub[0]

        ls_ses = []
        for a, element_a in enumerate(ls2do[i]):
            split_underscore = element_a.split("_")
            ses_post = split_underscore[3].split(".")
            ls_ses.append(ses_post[0])

        ls_ses.sort()
        #print(ls_ses)
        
        # Figures' titles and axis informations
        title = graph_title(sub)
        labels = {"title": title,
                  "x": "Fréquence (Hz)",
                  "y": "\u0394 seuil de détection (dB HL)"}

        # Figures initialization and general parameters definition
        fig_L = go.Figure()
        fig_R = go.Figure()

        fig_L.update_layout(title=labels["title"] + ", oreille gauche",
                            xaxis_title=labels["x"],
                            yaxis_title=labels["y"],
                            showlegend=True,
                            xaxis_type="log",
                            xaxis_range=[np.log10(100), np.log10(20000)],
                            yaxis_range=[-22, 32],
                            yaxis_dtick=5,
                            xaxis_showline=True,
                            xaxis_linecolor="black",
                            yaxis_showline=True,
                            yaxis_linecolor="black",
                            yaxis_zeroline=True,
                            yaxis_zerolinewidth=1,
                            yaxis_zerolinecolor="black")
        
        fig_R.update_layout(title=labels["title"] + ", oreille droite",
                            xaxis_title=labels["x"],
                            yaxis_title=labels["y"],
                            showlegend=True,
                            xaxis_type="log",
                            xaxis_range=[np.log10(100), np.log10(20000)],
                            yaxis_range=[-22, 32],
                            yaxis_dtick=5,
                            xaxis_showline=True,
                            xaxis_linecolor="black",
                            yaxis_showline=True,
                            yaxis_linecolor="black",
                            yaxis_zeroline=True,
                            yaxis_zerolinewidth=1,
                            yaxis_zerolinecolor="black")
        
        # Trace generations
        for b, element_b in enumerate(ls2do[i]):
            path_df = os.path.join(report_path, sub, element_b)
            df = pd.read_csv(path_df, sep="\t")

            columns = list(df.columns)

            decomp_ses = element_b.split("_")

            ses_type = decomp_ses[2]
            decomp_scan = decomp_ses[3].split(".")
            ses_scan = decomp_scan[0]
            
            file_ref = f"{sub}_sessions.tsv"
            path_df_ref = os.path.join(result_path, "BIDS_data", sub, file_ref)
            df_ref = pd.read_csv(path_df_ref, sep="\t")

            scan = df_ref.loc[df_ref["session_id"] == ses_scan,
                              "scan_type"].iloc[0].lower()[0:4]

            if ses_type == "ses-01":
                ses_name = (f"48Post - Bsl_1 "
                            f"(ses_{ls_ses.index(ses_scan)+1:02d}, {scan})")
            else:
                ses_name = (f"Post - Pre "
                            f"(ses_{ls_ses.index(ses_scan)+1:02d}, {scan})")
            
            x_L = []
            x_R = []
            data_L = []
            data_R = []
            
            for x in range(0, len(df)):
                try:
                    int(float(df.at[x, "diff_L"]))
                except ValueError:
                    pass
                else:
                    x_L.append(df.at[x, "freq"])
                    data_L.append(int(float(df.at[x, "diff_L"])))
                
                try:
                    int(float(df.at[x, "diff_R"]))
                except ValueError:
                    pass
                else:
                    x_R.append(df.at[x, "freq"])
                    data_R.append(int(float(df.at[x, "diff_R"])))
            
            #print(x_L)
            #print(data_L)
            #print(x_R)
            #print(data_R)

            fig_L.add_trace(go.Scatter(x=x_L,
                                       y=data_L,
                                       mode='lines+markers',
                                       name=ses_name,
                                       hovertemplate="%{x:1.0f} Hz<br>" +
                                                     "%{y:1.0f} dB HL"))
            fig_R.add_trace(go.Scatter(x=x_R,
                                       y=data_R,
                                       mode='lines+markers',
                                       name=ses_name,
                                       hovertemplate="%{x:1.0f} Hz<br>" +
                                                     "%{y:1.0f} dB HL"))

        #fig_L.show()
        #fig_R.show()
        
        savefile(result_path, fig_L, sub, "L")
        savefile(result_path, fig_R, sub, "R")


if __name__ == "__main__":
    root_path = ".."
    result_path = os.path.join(root_path, "results")

    fig_generation(result_path)
    print("\n")

else:
    pass
