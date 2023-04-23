import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table, State
from utils.mongodb_utils import loadMongoDB
from utils.mysql_utils import getKrc, getPaper, getAllPaper, getAllKeywords, likeProfessor, getLiked, unlikeProfessor
from utils.neo4j_utils import getVenues
from utils.mongodb_utils import getProfile
import plotly.graph_objects as go
import plotly.express as px
import geopandas as gpd
from geopy.geocoders import Nominatim

# dash constructor
app = Dash(__name__)

# load variable databases
mongo = loadMongoDB()

#  # top professors ranked by krc
app.layout = html.Div([
    html.H1(children='Awesome Academic Mentor', style={'textAlign':'center', 'color': 'white'}),


    # Widget 1: Search professor by keywords
    html.Div(className='row', children=[
    
        html.Div(children=[
            dcc.Input(id='input_key', placeholder='Enter a Research Keyword', style={'width': '30%', 'marginRight': '10px'}),
            dcc.Dropdown(
                id='professor_dropdown',
                options=[{'label': '10', 'value': '10'},
                        {'label': '20', 'value': '20'},
                        {'label': '50', 'value': '50'},
                        {'label': '100', 'value': '100'}],
                value='10',
                searchable=False,
                clearable=False,
                style={'width': '5%', 'color': 'black'}
            ),
            html.Button('Search Professors', id='search_professor', n_clicks=0, className='btn btn-primary', style={'marginRight': '20px'}),
        ], style={'display': 'flex'}),
        
        
        dash_table.DataTable(
            columns = [ {'name': 'Professor ID', 'id': 'id'},
                    {'name': 'Professor', 'id': 'name'}, 
                    {'name': 'Keyword-Relevant Citation', 'id': 'KRC'}, 
                    {'name': 'Position', 'id': 'pos'},
                    {'name': 'Affiliation University', 'id': 'uni'},
                    ],
            id='professor_table',
            style_header={
                'backgroundColor': '#0e263d',
                'fontWeight': 'bold',
                'color': 'white'
            },
            style_cell={
                'backgroundColor': '#7D9CC0',
                'color': 'black'
            }
        ),
    ], style={'backgroundColor': '#7D9CC0', 'alignItems': 'center', 'justifyContent': 'center', 'padding': '20px', 'border': '1px solid black', 'borderRadius': '5px', 'margin': '20px', 'overflow': 'auto'}),

    html.Div(className='row', children=[
        # Widget 2: Show professor profiles by input professor id
        html.Div(children=[
            html.Div(children=[
                dcc.Input(id='input_profNameProfile', placeholder='Enter Professor Name', style={'width': '30%', 'marginRight': '10px'}),
                html.Button('Search Profile', id='search_nameProfile', className='btn btn-primary', style={'marginRight': '20px'}),
            ], style={'display': 'flex'}),  

            html.Div(children=[
                html.Img(id='profile_pic', src="", style={'width': '100px', 'height': '250px', 'overflow': 'auto', 'width': '45%', 'display': 'inline-block', 'margin': '20px',}),
                html.Div(id='profile', children=[], style={'overflow': 'auto', 'width': '45%', 'display': 'inline-block', 'color': 'black'}),
            ], style={'display': 'flex'}),

            # Like the professor
            html.Div(children=[
                dcc.Input(id='input_likeKey', placeholder='Enter Professor Name', style={'width': '30%', 'marginRight': '10px'}),
                html.Button('Like', id='like_professor', className='btn btn-primary', style={'marginRight': '20px'}),
                html.Div(id='print_like'),
            ], style={'display': 'flex'}),
        ], style={
                'backgroundColor': '#7D9CC0', 'alignItems': 'center', 'justifyContent': 'center', 
                'padding': '20px', 'border': '1px solid black', 'borderRadius': '5px', 'margin': '20px', 
                'overflow': 'auto', 'width': '50%', 'display': 'inline-block'
                }),

        # Widget 3: Search publications by input professor id
        html.Div(children=[
                html.Div(children=[
                dcc.Input(id='input_id', placeholder='Enter Professor Name', style={'width': '30%', 'marginRight': '10px'}),
                dcc.Dropdown(
                        id='paper_dropdown',
                        options=[{'label': '10', 'value': '10'},
                                {'label': '20', 'value': '20'},
                                {'label': '50', 'value': '50'},
                                {'label': '100', 'value': '100'}],
                        value='10',
                        searchable=False,
                        clearable=False,
                        style={'width': '5%', 'color': 'black', 'marginRight': '20px'}
                    ),
                html.Button('Show Publications Ordered by Citation Number', id='search_paper', n_clicks=0, className='btn btn-primary'),
            ], style={'display': 'flex'}),
            dash_table.DataTable(
                columns = [
                        {'name': 'Paper Name', 'id': 'title'},
                        {'name': 'Publish Year', 'id': 'year'}, 
                        {'name': 'Paper Citation Number', 'id': 'num_citations'},
                        {'name': 'Paper Venue', 'id': 'venue'},
                        ],
                id='paper_table',
                style_header={
                    'backgroundColor': '#0e263d',
                    'fontWeight': 'bold',
                    'color': 'white'
                },
                style_cell={
                    'backgroundColor': '#7D9CC0',
                    'color': 'black'
                }
            ),     
        ], style={
                'backgroundColor': '#7D9CC0', 'alignItems': 'center', 'justifyContent': 'center', 
                'padding': '20px', 'border': '1px solid black', 'borderRadius': '5px', 'margin': '20px', 
                'overflow': 'auto', 'width': '50%', 'display': 'inline-block'
                }),
    ], style={'display': 'flex'}),

    html.Div(className='row', children=[
        # Widget 4: get the time line of publications
        html.Div(children=[
            dcc.Input(id='input_profIDLine', placeholder='Enter Professor Name', style={'width': '30%', 'marginRight': '10px'}),
            html.Button('Search Publication Time', id='search_pubTime', n_clicks=0, className='btn btn-primary', style={'marginRight': '20px'}),
            dcc.Graph(id = 'pubTime_plot')
        ], style={'backgroundColor': '#7D9CC0', 'alignItems': 'center', 'justifyContent': 'center', 
                    'padding': '20px', 'border': '1px solid black', 'borderRadius': '5px', 'margin': '20px', 
                    'overflow': 'auto', 'width': '50%', 'display': 'inline-block'}),

        # Widget 5: get the keyword distributions
        html.Div(children=[
            html.Div(children=[
                dcc.Input(id='input_profIDChart', placeholder='Enter Professor Name', style={'width': '30%', 'marginRight': '10px'}),
                # dcc.Dropdown(['5', '10', '15', '20', '25', '30', '50'], '10', id='keywordNum_dropdown', style={"width": "40%", 'color': 'black'},),
                dcc.Dropdown(
                        id='keywordNum_dropdown',
                        options=[{'label': '10', 'value': '10'},
                                {'label': '20', 'value': '20'},
                                {'label': '50', 'value': '50'},
                                {'label': '100', 'value': '100'}],
                        value='10',
                        searchable=False,
                        clearable=False,
                        style={'width': '5%', 'color': 'black', 'marginRight': '20px'}
                    ),
                html.Button('Search Keyword Distribution', id='search_keyword', n_clicks=0, className='btn btn-primary', style={'marginRight': '20px'}),
            ], style={'display': 'flex'}),
            dcc.Graph(id = 'keyword_chart')
        ], style={'backgroundColor': '#7D9CC0', 'alignItems': 'center', 'justifyContent': 'center', 
                    'padding': '20px', 'border': '1px solid black', 'borderRadius': '5px', 'margin': '20px', 
                    'overflow': 'auto', 'width': '50%', 'display': 'inline-block'}),
    ], style={'display': 'flex'}),    

    # Widget 6: get the publication venue distributions
    html.Div(className='row', children=[
        html.Div(children=[
            dcc.Input(id='input_venueChart', placeholder='Enter Professor Name', style={'width': '30%', 'marginRight': '10px'}),
            html.Button('Search Publication Venues', id='search_pubVenue', n_clicks=0, className='btn btn-primary', style={'marginRight': '20px'}),
        ], style={'display': 'flex'}),
        dcc.Graph(id = 'venue_chart'),
    ], style={'backgroundColor': '#7D9CC0', 'alignItems': 'center', 'justifyContent': 'center', 
              'padding': '20px', 'border': '1px solid black', 'borderRadius': '5px', 'margin': '20px', 
              'overflow': 'auto'}),


    # Widget 7: get the liked professors and unlike if any
    html.Div(className='row', children=[
        html.Button('Show Liked Professors', id='show_liked'),

        dash_table.DataTable(
            columns = [
                    {'name': 'Professor ID', 'id': 'id'},
                    {'name': 'Professor Name', 'id': 'name'}, 
                    {'name': 'University', 'id': 'U.name'},
                    ],
            id='like_data',
            style_header={
                'backgroundColor': '#0e263d',
                'fontWeight': 'bold',
                'color': 'white'
            },
            style_cell={
                'backgroundColor': '#7D9CC0',
                'color': 'black'
            }
        ),

        html.Div(className='row', children=[
            dcc.Input(id='input_unlikeKey', placeholder='Enter Professor Name', style={'width': '30%', 'marginRight': '10px'}),
            html.Button('Unlike Professor', id='unlike_professor'),
            html.Div(id='print_unlike'),
        ], style={'backgroundColor': '#7D9CC0'}),

      ], style={'backgroundColor': '#7D9CC0', 'alignItems': 'center', 'justifyContent': 'center', 
              'padding': '20px', 'border': '1px solid black', 'borderRadius': '5px', 'margin': '20px', 
              'overflow': 'auto'}),
    
], style={'backgroundColor': '#7D9CC0', 'color': 'white'})

