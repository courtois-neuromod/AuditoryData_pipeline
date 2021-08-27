import numpy as np
import plotly.graph_objects as go


def eliminate_row(df, column_to_search, value_to_search):
    """
    INPUTS
    -df: pandas dataframe to modify
    -column_to_search: takes a column name where to search for a specific value
    -value_to_search: takes a value to search in the specified column
    OUPUT
    -returns a dataframe where the unnecessary rows have been eliminated
    """

    to_drop = []

    for i in range(0, len(df)):
        if df[column_to_search][i] == value_to_search:
            to_drop.append(i)
        else:
            continue

    df = df.drop(to_drop, axis=0)
    df = df.reset_index(drop=True)

    return df


def extract_subject(df, subject):
    """
    INPUTS
    -df: dataframe containing all the tests
    -subject: ID of the participant to isolate
    OUTPUTS
    -returns a dataframe containing only the sessions linked to the ID provided
    """

    mask = df["Participant_ID"] == subject
    df_sub = df[mask].reset_index(drop=True)

    return df_sub


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


def save_graph_PTA(graph, df, ear):
    """
    INPUTS
    -graph: interactive plotly.graph_objects figure
    -df: dataframe with the informations that were used to generate the graph
    -ear: ear side linked with the graph
    OUTPUTS
    -saves the graph in a .html file to a subject's specific location in the
     repository
    """

    test = "PTA"

    row = df.index[0]

    sub = df["Participant_ID"][row]
    sub_short = sub.lstrip("Sub")
    sub_long = "sub-" + sub_short

    folder = "../results/graphs/" + sub_long + "/"
    path_header = folder + "Sub-" + sub_short + "_" + test + "_"

    if ear == "All_runs":
        path = path_header + ear + ".html"

    else:
        session = df["DATE"][row]
        name = df["Protocol name"][row]
        condition = df["Protocol condition"][row]

        path = (path_header + session + "_" + name + ": " + condition
                + " (" + ear + ")" + ".html")

    graph.write_html(path)

    return True


def save_graph_MTX(graph, df, language_ID):
    """
    INPUTS
    -graph: interactive plotly.graph_objects figure
    -df: dataframe with the informations that were used to generate the graph
    -language_ID: specifies if it is the L1 or L2 and which language was used
    OUTPUTS
    -saves the graph in a .html file to a subject's specific location in the
     repository
    """

    test = "MTX"

    row = df.index[0]

    sub = df["Participant_ID"][row]
    sub_short = sub.lstrip("Sub")
    sub_long = "sub-" + sub_short

    folder = "../results/graphs/" + sub_long + "/"
    path_header = folder + "Sub-" + sub_short + "_" + test + "_"

    if language_ID.endswith("_All_runs") is True:
        path = path_header + language_ID + ".html"

    else:
        session = df["DATE"][row]
        name = df["Protocol name"][row]
        condition = df["Protocol condition"][row]

        path = (path_header + session + "_" + name + ": " + condition + " ("
                + language_ID + ")" + ".html")

    graph.write_html(path)

    return True


def return_130(df, to_search):
    """
    INPUTS
    -df: takes a one row dataframe to scan for the value 130 (PTA's
         "no response" marker)
    -to_search: list of column names in which the fct has to look in
    OUTPUTS
    -returns a list of the columns containing the value 130
    """

    index_value = df.index[0]
    to_drop = []

    for i in to_search:
        if df[i][index_value] == 130:
            to_drop.append(to_search.index(i))
        else:
            continue

    return to_drop


def generate_title_graph(df, test):
    """
    INPUTS
    -df: dataframe with the informations to generate the title for a multiple
         runs graph
    OUTPUTS
    -returns a string to use as a title for the graph to generate
    """

    row = df.index[0]
    ID = df["Participant_ID"][row]

    if test == "PTA":
        title = ID + " - " + "Pure-Tone Audiometry"
    elif test == "MTX":
        title = ID + " - " + "Matrix Speech-in-Noise Perception Test"
    else:
        print("ERROR: The test parameter passed to the generate_title_graph "
              "function is not valid.")

    return title


def generate_title_run_PTA(df, ear, index):
    """
    INPUTS
    -df: dataframe with the informations to generate the title for a single run
    -ear: ear side linked with the title
    OUTPUTS
    -returns a string to use as a title for the graph to generate
    """

    ID = df["Participant_ID"][index]
    name = df["Protocol name"][index]
    condition = df["Protocol condition"][index]

    title = ID + " - " + "PTA, " + name + ": " + condition + " (" + ear + ")"

    return title


def generate_title_run_MTX(df, run_ID, index):
    """
    INPUTS
    -df: dataframe with the informations to generate the title for a single run
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


def data_to_plot_PTA(df, prefix):
    """
    INPUTS
    -df: one line dataframe from which this function extract the data to plot
    -prefix: str marker pointing to the columns containing the relevant data
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

    list_130 = return_130(df, to_search)

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


def data_to_plot_MTX(df, prefix):
    """
    INPUTS
    -df: one line dataframe from which this function extracts the data to plot
    -prefix: str marker pointing to the columns containing the relevant data
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


def plot_pta_L(df):
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

    completed = save_graph_PTA(fig, df, "Left Ear")

    if completed is True:
        return True
    else:
        return False


def plot_pta_R(df):
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

    completed = save_graph_PTA(fig, df, "Right Ear")

    if completed is True:
        return True
    else:
        return False


def plot_pta_subject(df, display=False):
    """
    INPUTS
    -df: pandas dataframe containing the data to plot
    OUTPUTS
    -saves pta graph in .html
    """

    title_graph = generate_title_graph(df, "PTA")
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
        completed = save_graph_PTA(fig, df, "All_runs")

        if completed is True:
            return True
        else:
            return False


def plot_mtx(df, run_ID):
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

    completed = save_graph_MTX(fig, df, language_ID)

    if completed is True:
        return True
    else:
        return False


def plot_mtx_subject(df, run_ID, display=False):
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
    title_graph = (generate_title_graph(df, "MTX") + " ("
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
        completed = save_graph_MTX(fig, df, language_ID_save)

        if completed is True:
            return True
        else:
            return False
