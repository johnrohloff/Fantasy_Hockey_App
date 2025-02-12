import pandas as pd

class NHLModel:
    def __init__(self, files):
        """
        Initialize NHLModel with a list of files

        Parameters:
        files (list): A list of CSV file names containing nhl player data, to be loaded into data frames
                      Does NOT contain the '.csv' extension
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
            {"label": "Faceoffs Won", "value": "faceoffswon"},
            {"label": "Takeaways", "value": "takeaways"},
            {"label": "Giveaways", "value": "giveaways"},
            {"label": "Blocked Shots", "value": "blocked_shots"},
            {"label": "Hits", "value": "hits"},
            {"label": "Penalty Mins", "value": "penalty_mins"},
            {"label": "Penalties Drawn", "value": "penaltiesdrawn"},
            {"label": "PP Points", "value": "pp_points"},
            {"label": "PP Goals", "value": "pp_goals"},
            {"label": "PP Assists", "value": "pp_assists"},
            {"label": "PK Points", "value": "pk_points"},
            {"label": "PK Goals", "value": "pk_goals"},
            {"label": "PK Assists", "value": "pk_assists"}
        ]

    #Grabs the dataframe of the selected year
    def get_df(self,year):
        """
        Gets the dataframe of the specified year

        Parameters:
        year (str): The year of data we wish to use

        Returns:
        The dataframe of the selected year
        """

        match year:
            case'2024':
                return self.dfs[0]
            case '2023':
                return self.dfs[1]
            case '2022':
                return self.dfs[2]
            case '2021':
                return self.dfs[3]
            case '2020':
                return self.dfs[4]
            case _:
                return None


#Subclass of NHLModel, expands and uses the NHLModel data but also incorporates its own features
class FantasyModel(NHLModel):
    def __init__(self, files):
        """
        This class focuses on the fantasy section of the application and contains the data sets, labels, and
        values used by the view, controller.

        Parameters:
        files (string): The dataframe loaded in of a specific year
        """
        super().__init__(files)

        #Default fantasy scoring values
        self.f_scoring = {
            'f_goal': 2.0,
            'f_ppg': 1.0,
            'f_shg': 2.0,
            'f_sog': 0.3,
            'f_assist': 1.0,
            'f_ppa': 0.5,
            'f_sha': 1.0,
            'f_faceoff_win': 0.1,
            'f_takeaway': 0.2,
            'f_giveaway': -0.3,
            'f_hit': 0.1,
            'f_block': 0.3,
        }

        #List of independant fantasy input values, used for updating f_scoring
        self.f_labels = ['f_goal', 'f_ppg', 'f_shg','f_sog','f_assist','f_ppa','f_sha',
                         'f_faceoff_win','f_takeaway','f_giveaway','f_hit','f_block']

        self.f_categories = ['f_goals', 'f_ppgs', 'f_shgs','f_sogs','f_assists','f_ppas','f_shas',
                         'f_faceoff_wins','f_takeaways','f_giveaways','f_hits','f_blocks', 'f_points']

        # All selectable stats
        self.f_options = [
            {"label": "Points", "value": "f_points"},
            {"label": "Goals", "value": "f_goals"},
            {"label": "Assists", "value": "f_assists"},
            {"label": "Shots", "value": "f_sogs"},
            {"label": "Faceoffs Won", "value": "f_faceoff_wins"},
            {"label": "Takeaways", "value": "f_takeaways"},
            {"label": "Giveaways", "value": "f_giveaways"},
            {"label": "Blocked Shots", "value": "f_blocks"},
            {"label": "Hits", "value": "f_hits"},
            {"label": "PPG", "value": "f_ppgs"},
            {"label": "PPA", "value": "f_ppas"},
            {"label": "SHG", "value": "f_shgs"},
            {"label": "SHA", "value": "f_shas"},
        ]

    #Create new columns in our dataframe for fantasy scoring
    def calc_fantasy_stats(self, df, scoring):
        """
        This function creates new columns in the selected dataset representing fantasy values for each player.
        Each player's real statistics for the given df is multiplied by the scoring value set in the application

        Parameters:
        df: The dataframe containing a selected years NHL data
        scoring (dict): A dictionary of keys (Stat columns) and values (User defined scoring values)

        Returns:
        df: A dataframe with the new fantasy stats calculated appeneded
        """
        df['f_goals'] = df['goals'] * scoring['f_goal']
        df['f_ppgs'] = df['pp_goals'] * scoring['f_ppg']
        df['f_shgs'] = df['pk_goals'] * scoring['f_shg']
        df['f_sogs'] = df['shots_on_goal'] * scoring['f_sog']
        df['f_assists'] = df['assists'] * scoring['f_assist']
        df['f_ppas'] = df['pp_assists'] * scoring['f_ppa']
        df['f_shas'] = df['pk_assists'] * scoring['f_sha']
        df['f_faceoff_wins'] = df['faceoffswon'] * scoring['f_faceoff_win']
        df['f_takeaways'] = df['takeaways'] * scoring['f_takeaway']
        df['f_giveaways'] = df['giveaways'] * scoring['f_giveaway']
        df['f_hits'] = df['hits'] * scoring['f_hit']
        df['f_blocks'] = df['blocked_shots'] * scoring['f_block']
        df['f_points'] = df[['f_goals', 'f_ppgs', 'f_shgs','f_sogs','f_assists','f_ppas','f_shas',
                             'f_faceoff_wins','f_takeaways','f_giveaways','f_hits','f_blocks']].sum(axis=1)
        return df

    def update_scoring(self, scoring_values):
        """
        This function recalculates the fantasy scoring dictionary when given user inputted values

        Parameters:
        scoring_values (dict): The user given values to be used instead of the default values

        Returns:
            None
        """
        self.f_scoring.update(scoring_values)