################## Widget 1 ##################
@callback(
    Output('professor_table', 'data'),
    State('input_key', 'value'),
    State('professor_dropdown', 'value'),
    Input('search_professor', 'n_clicks'),
)
def update_table(input_key, input_num, n_clicks):
    if not input_key:
        return dash.no_update
    res = getKrc(input_key, input_num)
    return res


################## Widget 2 ##################
@callback(
    [
    Output('profile_pic', 'src'),
    Output('profile', 'children'),
     ],
    State('input_profNameProfile', 'value'),
    Input('search_nameProfile', 'n_clicks'),
)
def profProfile(input_name, n_clicks):
    if not input_name:
        return dash.no_update
    res = getProfile(input_name)[0]
    pic_src = res['photo_url']
    profile_info = [
        html.P(f"Name: {res['name']}"),
        html.P(f"Email: {res['email']}"),
        html.P(f"Phone: {res['phone']}"),
        html.P(f"Position: {res['position']}"),
        html.P(f"University: {res['uni']}"),
        html.P(f"Publication Numbers: {res['pubNum']}"),
        html.P(f"Research Interest: {res['research_interest']}"),
    ]
    return pic_src, profile_info

@callback(
    Output('print_like', 'children'),
    State('input_likeKey', 'value'),
    Input('like_professor', 'n_clicks'),
)
def like_pro(input_key, n_clicks):
    if not input_key:
        return dash.no_update
    _name = likeProfessor(input_key)
    return f"{_name['name']} is liked!"

