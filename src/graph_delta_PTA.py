import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def trace_list(report_path, sub):
    ls_doc = os.listdir(report_path)
    
    ls = []
    for i in ls_doc:
        if (i.startswith(sub)
                and i.find("delta") != -1
                and i.find("PTA") != -1):
            ls.append(i)
        else:
            pass
    
    return ls

def file_name(sub, ear):
    filename = sub.capitalize() + "_PTA_deltas_" + ear + ".html"
    return filename

def savefile(result_path, fig, sub, ear):
    filename = file_name(sub, ear)
    save_path = os.path.join(result_path, "graphs", sub, filename)
    #print(save_path)
    fig.write_html(save_path)
    
def graph_title(sub):
    title = (sub.capitalize()
             + ", Différences (Postscan - Préscan), Audiométrie par sons purs")
    return title

def fct_1(result_path):
    report_path = os.path.join(result_path, "reports")
    
    files_01 = trace_list(report_path, "sub-01")
    files_02 = trace_list(report_path, "sub-02")
    files_03 = trace_list(report_path, "sub-03")
    # files_04 = trace_list(report_path, "sub-04")
    files_05 = trace_list(report_path, "sub-05")
    files_06 = trace_list(report_path, "sub-06")
    
    ls2do = [files_01, files_02,
             files_03, # files_04,
             files_05, files_06]

    #print(ls2do)
    
    for i in range(0, len(ls2do)):
        #print(ls2do[i])
        filename_decomp = ls2do[i][0].split("_")
        sub = filename_decomp[0]
        #print(sub)
        title = graph_title(sub)
        labels = {"title": title,
                  "x": "Fréquence (Hz)",
                  "y": "Variation du seuil de détection (dB HL)"}
        
        fig_L = go.Figure()
        fig_R = go.Figure()

        fig_L.update_layout(title=labels["title"] + ", oreille gauche",
                            xaxis_title=labels["x"],
                            yaxis_title=labels["y"],
                            xaxis_type="log",
                            xaxis_range=[np.log10(100), np.log10(20000)],
                            yaxis_range=[-20, 30],
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
                            xaxis_type="log",
                            xaxis_range=[np.log10(100), np.log10(20000)],
                            yaxis_range=[-20, 30],
                            yaxis_dtick=5,
                            xaxis_showline=True,
                            xaxis_linecolor="black",
                            yaxis_showline=True,
                            yaxis_linecolor="black",
                            yaxis_zeroline=True,
                            yaxis_zerolinewidth=1,
                            yaxis_zerolinecolor="black")
        
        for a in range(0, len(ls2do[i])):
            path_df = os.path.join(report_path, ls2do[i][a])
            df = pd.read_csv(path_df, sep="\t")
            #print(df)
            columns = list(df.columns)
            #columns.remove("side")
            
            x_L = []
            x_R = []
            data_L = []
            data_R = []
            
            for x in range(0, len(df)):
                try:
                    int(float(df.at[x, "diff_L"]))
                except:
                    pass
                else:
                    x_L.append(df.at[x, "freq"])
                    data_L.append(int(float(df.at[x, "diff_L"])))
                
                try:
                    int(float(df.at[x, "diff_R"]))
                except:
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
#                                       name=title_run_L,
                                       hovertemplate="%{x:1.0f} Hz<br>" +
                                                     "%{y:1.0f} dB HL"))
            fig_R.add_trace(go.Scatter(x=x_R,
                                       y=data_R,
                                       mode='lines+markers',
#                                       name=title_run_R,
                                       hovertemplate="%{x:1.0f} Hz<br>" +
                                                     "%{y:1.0f} dB HL"))
            
        #fig_L.show()
        #fig_R.show()
        
        savefile(result_path, fig_L, sub, "L")
        savefile(result_path, fig_R, sub, "R")
            

fct_1(os.path.join("..", "results"))
