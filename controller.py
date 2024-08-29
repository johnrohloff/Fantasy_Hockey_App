import dash
import plotly.express as px
from dash import dcc
from dash.dependencies import Input, Output

import model
from model import NHLModel, FantasyModel


class NHLController:
    def __init__(self, app, nhl_model, fantasy_model, view):
        """
        Initialize NHLController class

        Sets up the connection between app, model and view
        :param app: Dash app instance
        :param nhl_model: NHLModel instance, contains data, getters, setters for the real stats display
        :param fantasy_model: FantasyModel instance which contains data, getters, setters for the fantasy display
        :param view: NHLView instance which contains the UI

        """
        self.app = app
        self.nhl_model = nhl_model
        self.fantasy_model = fantasy_model
        self.view = view
        self.register_callbacks()

    def register_callbacks(self):
        """
        This function receives the inputs given by the UI and modifies the display based on the chosen selections
        The output is the resulting selections to make the display the selected stats and settings.
        :return:
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
            This function takes multiple inputs and modifies the display based on the user's selections and
            updated inputs (if modifying fantasy values)

            Parameters:
            data_selected (str):    A selected value representing the choice of displaying real statistics
                                    or fantasy statistics
            year_selected (str):    A selected value representing the statistical year to reference
            graph_selected (str):   A selected value representing the graph to be displayed (Bar or Scatter plot)
            team_selected (str):    Selected dropdown value representing selected team(s) to display
                                    their player's stats
            position_selected (str):Filters the data represented by the chosen position (L,R,C D)
            stat_selected (str):    Displays the selected stat(s) to the graph chosen
            stat2_selected (str or None): The secondary stat to be displayed if chosen
            slider_val: (int):      The int representing the number of players to display on the graph (1-1000 players)
            f_inputs: (float):      Customisable fantasy stat values. These are modifiable and will update
                                    the fantasy display based on the given user input.

            returns: A dash component is returned configured to user selected values
            """

            # Convert f_inputs to a dictionary
            f_inputs_dict = dict(zip(self.fantasy_model.f_labels, f_inputs))

            # Updated fantasy inputs from user input
            updated_f_scoring = {label: value for label, value in f_inputs_dict.items()}
            self.fantasy_model.update_scoring(updated_f_scoring)

            fig = {}

            #Selected choices
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

                    if isinstance(stat_selected,str):
                        stat_selected = [stat_selected]

                    dfs['total_f_points'] = dfs.loc[:, stat_selected].sum(axis=1)
                    selected_result = dfs.nlargest(slider_val, 'total_f_points')

                    fig = px.bar(
                        selected_result,
                        x='name',
                        y=stat_selected,
                        title='Fantasy Points',
                        labels={'name': 'Player Name'},
                        hover_data={'total_f_points': ':.1f'}
                    )
                    fig.update_layout(barmode='stack')

                #Scatter plot display
                elif graph_selected == 'scatter':
                    selected_result = dfs.nlargest(slider_val, stat_selected)
                    fig = px.scatter(
                        selected_result,
                        x=stat2_selected,
                        y=stat_selected,
                        title=f'Top {slider_val} Players Ranked By {stat_selected} and {stat2_selected}',
                        labels={'name': 'Player Name', stat_selected: stat_selected},
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
            """
            Updates the slider's min,max,step and marks values displayed based on the selected graph

            Parameters:
            select_graph (str): The selected graph (bar or scatter)

            Returns:
            marks_val (int): New range for the slider (0-100 or 0-500)
            max_val (int): Max value for the slider (100 or 500)
            min_val (int): Min value for the slider (0)
            step_val (int): Step value for the slider (10 or 50)
            """
            #Set the slider's range and values for the bar graph
            if select_graph == 'bar':
                marks_val = {i: str(i) for i in range(0, 101, 10)}
                max_val = 100
                min_val = 0
                step_val = 10

            #Set the slider's range and values for the scatter plot
            else:
                marks_val = {i: str(i) for i in range(0, 501, 50)}
                max_val = 500
                min_val = 0
                step_val = 50

            return marks_val, max_val, min_val, step_val

        #Callback for updating selectable dropdowns based on graph chosen
        @self.app.callback(
            Output(component_id='select_stat', component_property='options'),
            Output(component_id='select_stat', component_property='multi'),
            Output(component_id='select_stat2', component_property='options'),
            Output(component_id='select_stats_block2', component_property='style'),
            Output(component_id='fantasy_scores_block', component_property='style'),

            [Input(component_id='select_data', component_property='value'),
             Input(component_id='select_graph', component_property='value')]
        )
        #Show/Hide select_stat2 dropdown
        def update_dropdowns(select_data, select_graph):
            """
            Updates the select_stat, select_stat2 dropdowns and displays/hides the select_stat2 dropdown and
            custom fantasy stat values based on user selections.

            Parameters:
            select_data (str):  Selectable dropdown value representing real/fantasy statistics displayed
            select_graph (str): Selectable graph to display the selected stats (bar/scatter plot)

            Returns:
            select_stat: options
                bar: Real stat selections OR Fantasy stat selections
                scatter: Real stat selections OR Fantasy stat selections

            select_stat: multi
                True: Allow multiple selections for the 1st stat selection
                False: 1 selection allowed for stat selection

            select_stat2: options
                []: None
                all_options: Real stat selection options
                f_options: Fantasy stat selection options

            select_stats_block2: style
                none: No display for the secondary stat block
                inline-block: Visible secondary stat block

            fantasy_scores_block: style
                none: No display for the fantasy scores block
                inline-block: Visible fantasy stat block
            """
            #Real data display
            if select_data:
                #Show bar graph dropdown format (1 Stat selection dropdown)
                if select_graph == 'bar':
                    return self.nhl_model.all_options, False, [], {'width': "20%", 'display': 'none'},\
                           {'width': "20%", 'display': 'none'}

                #Scatter plot display: (X,Y stat dropdowns)
                else:
                    return self.nhl_model.all_options, False, self.nhl_model.all_options, \
                           {'width': "20%", 'display': 'inline-block'}, {'width': "20%", 'display': 'none'}

            #Fantasy display
            else:
                #Bar Graph
                if select_graph == 'bar':
                    return self.fantasy_model.f_options, True, [], {'width': "20%", 'display': 'none'},\
                       {'width': "50%", 'display': 'inline-block'}
                #Scatter Plot
                else:
                    return self.fantasy_model.f_options, False, self.fantasy_model.f_options, \
                           {'width': "20%", 'display': 'inline-block'}, {'width': "50%", 'display': 'inline-block'}