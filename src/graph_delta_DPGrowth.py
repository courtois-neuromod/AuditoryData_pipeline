import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go


def trace_list(report_path, sub, freq):
    """
    This function [...]
    INPUTS:
    -report_path:
    -sub:
    -ear:
    -freq:
    OUTPUTS:
    -returns [...]
    """

    path = os.path.join(report_path, sub)

    ls_doc = os.listdir(path)
    
    ls = []
    for i in ls_doc:
        if (i.startswith(sub)
                and i.find("report") != -1
                and i.find(f"Growth{freq}") != -1):
            ls.append(i)
        else:
            pass

    ls.sort()

    return ls


def file_name(sub, ear, freq):
    """
    This function [...]
    INPUTS:
    -sub:
    -ear:
    -freq:
    OUTPUTS:
    -returns [...]
    """

    filename = sub + f"_Growth{freq}_deltas_" + ear + ".html"

    return filename


def savefile(result_path, fig, sub, ear, freq):
    """
    This function [...]
    INPUTS:
    -result_path:
    -sub:
    -ear:
    -freq:
    OUTPUTS:
    -returns [...]
    """

    filename = file_name(sub, ear, freq)
    save_path = os.path.join(result_path, "graphs", sub, filename)
    #print(save_path)
    fig.write_html(save_path)


