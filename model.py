import pandas as pd

class NHLModel:
    def __init__(self, files):
        """
        Initialize NHLModel with a list of files

        :param files: A list of CSV file names containing nhl player data, to be loaded into data frames
        """
        #List of files given to the model
        self.files = files

        #Data frames of each year
        self.dfs = [pd.read_csv(f'{file}.csv') for file in self.files]
        self.teams = self.dfs[0]['team'].unique().tolist()
        self.positions = self.dfs[0]['position'].unique().tolist()

    def get_df(self,year):
        """
        Gets the dataframe based on the specified key name

        :param file: File name (String) without .csv extension
        :return: Returns the dataframe of the selected file name
        """
        if year == '2022':
            return self.dfs[0]
        elif year == '2023':
            return self.dfs[1]
        else:
            return None


