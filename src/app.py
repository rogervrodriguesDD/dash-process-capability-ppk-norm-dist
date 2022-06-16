import dash
from dash import html
from dash import dcc

from app_config import EXT_STYLESHEETS_REL_PATH, config
from app_layout import app_layout

app = dash.Dash(__name__, external_stylesheets = EXT_STYLESHEETS_REL_PATH)
app.title = config.app_config.app_title
app.layout = app_layout

if __name__ == '__main__':
    app.run_server(debug=config.app_config.debug,
                port=config.app_config.port,
                host=config.app_config.host)
