import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import plotly.graph_objects as go
#import plotly.figure_factory as ff
from matplotlib.ticker import ScalarFormatter

from src import graph_functions as gf


if __name__ == "__main__":
    print("This script is not designed to be used as a standalone script. "
          "Please use graph_generator.py to call it.")

else:
#    def save_graph(graph, ear, path, ID, session):
#        """
#        INPUTS
#        -graph: interactive plotly.graph_objects figure
#        -ear: ear side linked with the graph
#        -path: path to the result folder: [repo_root]/results/
#        -ID: subject ID number (digits only)
#        -session: session ID number (digits only)
#        OUTPUTS
#        -saves the graph in a .html file to a subject's specific
#         location in the repository
#        """

#        sub = "sub-" + ID
#        folder = os.path.join(path, "graphs", sub)
#        filename = ("Sub-" + ID + "_TEOAE_Session-" + session
#                    + "_(" + ear + ").html")
#        #print(folder, "\n", filename)

#        save_path = os.path.join(folder, filename)

#        graph.write_html(save_path)

#        return True

    def generate_title_dpoae(df, ear, filename):
        """
        INPUTS
        -df: dataframe with the informations to generate the title for a
             single run
        -ear: ear side linked with the title
        -filename: name of the .tsv file where the df is coming from
        OUTPUTS
        -returns a string to use as a title for the graph to generate,
         the subject ID number and the session number
        """
        ls_filename = filename.split("_")
        #print(ls_filename)
        ls_sub = ls_filename[0].split("-")
        #print(ls_sub)
        ls_ses = ls_filename[1].split("-")
        #print(ls_ses)

        ID = "Sub" + ls_sub[1]
        name = "Session " + ls_ses[1]

        title = (ID + " - " + name + ": DPOAE (" + ear + ")")
        #print(title)

        return title, ls_sub[1], ls_ses[1]

    def data_to_plot(df, column):
        """
        INPUTS
        -df: one line dataframe from which this function extract the data
             to plot
        -column: name of the column containing the relevant data
        OUTPUTS
        -returns two lists of data containing the x and y values to plot
        """

        x = []
        y = []

        for i in range(0, len(df)):
            x.append(df["freq2"][i])
            y.append(df[column][i])

        return x, y

###############################################################################

    def plot_dpoae(path, df, side, filename):
        """
        INPUTS
        -path: path to the result folder: [repo_root]/results/
        -df: pandas dataframe containing the data to plot
        -side: side of the ear linked to the data in the df
        -filename: .tsv file name to be used to extract test information
        OUTPUTS
        -saves DPOAE graphs in .html
        """

        if side == "R":
            ear = "Right Ear"
            marker = "o"
        elif side == "L":
            ear = "Left Ear"
            marker = "x"

        title, ID, session = generate_title_dpoae(df, ear, filename)
        labels = {"title": title,
                  "x": "F2 frequency (Hz)",
                  "y": "OAE response (dB SPL)"}

#        fig = go.Figure()
#        fig = plt.figure()

#        fig.update_layout(title=labels["title"],
#                          xaxis_title=labels["x"],
#                          yaxis_title=labels["y"],
#                          xaxis_type="linear",
#                          xaxis_range=[0, 6000],
#                          yaxis_range=[-20, 20],
#                          xaxis_dtick=1000,
#                          yaxis_dtick=5,
#                          xaxis_showline=True,
#                          xaxis_linecolor="black",
#                          yaxis_showline=True,
#                          yaxis_linecolor="black",
#                          yaxis_zeroline=True,
#                          yaxis_zerolinewidth=1,
#                          yaxis_zerolinecolor="black",
#                          barmode="overlay")

        x_data, y_data = data_to_plot(df, "dp")
        #print(y_data)
        x_2sd, y_2sd = data_to_plot(df, "noise+2sd")
        #print(x_2sd, y_2sd)
        x_1sd, y_1sd = data_to_plot(df, "noise+1sd")
        #print(x_1sd, y_1sd)
        y_floor = [-25, -25, -25, -25, -25, -25, -25, -25]

#        fig.add_trace(go.Scatter(x=x_data,
#                                 y=y_floor,
#                                 name="floor",
#                                 fill="none",
#                                 stackgroup=1,
#                                 showlegend=False))

#        fig.add_trace(go.Scatter(x=x_data,
#                                 y=y_data,
#                                 name="TEOAE response",
#                                 mode="none",
#                                 fill="tominimumy",
#                                 stackgroup=1,
#                                 hovertemplate="%{x:.0f} Hz<br>" +
#                                               "%{y:.1f} dB SPL"))

#        fig.add_trace(go.Scatter(x=x_noise,
#                                 y=y_noise,
#                                 name="Noise level",
#                                 fill="none",
#                                 stackgroup=1,
#                                 hovertemplate="%{x:.0f} Hz<br>" +
#                                               "%{y:.1f} dB SPL"))

        fig, ax = plt.subplots(figsize=(11, 8.5), dpi=250)
        plt.plot(x_data,
                 y_data,
                 label="DPOAE response",
                 color="darkturquoise",
                 marker=marker)
        plt.plot(x_2sd,
                 y_2sd,
                 label="Noise + 2 SD level",
                 color="orange")
        plt.plot(x_1sd,
                 y_1sd,
                 label="Noise + 1 SD level",
                 color="orangered")

        ax.axis([900, 11000, -10, 30])
        plt.grid()
        plt.xscale("log")
        ax.xaxis.set_major_formatter(ScalarFormatter())
        #plt.axhline(0, color="k")
        #plt.axvline(0, color="k")
        plt.title(labels["title"])
        plt.xlabel(labels["x"])
        plt.ylabel(labels["y"])
        plt.legend()

