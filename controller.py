import dash
import plotly.express as px
from dash.dependencies import Input, Output

import model


class NHLController:
    def __init__(self,app, model, view):
        """
        Initialize NHLController class

        Sets up the connection between app, model and view
        :param app: Dash app instance
        :param model: NHLModel instance which contains data, getters, setters
        :param view: NHLView instance which contains the UI

        """
        self.app = app
        self.model = model
        self.view = view
        self.register_callbacks()

    def register_callbacks(self):
        """
        Handles callbacks for the Dash app

        :return: None
        """
        @self.app.callback(
            Output(component_id='output_container', component_property='children'),
            [Input(component_id='select_data', component_property='value'),
             Input(component_id='select_year', component_property='value'),
             Input(component_id='select_graph', component_property='value'),
             Input(component_id='select_teams', component_property='value'),
             Input(component_id='select_position', component_property='value'),

             ]
        )

        def update_graph(data_selected, year_selected, graph_selected, team_selected, position_selected):
            """
            Updates the output_container based on the selected choice
            :param data_selected:
            :return: Selected choice
            """

            container = f' Real Data: {data_selected}, Year Selected: {year_selected}, Graph Selected: {graph_selected}' \
                        f'Teams Selected: {team_selected}, Position: {position_selected}'

            #Grab the data for the selected year
            if year_selected is not None:
                dfs = self.model.get_df(year_selected)
            else:
                dfs = None

            if team_selected in self.model.teams:
                return team_selected

            print(dfs)
            print(container)
            return data_selected, year_selected
