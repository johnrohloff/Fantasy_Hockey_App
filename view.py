import dash
from dash import dcc
from dash import html

import model


class NHLView:
    def __init__(self,model):
        """
        Initializes the NHLView class
        And stores the layout of the application and stores it in the layout attribute.
        """
        self.model = model
        self.layout = self.create_layout()


    def create_layout(self):
        """
        Creates the layout of the Dash application
        :return:
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
                                              {"label": "2023-2024", "value": '2023'},
                                              {"label": "2022-2023", "value": '2022'},
                                          ],
                                          multi=False,
                                          placeholder="Select Year",
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
                                          placeholder="Select Graph Type",
                                          ),
                         ], style={'width': "20%", 'display': 'inline-block'}
                         ),

                #Dropdown of teams
                html.Div(id="teams_block",
                         children=[
                             html.H5("Select Teams", style={'margin-top': '1px'}),
                             dcc.Dropdown(id="select_teams",
                                          options=[
                                              {"label": team, "value": team} for team in self.model.teams
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
                                              {"label": pos, "value": pos} for pos in self.model.positions
                                          ],
                                          multi=True,
                                          placeholder="All Positions",
                                          ),
                         ], style={'width': "20%", 'display': 'inline-block'}
                         ),

                # Filter stats based on situations (5v5, 5v4, 4v5)
                html.Div(id="stat_filter_block",
                         children=[
                             html.H5("Select Stat Filter", style={'margin-top': '1px'}),
                             dcc.Dropdown(id="select_stat_filter",
                                          options=[
                                              {"label": "All", "value": "all_situations"},
                                              {"label": "Powerplay", "value": "powerplay"},
                                              {"label": "Penalty Kill", "value": "penalty_kill"}
                                          ],
                                          multi=False,
                                          value='all_situations',
                                          ),
                         ], style={'width': "20%", 'display': 'inline-block'}
                         ),

                # Statistic to show (ie. Points/Goals/Assists)
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
        :return:
        """
        app = dash.Dash(__name__)
        app.layout = self.layout
        return app

