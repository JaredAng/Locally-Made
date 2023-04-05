import dash
from dash import html,dcc
import dash_bootstrap_components as dbc
import flask
import pageCreator as pages
import callbacks
import traceback

### init app
server =  flask.Flask(__name__)
app = dash.Dash(__name__,server = server ,external_stylesheets=[dbc.themes.CYBORG])
app.index_string = pages.main_layout
###

body = html.Div(id="body")
app.layout = dbc.Container([dcc.Location(id='url', refresh=True), pages.navbar,body])

### init callbacks
callbacks.callbacks(app)

if __name__ == "__main__":
    try:
        app.config['suppress_callback_exceptions']=True
        app.run_server(port=80, debug=False, threaded=True)
    except Exception as e:
        pass