################## Widget 3 ##################
@callback(
    Output('paper_table', 'data'),
    State('input_id', 'value'),
    State('paper_dropdown', 'value'),
    Input('search_paper', 'n_clicks')
)
def update_table(input_id, input_num, n_clicks):
    if not input_id:
        return dash.no_update
    res = getPaper(input_id, input_num)
    return res

################## Widget 4 ##################

@callback(
    Output('pubTime_plot', 'figure'),
    State('input_profIDLine', 'value'),
    Input('search_pubTime', 'n_clicks'),
)
def pubTime(input_id, n_clicks):
    if not input_id:
        return dash.no_update
    df, professor_name = getAllPaper(input_id)
    df = df.rename(columns={'id': 'Number of Publications'})
    df = df.reset_index()
    if n_clicks > 0:
        fig = px.line(df, x='year', y='Number of Publications')
        fig.update_layout(template='plotly_dark', title = f'{professor_name}: Number of Publications over Time')
        return fig
    else:
        return {} 

################## Widget 5 ##################

@callback(
    Output('keyword_chart', 'figure'),
    State('input_profIDChart', 'value'),
    State('keywordNum_dropdown', 'value'),
    Input('search_keyword', 'n_clicks'),
)
def keywordChart(input_id, input_num, n_clicks):
    if not input_id:
        return dash.no_update
    df, professor_name = getAllKeywords(input_id)
    df = df.rename(columns={'id': 'Number of Publications'})
    df = df.reset_index().iloc[:int(input_num)]
    if n_clicks > 0:
        fig = px.pie(df, values='Publication Number', names='Keyword')
        fig.update_layout(template='plotly_dark', title = f'{professor_name}: Top {input_num} Keywords by Number of Publications')
        return fig
    else:
        return {} 

################## Widget 6 ##################

@callback(
    Output('venue_chart', 'figure'),
    State('input_venueChart', 'value'),
    Input('search_pubVenue', 'n_clicks'),
)
def publicationVenue(input_name, n_clicks):
    if not input_name:
        return dash.no_update
    df = getVenues(input_name)
    df = df.rename(columns={'pub.venue': 'Publication Venue'})
    if n_clicks > 0:
        fig = px.histogram(df, x='Publication Venue', template='plotly_dark')
        return fig
    else:
        return {}

################## Widget 7 ##################

@callback(
    Output('like_data', 'data'),
    Input('show_liked', 'n_clicks'),
)
def user_liked(n_clicks):
    liked = getLiked()
    if len(liked) > 0:
        return liked
    else:
        return None
    
@callback(
    Output('print_unlike', 'children'),
    State('input_unlikeKey', 'value'),
    Input('unlike_professor', 'n_clicks'),
)
def unlike_pro(input_key, n_clicks):
    if not input_key:
        return dash.no_update
    _name = unlikeProfessor(input_key)
    return f"{_name['name']} is unliked!"    

if __name__ == '__main__':
    app.run_server()