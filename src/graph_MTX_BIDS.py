import os
import plotly.graph_objects as go
from src import graph_functions as gf


if __name__ == "__main__":
    print("This script is not designed to be used as a standalone script. "
          "Please use graph_generator.py to call it.")

else:
#    def extract_language(df, run_ID):
#        """
#        INPUTS
#        -df: one-line dataframe containing the tests
#        -run_ID: specifies if it is the first or second language
#        OUTPUTS
#        -returns the name of the language linked to the run_ID
#        """

#        row = df.index[0]

#        if run_ID == "L1":
#            language = df["MTX1_LANG"][row]
#        elif run_ID == "L2":
#            language = df["MTX2_LANG"][row]

#        return language

    def save_graph(graph, language, path, ID, session):
        """
        INPUTS
        -graph: interactive plotly.graph_objects figure
        -language: language of the test
        -path: path to the result folder: [repo_root]/results/
        -ID: subject ID number (digits only)
        -session: session ID number (digits only)
        OUTPUTS
        -saves the graph in a .html file to a subject's specific
         location in the repository
        """

        sub = "sub-" + ID
        folder = os.path.join(path, "graphs", sub)
        filename = ("Sub-" + ID + "_MTX_Session-" + session
                    + "_(" + language + ").html")
        #print(folder, "\n", filename)

        save_path = os.path.join(folder, filename)

        graph.write_html(save_path)

        return True

    def generate_title_mtx(df, filename, run_ID):
        """
        INPUTS
        -df: dataframe with the informations to generate the title for a
             single run
        -filename: name of the .tsv file where the df is coming from
        -run_ID: language ID (first or second language of the participant)
        OUTPUTS
        -returns a string to use as a title for the graph to generate,
         the subject ID number and the session number
        """

        #print(df)

        ls_filename = filename.split("_")
        #print(ls_filename)
        ls_sub = ls_filename[0].split("-")
        #print(ls_sub)
        ls_ses = ls_filename[1].split("-")
        #print(ls_ses)

        ID = "Sub" + ls_sub[1]
        name = "Session " + ls_ses[1]
        
        mask = df["order"] == run_ID
        sub_df = df[mask].reset_index(drop=True)
        
        language = sub_df.at[0, "language"]
        #print(language)

        title = (ID + " - " + name + ": MTX (Language "
                 + str(run_ID) + ": " + language + ")")
        #print(title)

        return title, ls_sub[1], ls_ses[1], language

#        """
#        INPUTS
#        -df: dataframe with the informations to generate the title for a
#             single run
#        -run_ID: indicates if it is the first or second language
#        OUTPUTS
#        -returns a string to use as a title for the graph to generate
#        """

#        ID = df["Participant_ID"][index]
#        name = df["Protocol name"][index]
#        condition = df["Protocol condition"][index]
#        language = run_ID + ": " + extract_language(df.loc[[index]], run_ID)

#        title = (ID + " - " + "Matrix Test, " + name + ": " + condition + " ("
#                 + language + ")")

#        return title

    def data_to_plot(df, run_ID):
        """
        INPUTS
        -df: one line dataframe from which this function extracts
             the data to plot
        -prefix: str marker pointing to the columns containing the
                 relevant data
        OUTPUTS
        -returns two lists of data containing the x and y values to plot
        """

        x = ["Noise: Left<br>Speech: Left",
             "Noise: Binaural<br>Speech: Left",
             "Noise: Binaural<br>Speech: Binaural",
             "Noise: Binaural<br>Speech: Right",
             "Noise: Right<br>Speech: Right"]
        y = []

        mask = df["order"] == run_ID
        df_mask = df[mask].reset_index(drop=True)

        y.append(df_mask.at[0, "sp_l_no_l"])
        y.append(df_mask.at[0, "sp_l_no_bin"])
        y.append(df_mask.at[0, "sp_bin_no_bin"])
        y.append(df_mask.at[0, "sp_r_no_bin"])
        y.append(df_mask.at[0, "sp_r_no_r"])

        return x, y

    def plot_mtx(path, df, filename, run_ID):
        """
        INPUTS
        -path: path to the result folder: [repo_root]/results/
        -df: pandas dataframe containing the data to plot
        -filename: .tsv file name to be used to extract test information
        -run_ID: language ID (first or second language of the participant)
        OUTPUTS
        -saves PTA graphs in .html
        """

        title, ID, session, language = generate_title_mtx(df, filename, run_ID)
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

        x, y = data_to_plot(df, run_ID)
        #print(x, y)

        fig.add_trace(go.Scatter(x=x,
                                 y=y,
                                 mode='lines+markers',
                                 name=labels["title"],
                                 hovertemplate="%{x}<br>" +
                                               "%{y:0.1f} dB"))

#        elif side == "L":
#            frequency_L, value_L = data_to_plot(df, "L")
#            #print(value_L)

