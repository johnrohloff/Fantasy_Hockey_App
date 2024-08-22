import dash
from dash import dcc
from dash import html


class NHLView:
    def __init__(self):
        """
        Initializes the NHLView class
        And stores the layout of the application and stores it in the layout attribute.
        """
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

