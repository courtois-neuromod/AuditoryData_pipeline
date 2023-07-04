import os
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter


if __name__ == "__main__":
    print("This script is not designed to be used as a standalone script. "
          "Please use graph_generator.py to call it.")

else:
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
        ls_sub = ls_filename[0].split("-")
        ls_ses = ls_filename[1].split("-")

        ID = "Sub" + ls_sub[1]
        name = "Session " + ls_ses[1]

        title = (ID + " - " + name + ": DPOAE (" + ear + ")")

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

        x_data, y_data = data_to_plot(df, "dp")
        x_2sd, y_2sd = data_to_plot(df, "noise+2sd")
        x_1sd, y_1sd = data_to_plot(df, "noise+1sd")
        y_floor = [-25, -25, -25, -25, -25, -25, -25, -25]

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
        plt.title(labels["title"])
        plt.xlabel(labels["x"])
        plt.ylabel(labels["y"])
        plt.legend()

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
