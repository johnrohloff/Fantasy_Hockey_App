import dash
from dash.dependencies import Input, Output


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
            [Input(component_id='select_data', component_property='value')]
        )

        def update_graph(data_selected):
            """
            Updates the output_container based on the selected choice
            :param data_selected:
            :return: Selected choice
            """
            if data_selected:
                return 'Real'
            else:
                return "Fantasy"
