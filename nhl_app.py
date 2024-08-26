import dash
from dash import dcc
from dash import html

import model
from model import NHLModel, FantasyModel
from view import NHLView
from controller import NHLController


class NHLApp:
    def __init__(self, files):
        """
        Main application for the NHL player/fantasy stats Dash app
        It initializes the model, view and controller and sets up the layout and
        callbacks for the app.

        :param files: List of filenames (String) without .csv to be loaded by the model
        """
        # Initialize the Dash app
        self.app = dash.Dash(__name__)
        self.nhl_model = NHLModel(files)
        self.fantasy_model = FantasyModel(files)
        self.view = NHLView(self.nhl_model)
        self.controller = NHLController(self.app, self.nhl_model, self.fantasy_model, self.view)

        # Set up the layout
        self.app.layout = self.view.create_layout()


    def run(self):
        """
        Runs the dash server
        :param debug:
        :return:
        """
        self.app.run_server(debug=True)

if __name__ == '__main__':
    """
    Starts the application and provides the required data files for the server.
    """
    files = ['skaters_23', 'skaters_22']
    app = NHLApp(files)
    app.run()
