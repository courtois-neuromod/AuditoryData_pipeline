import os
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import plotly.graph_objects as go
# import plotly.figure_factory as ff
# from src import graph_functions as gf


pta_freq = [250, 500, 1000, 2000, 3000, 4000, 6000, 8000,
            9000, 10000, 11200, 12500, 14000, 16000, 18000, 20000]


if __name__ == "__main__":
    print("This script is not designed to be used as a standalone script. "
          "Please use graph_generator.py to call it.")

else:
    def save_graph(graph, ear, path, ID, session):
        """
        INPUTS
        -graph: interactive plotly.graph_objects figure
        -ear: ear side linked with the graph
        -path: path to the result folder: [repo_root]/results/
        -ID: subject ID number (digits only)
        -session: session ID number (digits only)
        OUTPUTS
        -saves the graph in a .html file to a subject's specific
         location in the repository
        """

        sub = "sub-" + ID
        folder = os.path.join(path, "graphs", sub)
        filename = ("Sub-" + ID + "_PTA_Session-" + session
                    + "_(" + ear + ").html")
        #print(folder, "\n", filename)

        save_path = os.path.join(folder, filename)

        graph.write_html(save_path)

        return True

    def generate_title_pta(df, ear, filename):
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

        title = (ID + " - " + name + ": PTA (" + ear + ")")
        #print(title)

        return title, ls_sub[1], ls_ses[1]

    def data_to_plot(df, row):
        """
        INPUTS
        -df: one line dataframe from which this function extract the data
             to plot
        -row: value of the side column to extract the row containing
              the relevant data
        OUTPUTS
        -returns two lists of data containing the x and y values to plot
        """

        x = []
        y = []

        mask = df["side"] == row
        df_mask = df[mask].reset_index(drop=True)
        df_mask.drop(columns=["order", "side"], inplace=True)
        #print(mask, "\n", df_mask, "\n", df)

        columns = df_mask.columns

        for i in range(0, len(columns)):
            if df_mask[columns[i]][0] != "No response":
                x.append(pta_freq[i])
                y.append(df_mask[columns[i]][0])
            else:
                continue

        #print(x, y)

        return x, y

    def plot_pta(path, df, filename, side="Both"):
        """
        INPUTS
        -path: path to the result folder: [repo_root]/results/
        -df: pandas dataframe containing the data to plot
        -filename: .tsv file name to be used to extract test information
        -side: side of the ear linked to the data in the df
               -> Default value = Both sides
        OUTPUTS
        -saves PTA graphs in .html
        """

        if side == "R":
            ear = "Right Ear"
        elif side == "L":
            ear = "Left Ear"
        elif side == "Both":
            ear = "Both Ears"

        title, ID, session = generate_title_pta(df, ear, filename)
        labels = {"title": title,
                  "x": "Frequency (Hz)",
                  "y": "Hearing Threshold (dB HL)"}

        fig = go.Figure()

        fig.update_layout(title=labels["title"],
                          xaxis_title=labels["x"],
                          yaxis_title=labels["y"],
                          xaxis_type="log",
                          xaxis_range=[np.log10(100), np.log10(20000)],
                          yaxis_range=[80, -20],
                          yaxis_dtick=10,
                          xaxis_showline=True,
                          xaxis_linecolor="black",
                          yaxis_showline=True,
                          yaxis_linecolor="black",
                          yaxis_zeroline=True,
                          yaxis_zerolinewidth=1,
                          yaxis_zerolinecolor="black")

        if side == "R":
            frequency_R, value_R = data_to_plot(df, "R")
            #print(value_R)

            fig.add_trace(go.Scatter(x=frequency_R,
                                     y=value_R,
                                     line_color="red",
                                     mode='lines+markers',
                                     name=ear,
                                     hovertemplate="%{x:1.0f} Hz<br>" +
                                                   "%{y:1.0f} dB HL"))

        elif side == "L":
            frequency_L, value_L = data_to_plot(df, "L")
            #print(value_L)

            fig.add_trace(go.Scatter(x=frequency_L,
                                     y=value_L,
                                     line_color="blue",
                                     mode='lines+markers',
                                     name=ear,
                                     hovertemplate="%{x:1.0f} Hz<br>" +
                                                   "%{y:1.0f} dB HL"))

        elif side == "Both":
            frequency_R, value_R = data_to_plot(df, "R")
            #print(value_R)
            frequency_L, value_L = data_to_plot(df, "L")
            #print(value_L)

            fig.add_trace(go.Scatter(x=frequency_R,
                                     y=value_R,
                                     line_color="red",
                                     mode='lines+markers',
                                     name="Right ear",
                                     hovertemplate="%{x:1.0f} Hz<br>" +
                                                   "%{y:1.0f} dB HL"))

            fig.add_trace(go.Scatter(x=frequency_L,
                                     y=value_L,
                                     line_color="blue",
                                     mode='lines+markers',
                                     name="Left ear",
                                     hovertemplate="%{x:1.0f} Hz<br>" +
                                                   "%{y:1.0f} dB HL"))

        completed = save_graph(fig, ear, path, ID, session)

        if completed is True:
            return True
        else:
            return False

#    def plot_pta_subject(path, df, display=False):
#        """
#        INPUTS
#        -df: pandas dataframe containing the data to plot
#        OUTPUTS
#        -saves pta graph in .html
#        """

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
