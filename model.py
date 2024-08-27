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


#Subclass of NHLModel, expands and uses the NHLModel data but also incorporates its own features
class FantasyModel(NHLModel):
    def __init__(self, files):
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

        # All selectable stats
        self.f_options = [
            {"label": "Points", "value": "f_points"},
            {"label": "Goals", "value": "f_goals"},
            {"label": "PPG", "value": "f_ppgs"},
            {"label": "SHG", "value": "f_shgs"},
            {"label": "Assists", "value": "f_assists"},
            {"label": "PPA", "value": "f_ppas"},
            {"label": "SHA", "value": "f_shas"},
            {"label": "Shots", "value": "f_sogs"},
            {"label": "Takeaways", "value": "f_takeaways"},
            {"label": "Giveaways", "value": "f_giveaways"},
            {"label": "Blocked Shots", "value": "f_blocks"},
            {"label": "Hits", "value": "f_hits"},
        ]

    #Create new columns in our dataframe for fantasy scoring
    def calc_fantasy_stats(self, df, scoring):
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
        return df

    #Default fantasy scores dictionary
    #Update fantasy scores function
    #