#        plt.fill_between(x=x_data,
#                         y1=y_data,
#                         y2=y_floor,
#                         color="darkturquoise")
        plt.fill_between(x=x_2sd,
                         y1=y_2sd,
                         y2=y_floor,
                         color="orange")
        plt.fill_between(x=x_1sd,
                         y1=y_1sd,
                         y2=y_floor,
                         color="orangered")


        
        sub = "sub-" + ID
        folder = os.path.join(path, "graphs", sub)
        filename = ("Sub-" + ID + "_DPOAE_Session-" + session
                    + "_(" + ear + ").png")

        save_path = os.path.join(folder, filename)

        plt.savefig(save_path)
        plt.close()
        
        return True

#        completed = save_graph(fig, ear, path, ID, session)

#        if completed is True:
#            return True
#        else:
#            return False

###############################################################################

#    def plot_boxplot_pta(path, df, ear, display=False):
#        """
#        INPUTS
#        -df: pandas dataframe containing the data to plot
#        OUTPUTS
#        -saves pta graph in .html
#        """

#        if ear == "Right ear":
#            strip = "RE_"
#        elif ear == "Left ear":
#            strip = "LE_"

#        title_graph = gf.generate_title_graph(df, "PTA")
#        labels = {"title": title_graph,
#                  "x": "Frequency (Hz)",
#                  "y": "Hearing Threshold (dB HL)"}

#        fig = go.Figure()

#        fig.update_layout(title=labels["title"],
#                          xaxis_title=labels["x"],
#                          yaxis_title=labels["y"],
#                          xaxis_type="log",
#                          xaxis_range=[np.log10(100), np.log10(20000)],
#                          yaxis_range=[80, -20],
#                          yaxis_dtick=10,
#                          xaxis_showline=True,
#                          xaxis_linecolor="black",
#                          yaxis_showline=True,
#                          yaxis_linecolor="black",
#                          yaxis_zeroline=True,
#                          yaxis_zerolinewidth=1,
#                          yaxis_zerolinecolor="black")

#        conditions = df["Protocol condition"]

#        df_toplot = gf.eliminate_column(df, strip)
#        column_names = df_toplot.columns
#        column_names_int = []

#        for a in range(0, len(column_names)):
#            column_names_int.append(int(column_names[a].lstrip(strip)))

#        df_toplot.columns = column_names_int

#        rows = []

#        for d in range(0, len(df_toplot)):
#            for e in df_toplot.columns:
#                rows.append([e, df_toplot[e][d], conditions[d]])

#        new_df = pd.DataFrame(rows,
#                              columns=["Frequency (Hz)",
#                                       "Hearing Threshold (dB HL)",
#                                       "Protocol condition"])

#        new_df = gf.eliminate_row(new_df,
#                                  "Hearing Threshold (dB HL)",
#                                  130)

#        baseline = ["Baseline",
#                    "Supplementary PTA test (Baseline)"]
#        pre = ["Condition 1A (right before the scan)",
#               "Suppl. PTA test (right before the scan)"]
#        post = ["Condition 1B (right after the scan)",
#                "Suppl. PTA test (right after the scan)"]
#        post48 = "Condition 2 (2-7 days post-scan)"

#        new_df["Protocol condition"].replace(baseline,
#                                             "Baseline",
#                                             inplace=True)
#        new_df["Protocol condition"].replace(pre,
#                                             "Prescan",
#                                             inplace=True)
#        new_df["Protocol condition"].replace(post,
#                                             "Postscan",
#                                             inplace=True)
#        new_df["Protocol condition"].replace(post48,
#                                             "48h+ Postscan",
#                                             inplace=True)

#        fig.add_trace(go.Violin(
#            x=(new_df["Frequency (Hz)"]
#               [new_df["Protocol condition"] == "Baseline"]),
#            y=(new_df["Hearing Threshold (dB HL)"]
#               [new_df["Protocol condition"] == "Baseline"]),
#            name="Baseline",
#            legendgroup="Baseline")
#            )

#        fig.add_trace(go.Violin(
#            x=(new_df["Frequency (Hz)"]
#               [new_df["Protocol condition"] == "Prescan"]),
#            y=(new_df["Hearing Threshold (dB HL)"]
#               [new_df["Protocol condition"] == "Prescan"]),
#            name="Prescan",
#            legendgroup="Prescan")
#            )

#        fig.add_trace(go.Violin(
#            x=(new_df["Frequency (Hz)"]
#               [new_df["Protocol condition"] == "Postscan"]),
#            y=(new_df["Hearing Threshold (dB HL)"]
#               [new_df["Protocol condition"] == "Postscan"]),
#            name="Postscan",
#            legendgroup="Postscan")
#            )

#        fig.add_trace(go.Violin(
#            x=(new_df["Frequency (Hz)"]
#               [new_df["Protocol condition"] == "48h+ Postscan"]),
#            y=(new_df["Hearing Threshold (dB HL)"]
#               [new_df["Protocol condition"] == "48h+ Postscan"]),
#            name="48h+ Postscan",
#            legendgroup="48h+ Postscan")
#            )

#        if ear == "Right ear":
#            save_parameter = "boxplot_R"
#        elif ear == "Left ear":
#            save_parameter = "boxplot_L"

#        if display is True:
#            fig.show()
#       else:
#           completed = save_graph_PTA(path, fig, df, save_parameter)

#            if completed is True:
#                return True
#            else:
#                return False
