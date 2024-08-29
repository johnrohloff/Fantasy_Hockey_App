import dash
from model import NHLModel, FantasyModel
from view import NHLView
from controller import NHLController


class NHLApp:
    """
    This is the main application class which initializes the Dash app, models and view

    Attributes:
        app (dash.Dash): Dash application instance
        nhl_model (NHLModel): Model responsible for real nhl statistics
        fantasy_model (FantasyModel): Model responsible for fantasy statistics
        view (NHLView): View responsible for the Dash layout and UI
        controller (NHLController): Responsible for managing interactions between model + view
    """
    def __init__(self, files):
        """
        Initializes the NHLApp class with provided data files

        Parameters:
            files (list): List of file names, each containing nhl data of a specific year
        """

        # Initialize the Dash app
        self.app = dash.Dash(__name__)

        #Initialize models
        self.nhl_model = NHLModel(files)
        self.fantasy_model = FantasyModel(files)

        #Initialize view with models
        self.view = NHLView(self.nhl_model, self.fantasy_model)

        #Initialize controller with app, models, view
        self.controller = NHLController(self.app, self.nhl_model, self.fantasy_model, self.view)

        # Set up the layout
        self.app.layout = self.view.create_layout()

    def run(self):
        """
        Runs the dash server

        Returns: None
        """
        self.app.run_server(debug=True)


#Starts the application and provides the required data files for the server.
if __name__ == '__main__':
    files = ['skaters_24', 'skaters_23', 'skaters_22', 'skaters_21', 'skaters_20']
    app = NHLApp(files)
    app.run()
