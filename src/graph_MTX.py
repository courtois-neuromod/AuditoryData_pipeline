import os
import plotly.graph_objects as go
from src import graph_functions as gf


if __name__ == "__main__":
    print("This script is not designed to be used as a standalone script. "
          "Please use graph_generator.py to call it.")

else:
    def extract_language(df, run_ID):
        """
        INPUTS
        -df: one-line dataframe containing the tests
        -run_ID: specifies if it is the first or second language
        OUTPUTS
        -returns the name of the language linked to the run_ID
        """

        row = df.index[0]

        if run_ID == "L1":
            language = df["MTX1_LANG"][row]
        elif run_ID == "L2":
            language = df["MTX2_LANG"][row]

        return language

    def save_graph_MTX(path, graph, df, language_ID):
        """
        INPUTS
        -graph: interactive plotly.graph_objects figure
        -df: dataframe with the informations that were used to
             generate the graph
        -language_ID: specifies if it is the L1 or L2 and which
                      language was used
        OUTPUTS
        -saves the graph in a .html file to a subject's specific
         location in the repository
        """

        test = "MTX"

        row = df.index[0]

        sub = df["Participant_ID"][row]
        sub_short = sub.lstrip("Sub")
        sub_long = "sub-" + sub_short

        folder = os.path.join(path, "graphs", sub_long)
        path_header = os.path.join(folder,
                                   ("Sub-" + sub_short + "_" + test + "_"))

        if language_ID.endswith("_All_runs") is True:
            save_path = path_header + language_ID + ".html"

        else:
            session = df["DATE"][row]
            name = df["Protocol name"][row]
            condition = df["Protocol condition"][row]

            save_path = (path_header + session + "_" + name + ": "
                         + condition + " (" + language_ID + ")" + ".html")

        graph.write_html(save_path)

        return True

    def generate_title_run_MTX(df, run_ID, index):
        """
        INPUTS
        -df: dataframe with the informations to generate the title for a
             single run
        -run_ID: indicates if it is the first or second language
        OUTPUTS
        -returns a string to use as a title for the graph to generate
        """

        ID = df["Participant_ID"][index]
        name = df["Protocol name"][index]
        condition = df["Protocol condition"][index]
        language = run_ID + ": " + extract_language(df.loc[[index]], run_ID)

        title = (ID + " - " + "Matrix Test, " + name + ": " + condition + " ("
                 + language + ")")

        return title

    def data_to_plot_MTX(df, prefix):
        """
        INPUTS
        -df: one line dataframe from which this function extracts
             the data to plot
        -prefix: str marker pointing to the columns containing the
                 relevant data
        OUTPUTS
        -returns two lists of data containing the x and y values to plot
        """

        column_names = df.columns
        row = df.index[0]
        x = ["Noise: Left<br>Speech: Left",
             "Noise: Binaural<br>Speech: Left",
             "Noise: Binaural<br>Speech: Binaural",
             "Noise: Binaural<br>Speech: Right",
             "Noise: Right<br>Speech: Right"]
        y = []

        for i in column_names:
            if i.startswith(prefix):
                value = df[i][row].replace(",", ".")
                y.append(float(value))
            else:
                continue

        return x, y

    def plot_mtx(path, df, run_ID):
        """
        INPUTS
        -df: pandas dataframe containing the data to plot
        -run_ID: specifies if it is the first or second language
        OUTPUTS
        -saves mtx graphs in .html
        """

        if run_ID == "L1":
            prefix = "MTX1_"
        elif run_ID == "L2":
            prefix = "MTX2_"

        language = extract_language(df, run_ID)
        language_ID = run_ID + ": " + language
        no_lang_df = df.drop(labels=f"{prefix}LANG", axis=1)
        title = generate_title_run_MTX(df, run_ID, df.index[0])
        labels = {"title": title,
                  "x": "Test Condition",
                  "y": "50% Comprehension Threshold (dB)"}

        fig = go.Figure()

        fig.update_layout(title=labels["title"],
                          xaxis_title=labels["x"],
                          yaxis_title=labels["y"],
                          yaxis_range=[-15, 5],
                          yaxis_dtick=5,
                          xaxis_showline=True,
                          xaxis_linecolor="black",
                          yaxis_showline=True,
                          yaxis_linecolor="black",
                          yaxis_zeroline=True,
                          yaxis_zerolinewidth=1,
                          yaxis_zerolinecolor="black")

        x, y = data_to_plot_MTX(no_lang_df, prefix)

        fig.add_trace(go.Scatter(x=x,
                                 y=y,
                                 mode='lines+markers',
                                 name=labels["title"],
                                 hovertemplate="%{x}<br>" +
                                               "%{y:0.1f} dB"))

        completed = save_graph_MTX(path, fig, df, language_ID)

        if completed is True:
            return True
        else:
            return False

    def plot_mtx_subject(path, df, run_ID, display=False):
        """
        INPUTS
        -df: pandas dataframe containing the data to plot
        -run_ID: specifies if it is the first or second language
        OUTPUTS
        -saves mtx graphs in .html
        """

        if run_ID == "L1":
            prefix = "MTX1_"
        elif run_ID == "L2":
            prefix = "MTX2_"

        language_title = extract_language(df, run_ID)
        language_ID_title = run_ID + ": " + language_title
        language_ID_save = run_ID + "_" + language_title + "_All_runs"
        no_lang_df = df.drop(labels=f"{prefix}LANG", axis=1)
        title_graph = (gf.generate_title_graph(df, "MTX") + " ("
                       + language_ID_title + ")")
        labels = {"title": title_graph,
                  "x": "Test Condition",
                  "y": "50% Comprehension Threshold (dB)"}

        fig = go.Figure()

        fig.update_layout(title=labels["title"],
                          xaxis_title=labels["x"],
                          yaxis_title=labels["y"],
                          yaxis_range=[-15, 5],
                          yaxis_dtick=5,
                          xaxis_showline=True,
                          xaxis_linecolor="black",
                          yaxis_showline=True,
                          yaxis_linecolor="black",
                          yaxis_zeroline=True,
                          yaxis_zerolinewidth=1,
                          yaxis_zerolinecolor="black")

        for i in range(0, len(df)):
            x, y = data_to_plot_MTX(no_lang_df.loc[[i]], prefix)

            title_run = generate_title_run_MTX(df, run_ID, i)

            fig.add_trace(go.Scatter(x=x,
                                     y=y,
                                     mode='lines+markers',
                                     name=title_run,
                                     hovertemplate="%{x}<br>" +
                                                   "%{y:0.1f} dB"))

        if display is True:
            fig.show()
        else:
            completed = save_graph_MTX(path, fig, df, language_ID_save)

            if completed is True:
                return True
            else:
                return False
