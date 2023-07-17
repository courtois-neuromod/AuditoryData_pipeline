import os
import matplotlib.pyplot as plt

from src import graph_functions as gf


if __name__ == "__main__":
    print("This script is not designed to be used as a standalone script. "
          "Please use graph_generator.py to call it.")

else:
    def generate_title_teoae(df, ear, filename):
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

        title = (ID + " - " + name + ": TEOAE (" + ear + ")")

        return title, ls_sub[1], ls_ses[1]

    def plot_teoae(path, df, side, filename):
        """
        INPUTS
        -path: path to the result folder: [repo_root]/results/
        -df: pandas dataframe containing the data to plot
        -side: side of the ear linked to the data in the df
        -filename: .tsv file name to be used to extract test information
        OUTPUTS
        -saves TEOAE graphs in .html
        """

        if side == "R":
            ear = "Right Ear"
        elif side == "L":
            ear = "Left Ear"

        title, ID, session = generate_title_teoae(df, ear, filename)
        labels = {"title": title,
                  "x": "Frequency (Hz)",
                  "y": "OAE response (dB SPL)"}

        x_data, y_data = gf.data_to_plot_oae(df, "freq", "oae")
        x_noise, y_noise = gf.data_to_plot_oae(df, "freq", "noise")
        y_floor = [-25, -25, -25, -25, -25]

        plt.figure(figsize=(11, 8.5), dpi=250)
        plt.plot(x_data, y_data, label="TEOAE response", color="c")
        plt.plot(x_noise, y_noise, label="Noise level", color="r")

        plt.axis([900, 5000, -20, 20])
        plt.grid()
        plt.xscale("log")
        plt.title(labels["title"])
        plt.xlabel(labels["x"])
        plt.ylabel(labels["y"])
        plt.legend()

        plt.fill_between(x=x_data, y1=y_data, y2=y_floor, color="c")
        plt.fill_between(x=x_noise, y1=y_noise, y2=y_floor, color="r")

        sub = "sub-" + ID
        folder = os.path.join(path, "graphs", sub)
        filename = ("Sub-" + ID + "_TEOAE_Session-" + session
                    + "_(" + ear + ").png")

        save_path = os.path.join(folder, filename)

        plt.savefig(save_path)
        plt.close()
        
        return True
