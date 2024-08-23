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

        # Selectable stats for all situations (5v5, 5v4, 4v5...)
        self.all_options = [
            {"label": "Points", "value": "points"},
            {"label": "Goals", "value": "goals"},
            {"label": "Assists", "value": "assists"},
            {"label": "Shots", "value": "shots_on_goal"},
            {"label": "Takeaways", "value": "takeaways"},
            {"label": "Giveaways", "value": "giveaways"},
            {"label": "Blocked Shots", "value": "blocked_shots"},
            {"label": "Hits", "value": "hits"},
            {"label": "Penalty Mins", "value": "penalty_mins"},
            {"label": "Penalties Drawn", "value": "penaltiesdrawn"}
        ]

        #Selectable stats for powerplay situations (5v4, 5v3...)
        self.pp_options = [{"label": "PP Points", "value": "pp_points"},
            {"label": "PP Goals", "value": "pp_goals"},
            {"label": "PP Assists", "value": "pp_assists"}]

        #Selectable stats for penalty kill situations (4v5, 3v5)
        self.pk_options = [{"label": "PK Points", "value": "pk_points"},
            {"label": "PK Goals", "value": "pk_goals"},
            {"label": "PK Assists", "value": "pk_assists"}]

    #Grabs the dataframe of the selected year
    def get_df(self,year):
        """
        Gets the dataframe based on the specified key name

        :param file: File name (String) without .csv extension
        :return: Returns the dataframe of the selected file name
        """
        if year == '2023':
            return self.dfs[0]
        elif year == '2022':
            return self.dfs[1]
        else:
            return None


