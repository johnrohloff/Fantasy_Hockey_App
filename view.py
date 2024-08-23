import dash
from dash import dcc
from dash import html

import model
import view


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

                # Select Real Data or Fantasy Hockey Data
                dcc.RadioItems(id="select_data",
                               options=[
                                   {"label": "Real Statistics", "value": True},
                                   {"label": "Fantasy Hockey", "value": False}
                               ],
                               value=True,
                               style={'width': "20%", 'display': 'inline-block'}
                               ),

                #Dropdown for the statistical year
                html.Div(id="year_block",
                         children=[
                             html.H5("Select Year", style={'margin-top': '1px'}),
                             dcc.Dropdown(id="select_year",
                                          options=[
                                              {"label": "2022-2023", "value": '2022'},
                                              {"label": "2023-2024", "value": '2023'},
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

                # Statistic to show (ie. Points/Goals/Assists)
                html.Div(id="select_stats_block",
                         children=[
                             html.H5("Select Stats", style={'margin-top': '1px'}),
                             dcc.Dropdown(id="select_stat",
                                          options=self.model.all_options,
                                          multi=False,
                                          value='points',
                                          ),
                         ], style={'width': "20%", 'display': 'inline-block'}
                         ),

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