def graph_title(sub):
    """
    This function [...]
    INPUTS:
    -sub:
    OUTPUTS:
    -returns [...]
    """

    title = sub + (", Différences test-retest, Émissions otoacoustiques par "
                   "produits de distortion: fonction de croissance")

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
    files_01_2 = trace_list(report_path, "sub-01", 2)
    files_01_4 = trace_list(report_path, "sub-01", 4)
    files_01_6 = trace_list(report_path, "sub-01", 6)
    files_02_2 = trace_list(report_path, "sub-02", 2)
    files_02_4 = trace_list(report_path, "sub-02", 4)
    files_02_6 = trace_list(report_path, "sub-02", 6)
    files_03_2 = trace_list(report_path, "sub-03", 2)
    files_03_4 = trace_list(report_path, "sub-03", 4)
    files_03_6 = trace_list(report_path, "sub-03", 6)
    # files_04_2 = trace_list(report_path, "sub-04", 2)
    # files_04_4 = trace_list(report_path, "sub-04", 4)
    # files_04_6 = trace_list(report_path, "sub-04", 6)
    files_05_2 = trace_list(report_path, "sub-05", 2)
    files_05_4 = trace_list(report_path, "sub-05", 4)
    files_05_6 = trace_list(report_path, "sub-05", 6)
    files_06_2 = trace_list(report_path, "sub-06", 2)
    files_06_4 = trace_list(report_path, "sub-06", 4)
    files_06_6 = trace_list(report_path, "sub-06", 6)
    
    ls2do = [[files_01_2, files_01_4, files_01_6],
             [files_02_2, files_02_4, files_02_6],
             [files_03_2, files_03_4, files_03_6],
             # [files_04_2, files_04_4, files_04_6],
             [files_05_2, files_05_4, files_05_6],
             [files_06_2, files_06_4, files_06_6]
            ]

    #print(ls2do)
    
    for i in range(0, len(ls2do)):
        #print(ls2do[i])
        decomp_sub = ls2do[i][0][0].split("_")
        sub = decomp_sub[0]
        #print(sub)

        ls_ses = []
        for a in range(0, len(ls2do[i])):
            #print(ls2do[i][a])
            for x in range(0, len(ls2do[i][a])):
                #print(ls2do[i][a][x])
                split_underscore = ls2do[i][a][x].split("_")
                ses_post = split_underscore[3].split(".")
                ls_ses.append(ses_post[0])

        ls_ses.sort

        # Figures' titles and axis informations
        title = graph_title(sub)
        labels = {"title": title,
                  "x": "Niveau de présentation de F2 (dB SPL)",
                  "y": "\u0394 amplitude émissions otoacoustiques (dB SPL)"}
        #print(labels["y"])

        # Figures initialization and general parameters definition
        fig_L2 = go.Figure()
        fig_R2 = go.Figure()
        fig_L4 = go.Figure()
        fig_R4 = go.Figure()
        fig_L6 = go.Figure()
        fig_R6 = go.Figure()

        fig_L2.update_layout(title=(labels["title"]
                                    + " à 2 kHz, oreille gauche"),
                             xaxis_title=labels["x"],
                             yaxis_title=labels["y"],
                             #xaxis_type="log",
                             xaxis_range=[30, 80],
                             yaxis_range=[-35, 35],
                             yaxis_dtick=5,
                             xaxis_showline=True,
                             xaxis_linecolor="black",
                             yaxis_showline=True,
                             yaxis_linecolor="black",
                             yaxis_zeroline=True,
                             yaxis_zerolinewidth=1,
                             yaxis_zerolinecolor="black")

        fig_R2.update_layout(title=(labels["title"]
                                    + " à 2 kHz, oreille droite"),
                             xaxis_title=labels["x"],
                             yaxis_title=labels["y"],
                             #xaxis_type="log",
                             xaxis_range=[30, 80],
                             yaxis_range=[-35, 35],
                             yaxis_dtick=5,
                             xaxis_showline=True,
                             xaxis_linecolor="black",
                             yaxis_showline=True,
                             yaxis_linecolor="black",
                             yaxis_zeroline=True,
                             yaxis_zerolinewidth=1,
                             yaxis_zerolinecolor="black")

        fig_L4.update_layout(title=(labels["title"]
                                    + " à 4 kHz, oreille gauche"),
                             xaxis_title=labels["x"],
                             yaxis_title=labels["y"],
                             #xaxis_type="log",
                             xaxis_range=[30, 80],
                             yaxis_range=[-35, 35],
                             yaxis_dtick=5,
                             xaxis_showline=True,
                             xaxis_linecolor="black",
                             yaxis_showline=True,
                             yaxis_linecolor="black",
                             yaxis_zeroline=True,
                             yaxis_zerolinewidth=1,
                             yaxis_zerolinecolor="black")

        fig_R4.update_layout(title=(labels["title"]
                                    + " à 4 kHz, oreille droite"),
                             xaxis_title=labels["x"],
                             yaxis_title=labels["y"],
                             #xaxis_type="log",
                             xaxis_range=[30, 80],
                             yaxis_range=[-35, 35],
                             yaxis_dtick=5,
                             xaxis_showline=True,
                             xaxis_linecolor="black",
                             yaxis_showline=True,
                             yaxis_linecolor="black",
                             yaxis_zeroline=True,
                             yaxis_zerolinewidth=1,
                             yaxis_zerolinecolor="black")

        fig_L6.update_layout(title=(labels["title"] 
                                    + " à 6 kHz, oreille gauche"),
                             xaxis_title=labels["x"],
                             yaxis_title=labels["y"],
                             #xaxis_type="log",
                             xaxis_range=[30, 80],
                             yaxis_range=[-35, 35],
                             yaxis_dtick=5,
                             xaxis_showline=True,
                             xaxis_linecolor="black",
                             yaxis_showline=True,
                             yaxis_linecolor="black",
                             yaxis_zeroline=True,
                             yaxis_zerolinewidth=1,
                             yaxis_zerolinecolor="black")

        fig_R6.update_layout(title=(labels["title"]
                                    + " à 6 kHz, oreille droite"),
                             xaxis_title=labels["x"],
                             yaxis_title=labels["y"],
                             #xaxis_type="log",
                             xaxis_range=[30, 80],
                             yaxis_range=[-35, 35],
                             yaxis_dtick=5,
                             xaxis_showline=True,
                             xaxis_linecolor="black",
                             yaxis_showline=True,
                             yaxis_linecolor="black",
                             yaxis_zeroline=True,
                             yaxis_zerolinewidth=1,
                             yaxis_zerolinecolor="black")
        
        # Trace generation
        for b in range(0, len(ls2do[i])):
            for y in range(0, len(ls2do[i][b])):
                #print(ls2do[i][b][y])
                path_df = os.path.join(report_path, sub, ls2do[i][b][y])
                df = pd.read_csv(path_df, sep="\t")
                #print(df)
                columns = list(df.columns)
                #columns.remove("side")

                decomp_ses = ls2do[i][b][y].split("_")
                #print(decomp_ses)
                ses_type = decomp_ses[2]
                #print(ses_type)
                decomp_scan = decomp_ses[3].split(".")
                ses_scan = decomp_scan[0]

                file_ref = f"{sub}_sessions.tsv"
                path_df_ref = os.path.join(result_path, "BIDS_data",
                                           sub, file_ref)
                df_ref = pd.read_csv(path_df_ref, sep="\t")

                scan = df_ref.loc[df_ref["session_id"] == ses_scan,
                                  "scan_type"].iloc[0].lower()[0:4]

                #print(ses_type, ses_type == "ses-01")

                if ses_type == "ses-01":
                    ses_name = (f"48Post - Bsl_1 "
                                f"(ses_{ls_ses.index(ses_scan)+1:02d}, "
                                f"{scan})")

                else:
                    ses_name = (f"Post - Pre "
                                f"(ses_{ls_ses.index(ses_scan)+1:02d}, "
                                f"{scan})")

                x_L = []
                x_R = []
                data_L = []
                data_R = []
            
                for p in range(0, len(df)):
                    try:
                        int(df.at[p, "l2_target"])
                    except:
                        pass
                    else:
                        x_L.append(int(df.at[p, "l2_target"]))
                        data_L.append(float(df.at[p, "diff_L"]))
                
                    try:
                        int(df.at[p, "l2_target"])
                    except:
                        pass
                    else:
                        x_R.append(int(df.at[p, "l2_target"]))
                        data_R.append(float(df.at[p, "diff_R"]))
            
                #print(x_L)
                #print(data_L)
                #print(x_R)
                #print(data_R)

                if ls2do[i][b][y].find("Growth2") != -1:
                    fig_L2.add_trace(go.Scatter(x=x_L,
                                                y=data_L,
                                                mode='lines+markers',
                                                name=ses_name,
                                                hovertemplate=("%{x:1.1f}"
                                                              + " dB SPL<br>"
                                                               + "%{y:1.1f}"
                                                               + " dB SPL")))
                    fig_R2.add_trace(go.Scatter(x=x_R,
                                                y=data_R,
                                                mode='lines+markers',
                                                name=ses_name,
                                                hovertemplate=("%{x:1.1f}"
                                                               + " dB SPL<br>"
                                                               + "%{y:1.1f}"
                                                               + " dB SPL")))

                elif ls2do[i][b][y].find("Growth4") != -1:
                    fig_L4.add_trace(go.Scatter(x=x_L,
                                                y=data_L,
                                                mode='lines+markers',
                                                name=ses_name,
                                                hovertemplate=("%{x:1.1f}"
                                                               + " dB SPL<br>"
                                                               + "%{y:1.1f}"
                                                               + " dB SPL")))
                    fig_R4.add_trace(go.Scatter(x=x_R,
                                                y=data_R,
                                                mode='lines+markers',
                                                name=ses_name,
                                                hovertemplate=("%{x:1.1f}"
                                                               + " dB SPL<br>"
                                                               + "%{y:1.1f}"
                                                               + " dB SPL")))

                elif ls2do[i][b][y].find("Growth6") != -1:
                    fig_L6.add_trace(go.Scatter(x=x_L,
                                                y=data_L,
                                                mode='lines+markers',
                                                name=ses_name,
                                                hovertemplate=("%{x:1.1f}"
                                                               + " dB SPL<br>"
                                                               + "%{y:1.1f}"
                                                               + " dB SPL")))
                    fig_R6.add_trace(go.Scatter(x=x_R,
                                                y=data_R,
                                                mode='lines+markers',
                                                name=ses_name,
                                                hovertemplate=("%{x:1.1f}"
                                                               + " dB SPL<br>"
                                                               + "%{y:1.1f}"
                                                               + " dB SPL")))
            
        #fig_L2.show()
        #fig_R2.show()
        #fig_L4.show()
        #fig_R4.show()
        #fig_L6.show()
        #fig_R6.show()
        
        savefile(result_path, fig_L2, sub, "L", 2)
        savefile(result_path, fig_R2, sub, "R", 2)
        savefile(result_path, fig_L4, sub, "L", 4)
        savefile(result_path, fig_R4, sub, "R", 4)
        savefile(result_path, fig_L6, sub, "L", 6)
        savefile(result_path, fig_R6, sub, "R", 6)
            

fig_generation(os.path.join("..", "results"))
