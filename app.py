from utils.mongodb_utils import hello
from dash import Dash, html
import pymongo


app = Dash(__name__)

app.layout = html.Div([
    html.Div(children='Hello World')
])

# @callback()

if __name__ == '__main__':
    app.run_server(debug=True)