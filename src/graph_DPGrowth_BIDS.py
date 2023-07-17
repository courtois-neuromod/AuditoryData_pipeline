import os
import matplotlib.pyplot as plt

from src import graph_functions as gf


if __name__ == "__main__":
    print("This script is not designed to be used as a standalone script. "
          "Please use graph_generator.py to call it.")


else:
    def generate_title_growth(df, ear, filename):
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

        if df["freq2"][0] == 2002:
            frequency = "2 kHz"
        elif df["freq2"][0] == 4004:
            frequency = "4 kHz"
        elif df["freq2"][0] == 6006:
            frequency = "6 khz"

        title = (ID + " - " + name + ": DP growth, "
                 + frequency + " (" + ear + ")")
        #print(title)

        return title, ls_sub[1], ls_ses[1], frequency

    def plot_growth(path, df, side, filename):
        """
        INPUTS
        -path: path to the result folder: [repo_root]/results/
        -df: pandas dataframe containing the data to plot
        -side: side of the ear linked to the data in the df
        -filename: .tsv file name to be used to extract test information
        OUTPUTS
        -saves DP Growth graphs in .png
        """

        if side == "R":
            ear = "Right Ear"
            marker = "o"
        elif side == "L":
            ear = "Left Ear"
            marker = "x"

        title, ID, session, frequency = generate_title_growth(df,
                                                              ear,
                                                              filename)
        labels = {"title": title,
                  "x": "F2 frequency presentation level (dB SPL)",
                  "y": "OAE response (dB SPL)"}

        x_data, y_data = gf.data_to_plot_oae(df, "l2", "dp")
        x_2sd, y_2sd = gf.data_to_plot_oae(df, "l2", "noise+2sd")
        x_1sd, y_1sd = gf.data_to_plot_oae(df, "l2", "noise+1sd")
        y_floor = [-25, -25, -25, -25, -25, -25, -25]

        plt.figure(figsize=(11, 8.5), dpi=250)
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

        plt.axis([30, 80, -10, 30])
        plt.grid()
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
        frequency = frequency.replace(" ", "_")
        folder = os.path.join(path, "graphs", sub)
        filename = ("Sub-" + ID + "_Growth_" + frequency +"_Session-"
                    + session + "_(" + ear + ").png")

        save_path = os.path.join(folder, filename)

        plt.savefig(save_path)
        plt.close()
        
        return True
