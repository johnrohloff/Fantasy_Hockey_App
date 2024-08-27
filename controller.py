import dash
import plotly.express as px
from dash import dcc
from dash.dependencies import Input, Output

import model
from model import NHLModel, FantasyModel


class NHLController:
    def __init__(self,app, nhl_model, fantasy_model, view):
        """
        Initialize NHLController class

        Sets up the connection between app, model and view
        :param app: Dash app instance
        :param model: NHLModel instance which contains data, getters, setters
        :param view: NHLView instance which contains the UI

        """
        self.app = app
        self.nhl_model = nhl_model
        self.fantasy_model = fantasy_model
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
             Input(component_id='select_stat2', component_property='value'),
             Input(component_id='slider_value', component_property='value'),]
            + [Input(component_id=label, component_property='value') for label in self.fantasy_model.f_labels]
        )
        def update_graph(data_selected, year_selected, graph_selected, team_selected, position_selected,
                         stat_selected, stat2_selected, slider_val, *f_inputs):
            """
            Updates the output_container based on the selected choice
            :param data_selected:
            :return: Selected choice
            """

            # Convert f_inputs to a dictionary if needed
            f_inputs_dict = dict(zip(self.fantasy_model.f_labels, f_inputs))

            # Update your model with the fantasy inputs
            updated_f_scoring = {label: value for label, value in f_inputs_dict.items()}
            self.fantasy_model.update_scoring(updated_f_scoring)


            fig = {}

            container = f' Real Data: {data_selected}, Year Selected: {year_selected}, Graph Selected: {graph_selected}' \
                        f'Teams Selected: {team_selected}, Position: {position_selected}, Stat: {stat_selected},' \
                        f' Stat 2: {stat2_selected}, Slider: {slider_val}'

            #Assign dataframe for the selected year
            dfs = self.nhl_model.get_df(year_selected)

            #Add on the fantasy statistics to the dataframe selected
            dfs = self.fantasy_model.calc_fantasy_stats(dfs, self.fantasy_model.f_scoring)

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
                        x=stat2_selected,
                        y=stat_selected,
                        title=f'Top 5 {position_selected} Ranked By {stat_selected.capitalize()}',
                        labels={'name': 'Player Name', stat_selected: stat_selected.capitalize()},
                        hover_data={'name': True},
                    )

            ###---- Fantasy hockey display ---- ####
            else:
                #Bar graph display
                if graph_selected == 'bar':
                    selected_result = dfs.nlargest(slider_val, stat_selected)
                    fig = px.bar(
                        selected_result,
                        x='name',
                        y=stat_selected,
                        title=f'Top 10 {position_selected} Ranked By {stat_selected.capitalize()}'
                    )
                #Scatter plot display
                elif graph_selected == 'scatter':
                    selected_result = dfs.nlargest(slider_val, stat_selected)
                    fig = px.scatter(
                       selected_result,
                       x=stat2_selected,
                       y=stat_selected,
                       title=f'Top 5 {position_selected} Ranked By {stat_selected.capitalize()}',
                       labels={'name': 'Player Name', stat_selected: stat_selected.capitalize()},
                       hover_data={'name': True},
                   )

            print(container)
            return dcc.Graph(figure=fig)

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

        #Callback for updating selectable dropdowns based on graph chosen
        @self.app.callback(
            Output(component_id='select_stat', component_property='options'),
            Output(component_id='select_stat2', component_property='options'),
            Output(component_id='select_stats_block2', component_property='style'),
            Output(component_id='fantasy_scores_block', component_property='style'),

            [Input(component_id='select_data', component_property='value'),
             Input(component_id='select_graph', component_property='value')]
        )
        #Show/Hide select_stat2 dropdown
        def update_dropdowns(select_data, select_graph):
            #Real data display
            if select_data:
                #Show bar graph dropdown format (1 Stat selection dropdown)
                if select_graph == 'bar':
                    return self.nhl_model.all_options, [], {'width': "20%", 'display': 'none'},\
                           {'width': "20%", 'display': 'none'}

                #Scatter plot display: (X,Y stat dropdowns)
                else:
                    return self.nhl_model.all_options, self.nhl_model.all_options, \
                           {'width': "20%", 'display': 'inline-block'}, {'width': "20%", 'display': 'none'}

            #Fantasy display
            else:
                #Bar Graph
                if select_graph == 'bar':
                    return self.fantasy_model.f_options, [], {'width': "20%", 'display': 'none'},\
                       {'width': "50%", 'display': 'inline-block'}
                #Scatter Plot
                else:
                    return self.fantasy_model.f_options, self.fantasy_model.f_options, \
                           {'width': "20%", 'display': 'inline-block'}, {'width': "20%", 'display': 'none'}