import pandas as pd


if __name__ == "__main__":
    print("This script is not designed to be used as a standalone script. "
          "Please use graph_generator.py to call it.")

else:
    def eliminate_row(df, column_to_search, value_to_search):
        """
        INPUTS
        -df: pandas dataframe to modify
        -column_to_search: takes a column name where to search for a specific
                           value
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

    def eliminate_column(df, prefix_to_keep):
        """
        INPUTS
        -df: pandas dataframe to modify
        -prefix_to_keep: takes a column name's prefix for the columns to keep
                         (will drop every column that doesn't start with it)
        OUPUT
        -returns a dataframe where the unnecessary columns have been eliminated
        """

        column_names = df.columns
        to_drop = []

        for i in column_names:
            if i.startswith(prefix_to_keep):
                continue
            else:
                to_drop.append(i)

        df = df.drop(to_drop, axis=1)

        return df

    def extract_subject(df, subject):
        """
        INPUTS
        -df: dataframe containing all the tests
        -subject: ID of the participant to isolate
        OUTPUTS
        -returns a dataframe containing only the sessions linked
         to the ID provided
        """

        mask = df["Participant_ID"] == subject
        df_sub = df[mask].reset_index(drop=True)

        return df_sub

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
        -df: dataframe with the informations to generate the title for a
             multiple runs graph
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
            print("ERROR: The test parameter passed to the "
                  "generate_title_graph function is not valid.")

        return title
