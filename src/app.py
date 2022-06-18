import argparse
import dash
from dash import html
from dash import dcc

from app_config import EXT_STYLESHEETS_REL_PATH, config
from app_layout import app_layout

app = dash.Dash(__name__, external_stylesheets = EXT_STYLESHEETS_REL_PATH)
app.title = config.app_config.app_title
app.layout = app_layout

def _setup_parser_run_app_config():
    """
    Setup Python's ArgumentParser with Application-level configuration.
    The default values of the arguments are given by the 'config.app_config'
    object.
    """

    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('--help', '-h', action='help')
    parser.add_argument('--host', type=str, default=config.app_config.host)
    parser.add_argument('--port', type=int, default=config.app_config.port)
    parser.add_argument('--debug', type=bool, default=config.app_config.debug)

    return parser

if __name__ == '__main__':
    """
    Server application

    Example of command:
    ```
    python app.py --host=localhost --port=8080 --debug=False
    ```
    """

    parser = _setup_parser_run_app_config()
    run_app_config = parser.parse_args()

    app.run_server(debug=run_app_config.debug,
                port=run_app_config.port,
                host=run_app_config.host)
