import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from src import graph_functions as gf


if __name__ == "__main__":
    print("This script is not designed to be used as a standalone script. "
          "Please use graph_generator.py to call it.")

else:
    def save_graph_PTA(path, graph, df, ear):
        """
        INPUTS
        -graph: interactive plotly.graph_objects figure
        -df: dataframe with the informations that were used to
             generate the graph
        -ear: ear side linked with the graph
        OUTPUTS
        -saves the graph in a .html file to a subject's specific
         location in the repository
        """

        test = "PTA"

        row = df.index[0]

        sub = df["Participant_ID"][row]
        sub_short = sub.lstrip("Sub")
        sub_long = "sub-" + sub_short

        folder = os.path.join(path, "graphs", sub_long)
        path_header = os.path.join(folder,
                                   ("Sub-" + sub_short + "_" + test + "_"))

        if ear == "All_runs":
            save_path = path_header + ear + ".html"

        elif ear.startswith("boxplot"):
            save_path = path_header + ear + ".html"

        else:
            session = df["DATE"][row]
            name = df["Protocol name"][row]
            condition = df["Protocol condition"][row]

            save_path = (path_header + session + "_" + name + ": "
                         + condition + " (" + ear + ")" + ".html")

        graph.write_html(save_path)

        return True

    def generate_title_run_PTA(df, ear, index):
        """
        INPUTS
        -df: dataframe with the informations to generate the title for a
             single run
        -ear: ear side linked with the title
        OUTPUTS
        -returns a string to use as a title for the graph to generate
        """

        ID = df["Participant_ID"][index]
        name = df["Protocol name"][index]
        condition = df["Protocol condition"][index]

        title = (ID + " - " + "PTA, " + name + ": " + condition
                 + " (" + ear + ")")

        return title

    def data_to_plot_PTA(df, prefix):
        """
        INPUTS
        -df: one line dataframe from which this function extract the data
             to plot
        -prefix: str marker pointing to the columns containing the
                 relevant data
        OUTPUTS
        -returns two lists of data containing the x and y values to plot
        """

        column_names = df.columns
        row = df.index[0]
        to_search = []
        x = []
        y = []

        for i in column_names:
            if i.startswith(prefix):
                to_search.append(i)
            else:
                continue

        list_130 = gf.return_130(df, to_search)

        for j in list_130:
            to_remove = to_search[j]
            df = df.drop(to_remove, axis=1)

        column_names = df.columns

        for k in column_names:
            if k.startswith(prefix):
                x.append(int(k.lstrip(prefix)))
                y.append(df[k][row])
            else:
                continue

        return x, y

    def plot_pta_L(path, df):
        """
        INPUTS
        -df: pandas dataframe containing the data to plot
        OUTPUTS
        -saves pta graphs in .html
        """

        title = generate_title_run_PTA(df, "Left Ear", df.index[0])
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

        x, y = data_to_plot_PTA(df, "LE_")

        fig.add_trace(go.Scatter(x=x,
                                 y=y,
                                 line_color="blue",
                                 mode='lines+markers',
                                 name=labels["title"],
                                 hovertemplate="%{x:1.0f} Hz<br>" +
                                               "%{y:1.0f} dB HL"))

        completed = save_graph_PTA(path, fig, df, "Left Ear")

        if completed is True:
            return True
        else:
            return False

    def plot_pta_R(path, df):
        """
        INPUTS
        -df: pandas dataframe containing the data to plot
        OUTPUTS
        -saves pta graphs in .html
        """

        title = generate_title_run_PTA(df, "Right Ear", df.index[0])
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

        x, y = data_to_plot_PTA(df, "RE_")

        fig.add_trace(go.Scatter(x=x,
                                 y=y,
                                 line_color="red",
                                 mode='lines+markers',
                                 name=labels["title"],
                                 hovertemplate="%{x:1.0f} Hz<br>" +
                                               "%{y:1.0f} dB HL"))

        completed = save_graph_PTA(path, fig, df, "Right Ear")

        if completed is True:
            return True
        else:
            return False

    def plot_pta_subject(path, df, display=False):
        """
        INPUTS
        -df: pandas dataframe containing the data to plot
        OUTPUTS
        -saves pta graph in .html
        """

        title_graph = gf.generate_title_graph(df, "PTA")
        labels = {"title": title_graph,
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

        for i in range(0, len(df)):
            run_R_x, run_R_y = data_to_plot_PTA(df.loc[[i]], "RE_")
            run_L_x, run_L_y = data_to_plot_PTA(df.loc[[i]], "LE_")

            title_run_R = generate_title_run_PTA(df, "Right Ear", i)
            title_run_L = generate_title_run_PTA(df, "Left Ear", i)

            fig.add_trace(go.Scatter(x=run_R_x,
                                     y=run_R_y,
                                     line_color="red",
                                     mode='lines+markers',
                                     name=title_run_R,
                                     hovertemplate="%{x:1.0f} Hz<br>" +
                                                   "%{y:1.0f} dB HL"))

            fig.add_trace(go.Scatter(x=run_L_x,
                                     y=run_L_y,
                                     line_color="blue",
                                     mode='lines+markers',
                                     name=title_run_L,
                                     hovertemplate="%{x:1.0f} Hz<br>" +
                                                   "%{y:1.0f} dB HL"))

        if display is True:
            fig.show()
        else:
            completed = save_graph_PTA(path, fig, df, "All_runs")

            if completed is True:
                return True
            else:
                return False

    def plot_boxplot_pta(path, df, ear, display=False):
        """
        INPUTS
        -df: pandas dataframe containing the data to plot
        OUTPUTS
        -saves pta graph in .html
        """

        if ear == "Right ear":
            strip = "RE_"
        elif ear == "Left ear":
            strip = "LE_"

        title_graph = gf.generate_title_graph(df, "PTA")
        labels = {"title": title_graph,
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

        conditions = df["Protocol condition"]

        df_toplot = gf.eliminate_column(df, strip)
        column_names = df_toplot.columns
        column_names_int = []

        for a in range(0, len(column_names)):
            column_names_int.append(int(column_names[a].lstrip(strip)))

        df_toplot.columns = column_names_int

        rows = []

        for d in range(0, len(df_toplot)):
            for e in df_toplot.columns:
                rows.append([e, df_toplot[e][d], conditions[d]])

        new_df = pd.DataFrame(rows,
                              columns=["Frequency (Hz)",
                                       "Hearing Threshold (dB HL)",
                                       "Protocol condition"])

        new_df = gf.eliminate_row(new_df,
                                  "Hearing Threshold (dB HL)",
                                  130)

        baseline = ["Baseline",
                    "Supplementary PTA test (Baseline)"]
        pre = ["Condition 1A (right before the scan)",
               "Suppl. PTA test (right before the scan)"]
        post = ["Condition 1B (right after the scan)",
                "Suppl. PTA test (right after the scan)"]
        post48 = "Condition 2 (2-7 days post-scan)"

        new_df["Protocol condition"].replace(baseline,
                                             "Baseline",
                                             inplace=True)
        new_df["Protocol condition"].replace(pre,
                                             "Prescan",
                                             inplace=True)
        new_df["Protocol condition"].replace(post,
                                             "Postscan",
                                             inplace=True)
        new_df["Protocol condition"].replace(post48,
                                             "48h+ Postscan",
                                             inplace=True)

        fig.add_trace(go.Violin(
            x=(new_df["Frequency (Hz)"]
               [new_df["Protocol condition"] == "Baseline"]),
            y=(new_df["Hearing Threshold (dB HL)"]
               [new_df["Protocol condition"] == "Baseline"]),
            name="Baseline",
            legendgroup="Baseline")
            )

        fig.add_trace(go.Violin(
            x=(new_df["Frequency (Hz)"]
               [new_df["Protocol condition"] == "Prescan"]),
            y=(new_df["Hearing Threshold (dB HL)"]
               [new_df["Protocol condition"] == "Prescan"]),
            name="Prescan",
            legendgroup="Prescan")
            )

        fig.add_trace(go.Violin(
            x=(new_df["Frequency (Hz)"]
               [new_df["Protocol condition"] == "Postscan"]),
            y=(new_df["Hearing Threshold (dB HL)"]
               [new_df["Protocol condition"] == "Postscan"]),
            name="Postscan",
            legendgroup="Postscan")
            )

        fig.add_trace(go.Violin(
            x=(new_df["Frequency (Hz)"]
               [new_df["Protocol condition"] == "48h+ Postscan"]),
            y=(new_df["Hearing Threshold (dB HL)"]
               [new_df["Protocol condition"] == "48h+ Postscan"]),
            name="48h+ Postscan",
            legendgroup="48h+ Postscan")
            )

        if ear == "Right ear":
            save_parameter = "boxplot_R"
        elif ear == "Left ear":
            save_parameter = "boxplot_L"

        if display is True:
            fig.show()
        else:
            completed = save_graph_PTA(path, fig, df, save_parameter)

            if completed is True:
                return True
            else:
                return False
