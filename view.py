import dash
from dash import dcc
from dash import html


class NHLView:
    def __init__(self, nhl_model, fantasy_model):
        """
        Initializes the NHLView class which creates the Dash application layout

        This class is responsible for creating and formatting the different components
        that develop and modify the Dash application's visual UI.

        Parameters:
        nhl_model: NHLModel
            Model containing real NHL player statistics + team information
        fantasy_model: FantasyModel
            Model containing fantasy scoring data sets and scoring settings
        """
        self.nhl_model = nhl_model
        self.fantasy_model = fantasy_model
        self.layout = self.create_layout()

    def create_layout(self):
        """
        This function generates the layout of the Dash application by creating
        the dropdowns, labels, headers etc...

        Returns:
            html.Div: A Dash Html Div component that contains the application's layout
        """
        return html.Div([
            # Header
            html.H1("NHL Player Statistics", style={'text-align': 'center'}),

            # All UI Blocks
            html.Div([

                html.Div(id="data_block",
                         children=[
                             html.H5("Data Displayed:", style={'margin-top': '1px'}),
                             dcc.Dropdown(id="select_data",
                                          options=[
                                              {"label": "Real Statistics", "value": True},
                                              {"label": "Fantasy Hockey", "value": False}
                                          ],
                                          multi=False,
                                          value=True,
                                          ),
                         ], style={'width': "20%", 'display': 'inline-block'}
                         ),

                #Dropdown for the statistical year
                html.Div(id="year_block",
                         children=[
                             html.H5("Select Year", style={'margin-top': '1px'}),
                             dcc.Dropdown(id="select_year",
                                          options=[
                                              {"label": "2023-2024", "value": '2024'},
                                              {"label": "2022-2023", "value": '2023'},
                                              {"label": "2021-2022", "value": '2022'},
                                              {"label": "2020-2021", "value": '2021'},
                                              {"label": "2019-2020", "value": '2020'},

                                          ],
                                          multi=False,
                                          value="2024",
                                          ),
                         ], style={'width': "20%", 'display': 'inline-block'}
                         ),

                #Graph dropdown
                html.Div(id="graph_block",
                         children=[
                             html.H5("Select Graph", style={'margin-top': '1px'}),
                             dcc.Dropdown(id="select_graph",
                                          options=[
                                              {"label": "Bar", "value": "bar"},
                                              {"label": "Scatter", "value": "scatter"}
                                          ],
                                          multi=False,
                                          value="bar",
                                          ),
                         ], style={'width': "20%", 'display': 'inline-block'}
                         ),

                #Dropdown of teams
                html.Div(id="teams_block",
                         children=[
                             html.H5("Select Teams", style={'margin-top': '1px'}),
                             dcc.Dropdown(id="select_teams",
                                          options=[
                                              {"label": team, "value": team} for team in self.nhl_model.teams
                                          ],
                                          multi=True,
                                          placeholder="All Teams",
                                          # style={'width': "40%", 'display':'inline-block'}
                                          ),
                         ], style={'width': "20%", 'display': 'inline-block'}
                         ),

                # Dropdown of positions
                html.Div(id="positions_block",
                         children=[
                             html.H5("Select Positions", style={'margin-top': '1px'}),
                             dcc.Dropdown(id="select_position",
                                          options=[
                                              {"label": pos, "value": pos} for pos in self.nhl_model.positions
                                          ],
                                          multi=True,
                                          placeholder="All Positions",
                                          ),
                         ], style={'width': "20%", 'display': 'inline-block'}
                         ),

                # Statistic to show (ie. Points/Goals/Assists)
                html.Div([
                html.Div(id="select_stats_block",
                         children=[
                             html.H5("Select Stats", style={'margin-top': '1px'}),
                             dcc.Dropdown(id="select_stat",
                                          options=[],
                                          multi=False,
                                          value='points',
                                          ),
                         ], style={'width': "20%", 'display': 'inline-block'}
                         ),

                #2nd Statistic to show (ie. Points/Goals/Assists)
                html.Div(id="select_stats_block2",
                         children=[
                             html.H5("Stat 2", style={'margin-top': '1px'}),
                             dcc.Dropdown(id="select_stat2",
                                          options=[],
                                          multi=False,
                                          value='points',
                                          ),
                         ], style={'width': "20%", 'display': 'none'}
                         ),
                    ]),

                #Fantasy Scoring Inputs
                html.Div(id='fantasy_scores_block', style={'width': "20%", 'display': 'none'},
                         children=[
                             html.H3("Fantasy Scoring Values", style={'text-align': 'center'}),

                             # Row 1 Fantasy Data (Shooting)
                             html.Div([
                                 html.H5("5on5 Goal:", style={'margin-right': '5px'}),
                                 dcc.Input(id='f_goal',
                                           type='number',
                                           value=self.fantasy_model.f_scoring['f_goal'],
                                           style={'width': '20%', 'display': 'inline-block', 'margin-right': '10px'}
                                           ),

                                 html.H5("PPG:", style={'margin-right': '5px'}),
                                 dcc.Input(id='f_ppg',
                                           type='number',
                                           value=self.fantasy_model.f_scoring['f_ppg'],
                                           style={'width': '20%', 'display': 'inline-block', 'margin-right': '10px'}
                                           ),

                                 html.H5("SHG:", style={'margin-right': '5px'}),
                                 dcc.Input(id='f_shg',
                                           type='number',
                                           value=self.fantasy_model.f_scoring['f_shg'],
                                           style={'width': '20%', 'display': 'inline-block', 'margin-right': '10px'}
                                           ),

                                 html.H5("SOG:", style={'margin-right': '5px'}),
                                 dcc.Input(id='f_sog',
                                           type='number',
                                           value=self.fantasy_model.f_scoring['f_sog'],
                                           style={'width': '20%', 'display': 'inline-block', 'margin-right': '10px'}
                                           )

                             ], style={'display': 'flex', 'align-items': 'center'}
                             ),

                             #Row 2 Fantasy Data (Play Making)
                             html.Div([
                                 html.H5("5on5 Assist:", style={'margin-right': '5px'}),
                                 dcc.Input(id='f_assist',
                                           type='number',
                                           value=self.fantasy_model.f_scoring['f_assist'],
                                           style={'width': '20%', 'display': 'inline-block', 'margin-right': '10px'}
                                           ),

                                 html.H5("PPA:", style={'margin-right': '5px'}),
                                 dcc.Input(id='f_ppa',
                                           type='number',
                                           value=self.fantasy_model.f_scoring['f_ppa'],
                                           style={'width': '20%', 'display': 'inline-block', 'margin-right': '10px'}
                                           ),

                                 html.H5("SHA:", style={'margin-right': '5px'}),
                                 dcc.Input(id='f_sha',
                                           type='number',
                                           value=self.fantasy_model.f_scoring['f_sha'],
                                           style={'width': '20%', 'display': 'inline-block', 'margin-right': '10px'}
                                           ),

                                 html.H5("Faceoff Wins:", style={'margin-right': '5px'}),
                                 dcc.Input(id='f_faceoff_win',
                                           type='number',
                                           value=self.fantasy_model.f_scoring['f_faceoff_win'],
                                           style={'width': '20%', 'display': 'inline-block', 'margin-right': '10px'}
                                           )
                             ], style={'display': 'flex', 'align-items': 'center'}
                             ),

                             # Row 3 Fantasy Data (Other/Physical)
                             html.Div([
                                 html.H5("Takeaways:", style={'margin-right': '5px'}),
                                 dcc.Input(id='f_takeaway',
                                           type='number',
                                           value=self.fantasy_model.f_scoring['f_takeaway'],
                                           style={'width': '20%', 'display': 'inline-block', 'margin-right': '10px'}
                                           ),

                                 html.H5("Giveaways:", style={'margin-right': '5px'}),
                                 dcc.Input(id='f_giveaway',
                                           type='number',
                                           value=self.fantasy_model.f_scoring['f_giveaway'],
                                           style={'width': '20%', 'display': 'inline-block', 'margin-right': '10px'}
                                           ),

                                 html.H5("Hits:", style={'margin-right': '5px'}),
                                 dcc.Input(id='f_hit',
                                           type='number',
                                           value=self.fantasy_model.f_scoring['f_hit'],
                                           style={'width': '20%', 'display': 'inline-block', 'margin-right': '10px'}
                                           ),

                                 html.H5("Blocks:", style={'margin-right': '5px'}),
                                 dcc.Input(id='f_block',
                                           type='number',
                                           value=self.fantasy_model.f_scoring['f_block'],
                                           style={'width': '20%', 'display': 'inline-block', 'margin-right': '10px'}
                                           )
                             ], style={'display': 'flex', 'align-items': 'center'}
                             ),
                         ]),

                # Slider to represent number of players
                html.H5("Select Num. Players", style={'margin-top': '1px'}),
                html.Div([
                    dcc.Slider(
                               id='slider_value',
                               value=20,
                               marks={i: str(i) for i in range(0, 1001, 50)},
                               min=0,
                               max=1000,
                               step=50,
                               tooltip={"placement": "bottom", "always_visible": True}
                               )
                ], id='slider_container'),

                html.Div(id='output_container')
            ])
        ])

    def create_app(self):
        """
        Creates + Returns a Dash app instance

        Returns:
            app: A configured Dash app instance
        """
        app = dash.Dash(__name__)
        app.layout = self.layout
        return app
