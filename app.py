import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table, State
from utils.mongodb_utils import loadMongoDB
from utils.mysql_utils import getKrc, getPaper
from utils.neo4j_utils import loadNEO4J

# dash constructor
app = Dash(__name__)

# load variable databases
mongo = loadMongoDB()
neo4j = loadNEO4J("bolt://localhost:7687", "neo4j", "cs411")


# top professors ranked by krc
app.layout = html.Div([
    html.H1(children='Ausome Academic Mentor', style={'textAlign':'center'}),

    html.Div(className='row', children=[
        dcc.Input(id='input_key'),
        html.Button('Search Professor', id='search_professor'),

        dcc.Input(id='input_id'),
        html.Button('Search Paper', id='search_paper'),
    ]),
    
    html.Div(className='row', children=[
        dash_table.DataTable(
            columns = [{'name': 'Professor', 'id': 'name'}, 
                    {'name': 'Keyword-Relevant Citation', 'id': 'KRC'}, 
                    {'name': 'Position', 'id': 'pos'},
                    {'name': 'Affiliation University', 'id': 'uni'},
                    {'name': 'Professor ID', 'id': 'id'}],
            id='professor_table'),
        dash_table.DataTable(
            columns = [{'name': 'Paper Name', 'id': 'title'},
                    {'name': 'Publish Year', 'id': 'year'}, 
                    {'name': 'Paper Venue', 'id': 'venue'},
                    {'name': 'Paper Citation Number', 'id': 'num_citations'},
                    ],
            id='paper_table'),     
    ])
      
])



@callback(
    Output('professor_table', 'data'),
    Output('paper_table', 'data'),
    State('input_key', 'value'),
    State('input_id', 'value'),
    Input('search_professor', 'n_clicks'),
    Input('search_paper', 'n_clicks')
)
def update_table(input_key, input_id, n_clicks1, n_clicks2):
    if not input_key:
        return dash.no_update
    if not input_id:
        return dash.no_update
    res1 = getKrc(input_key)
    res2 = getPaper(input_id)
    # print(result)
    return res1, res2



if __name__ == '__main__':
    app.run_server(debug=True)