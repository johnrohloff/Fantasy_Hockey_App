import pandas as pd

class NHLModel:
    def __init__(self, files):
        """
        Initialize NHLModel with a list of files

        :param files: A list of CSV file names containing nhl player data, to be loaded into data frames
        """
        self.files = files
        self.dfs = self.load_dfs()

    def load_dfs(self):
        """
        Loads each CSV file into their respective data frame
        :return dict: A dictionary, Keys: File names , Values: CSV dataframe
        """
        return {file: pd.read_csv(f'{file}.csv') for file in self.files}

    def get_df(self,file):
        """
        Gets the dataframe based on the specified key name

        :param file: File name (String) without .csv extension
        :return: Returns the dataframe of the selected file name
        """
        return self.dfs.get(file)