#            fig.add_trace(go.Scatter(x=frequency_L,
#                                     y=value_L,
#                                     line_color="blue",
#                                     mode='lines+markers',
#                                     name=ear,
#                                     hovertemplate="%{x:1.0f} Hz<br>" +
#                                                   "%{y:1.0f} dB HL"))

#        elif side == "Both":
#            frequency_R, value_R = data_to_plot(df, "R")
#            #print(value_R)
#            frequency_L, value_L = data_to_plot(df, "L")
#            #print(value_L)

#            fig.add_trace(go.Scatter(x=frequency_R,
#                                     y=value_R,
#                                     line_color="red",
#                                     mode='lines+markers',
#                                     name="Right ear",
#                                     hovertemplate="%{x:1.0f} Hz<br>" +
#                                                   "%{y:1.0f} dB HL"))

#            fig.add_trace(go.Scatter(x=frequency_L,
#                                     y=value_L,
#                                     line_color="blue",
#                                     mode='lines+markers',
#                                     name="Left ear",
#                                     hovertemplate="%{x:1.0f} Hz<br>" +
#                                                   "%{y:1.0f} dB HL"))

#        fig.show()

        completed = save_graph(fig, language, path, ID, session)

        if completed is True:
            return True
        else:
            return False

###############################################################################

#        """
#        INPUTS
#        -df: pandas dataframe containing the data to plot
#        -run_ID: specifies if it is the first or second language
#        OUTPUTS
#        -saves mtx graphs in .html
#        """

#        if run_ID == "L1":
#            prefix = "MTX1_"
#        elif run_ID == "L2":
#            prefix = "MTX2_"

#        language = extract_language(df, run_ID)
#        language_ID = run_ID + ": " + language
#        no_lang_df = df.drop(labels=f"{prefix}LANG", axis=1)
#        title = generate_title_run_MTX(df, run_ID, df.index[0])
#        labels = {"title": title,
#                  "x": "Test Condition",
#                  "y": "50% Comprehension Threshold (dB)"}

#        fig = go.Figure()

#        fig.update_layout(title=labels["title"],
#                          xaxis_title=labels["x"],
#                          yaxis_title=labels["y"],
#                          yaxis_range=[-15, 5],
#                          yaxis_dtick=5,
#                          xaxis_showline=True,
#                          xaxis_linecolor="black",
#                          yaxis_showline=True,
#                          yaxis_linecolor="black",
#                          yaxis_zeroline=True,
#                          yaxis_zerolinewidth=1,
#                          yaxis_zerolinecolor="black")

#        x, y = data_to_plot_MTX(no_lang_df, prefix)

#        fig.add_trace(go.Scatter(x=x,
#                                 y=y,
#                                 mode='lines+markers',
#                                 name=labels["title"],
#                                 hovertemplate="%{x}<br>" +
#                                               "%{y:0.1f} dB"))

#        completed = save_graph_MTX(path, fig, df, language_ID)

#        if completed is True:
#            return True
#        else:
#            return False

###############################################################################

#    def plot_mtx_subject(path, df, run_ID, display=False):
#        """
#        INPUTS
#        -df: pandas dataframe containing the data to plot
#        -run_ID: specifies if it is the first or second language
#        OUTPUTS
#        -saves mtx graphs in .html
#        """

#        if run_ID == "L1":
#            prefix = "MTX1_"
#        elif run_ID == "L2":
#            prefix = "MTX2_"

#        language_title = extract_language(df, run_ID)
#        language_ID_title = run_ID + ": " + language_title
#        language_ID_save = run_ID + "_" + language_title + "_All_runs"
#        no_lang_df = df.drop(labels=f"{prefix}LANG", axis=1)
#        title_graph = (gf.generate_title_graph(df, "MTX") + " ("
#                       + language_ID_title + ")")
#        labels = {"title": title_graph,
#                  "x": "Test Condition",
#                  "y": "50% Comprehension Threshold (dB)"}

#        fig = go.Figure()

#        fig.update_layout(title=labels["title"],
#                          xaxis_title=labels["x"],
#                          yaxis_title=labels["y"],
#                          yaxis_range=[-15, 5],
#                          yaxis_dtick=5,
#                          xaxis_showline=True,
#                          xaxis_linecolor="black",
#                          yaxis_showline=True,
#                          yaxis_linecolor="black",
#                          yaxis_zeroline=True,
#                          yaxis_zerolinewidth=1,
#                          yaxis_zerolinecolor="black")

#        for i in range(0, len(df)):
#            x, y = data_to_plot_MTX(no_lang_df.loc[[i]], prefix)

#            title_run = generate_title_run_MTX(df, run_ID, i)

#            fig.add_trace(go.Scatter(x=x,
#                                     y=y,
#                                     mode='lines+markers',
#                                     name=title_run,
#                                     hovertemplate="%{x}<br>" +
#                                                   "%{y:0.1f} dB"))

#        if display is True:
#            fig.show()
#        else:
#            completed = save_graph_MTX(path, fig, df, language_ID_save)

#            if completed is True:
#                return True
#            else:
#                return False
