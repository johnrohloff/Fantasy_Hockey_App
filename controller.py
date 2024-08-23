import dash
import plotly.express as px
from dash import dcc
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
             Input(component_id='select_stat', component_property='value'),
             Input(component_id='slider_value', component_property='value')
             ]
        )
        def update_graph(data_selected, year_selected, graph_selected, team_selected, position_selected,
                         stat_selected, slider_val):
            """
            Updates the output_container based on the selected choice
            :param data_selected:
            :return: Selected choice
            """
            fig = {}
            container = f' Real Data: {data_selected}, Year Selected: {year_selected}, Graph Selected: {graph_selected}' \
                        f'Teams Selected: {team_selected}, Position: {position_selected}, Stat: {stat_selected},' \
                        f' Slider: {slider_val}'

            #Data set for the selected year
            dfs = self.model.get_df(year_selected)

            #Filter by teams
            if team_selected:
                dfs = dfs[dfs['team'].isin(team_selected)]

            #Filter by position
            if position_selected:
                dfs = dfs[dfs['position'].isin(position_selected)]

            #Graphs for real statistics
            if data_selected:
                if graph_selected == 'bar':
                    selected_result = dfs.nlargest(slider_val, stat_selected)
                    fig = px.bar(
                        selected_result,
                        x='name',
                        y=stat_selected,
                        title=f'Top 10 {position_selected} Ranked By {stat_selected.capitalize()}'
                    )

                #Scatter plot chart
                elif graph_selected == 'scatter':
                    selected_result = dfs.nlargest(slider_val, stat_selected)
                    fig = px.scatter(
                        selected_result,
                        x='name',
                        y=stat_selected,
                        title=f'Top 5 {position_selected} Ranked By {stat_selected.capitalize()}'
                    )

            print(container)
            return dcc.Graph(figure=fig)

        #Callback to update stat_options based on the selected filter (All, PP, PK)
        @self.app.callback(
            Output(component_id='select_stat', component_property='options'),
            [Input(component_id='select_stat_filter', component_property='value')]
        )
        #Returns the selectable options based on the situation
        def update_stat_options(stat_filter_selected):
            if stat_filter_selected == 'all_situations':
                return self.model.all_options
            elif stat_filter_selected == 'powerplay':
                return self.model.pp_options
            elif stat_filter_selected == 'penalty_kill':
                return self.model.pk_options
            else:
                return []

        #Callback to update the slider value based on the graph
        @self.app.callback(
            Output(component_id='slider_value', component_property='marks'),
            Output(component_id='slider_value', component_property='max'),
            Output(component_id='slider_value', component_property='min'),
            Output(component_id='slider_value', component_property='step'),
            [Input(component_id='select_graph', component_property='value')]
        )
        #Changes the range of values for bar/scatter graphs
        def update_slider_val(select_graph):
            if select_graph == 'bar':
                marks_val = {i: str(i) for i in range(0, 101, 10)}
                max_val = 100
                min_val = 0
                step_val = 10
            else:
                marks_val = {i: str(i) for i in range(0, 501, 50)}
                max_val = 500
                min_val = 0
                step_val = 50
            return marks_val, max_val, min_val, step_val
