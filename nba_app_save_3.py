from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import statsmodels
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.metrics import accuracy_score, mean_squared_error
import numpy as np

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

server = app.server

df = pd.read_csv("../players_CSV/players_20years_change.csv")
df_list = pd.read_csv("../players_CSV/players_list.csv")
df_stat = pd.read_csv("../players_CSV/stat_mean.csv")
list_name_lower = pd.read_csv("../players_CSV/name_lower.csv")

fig = go.Figure(data=[go.Table(
    header=dict(values=list(df_list[["PLAYER_NAME"]]),
                align='center'),
    cells=dict(values=[df_list.PLAYER_NAME],
               align='center'))
])

app.title = "20 Years of NBA Statistics"

# Markdown Text

markdown_text = """
This app is a data student project. Most of the informations for the statistics comes from an API named nba-api 1.1.8,
enriched with a scraping of the website www.basketball-reference.com. It contains the statistics of every players and every
teams since the 2000-01 season, which means that the stats of a players that plays before are not taken into consideration.
"""

explain_3d_pos = """
Choose 3 features to compute which ones are key features to determine the position of a player. You can select Position that
gives the 5 position or Generalized position that group in 3 categories (Front, Wing and Guard). You can also keep only players
that plays a minimum of time with the slider.
"""

explain_box_pos = """
Choose 1 stat category to see the evolution of this stat in function of th position.
"""

explain_player_choice = """
Write 1 to 5 player names and choose a stat category to compare their evolution.
"""

# Graphs








app.layout = html.Div([
    html.H1(
      children='20 Years of NBA Statistics',
      style={
         'textAlign': 'center'
      }
    ),

    dcc.Markdown(children= markdown_text
    ),

    html.Br(),

    dcc.Tabs([
    dcc.Tab(label="Data Exploration", children=[

        html.H3(
          children="Observation of statistics in function of the player's position",
          style={
             'textAlign': 'center'
          }
        ),

        html.Br(),

        html.Div([
            html.Div(children=[

                dcc.Markdown(children= explain_3d_pos
                ),

                html.H3(
                  children='Position to predict',
                  style={
                     'textAlign': 'center'
                  }
                ),

                dcc.Dropdown(
                    id='position to predict',
                    options=[
                            {'label': 'Postion', 'value': 'POSITION'},
                            {'label': 'Generalized Position', 'value': 'GEN_POST'}
                            ],
                            value='POSITION',
                            multi=False
                ),


                html.H3(
                  children='Choose your stat categories',
                  style={
                     'textAlign': 'center'
                  }
                ),
                dcc.Dropdown(
                    id='stat_category',
                    options=[
                        {'label': 'Points per games', 'value': 'PPG'},
                        {'label': 'Field Goals percentage', 'value': 'FG_PCT'},
                        {'label': '3 points percentage', 'value': 'FG3_PCT'},
                        {'label': 'Free Throws percentage', 'value': 'FT_PCT'},
                        {'label': 'Rebounds per games', 'value': 'RPG'},
                        {'label': 'Assists per games', 'value': 'APG'},
                        {'label': 'Steals per games', 'value': 'SPG'},
                        {'label': 'Blocks per games', 'value': 'BPG'},
                        {'label': 'Turnovers per games', 'value': 'TPG'},
                        {'label': 'Fouls per games', 'value': 'FPG'}

                ],
                value=['FG3_PCT', 'FT_PCT', 'BPG'],
                multi=True
                ),

                html.H3(
                  children='Minimum minutes played',
                  style={
                     'textAlign': 'center'
                  }
                ),

                dcc.Slider(
                    id='my_slider',
                    min=0,
                    max=30,
                    step=10,
                    value=20,
                    marks={
                        0: '0',
                        10: '10',
                        20: '20',
                        30: '30',

                        },
                )

             ], className="four columns"),



            html.Div(children=[
            ], className="eight columns", id='output-container-button1')
        ], className="row"),

            html.Br(),
            html.Br(),
            html.Br(),

        html.Div([
            html.Div(children=[

                dcc.Markdown(children= explain_box_pos
                ),

                html.H3(
                        children='Position to predict',
                        style={
                        'textAlign': 'center'
                         }
                ),

                dcc.Dropdown(
                    id='position to predict2',
                    options=[
                            {'label': 'Postion', 'value': 'POSITION'},
                            {'label': 'Generalized Position', 'value': 'GEN_POST'}
                            ],
                            value='POSITION',
                            multi=False
                ),


                html.H3(
                        children='Choose your stat category',
                        style={
                        'textAlign': 'center'
                         }
                ),

                dcc.RadioItems(
                    id='stat_category2',
                    options=[
                        {'label': 'Minutes per games', 'value': 'MPG'},
                        {'label': 'Points per games', 'value': 'PPG'},
                        {'label': 'Field Goals percentage', 'value': 'FG_PCT'},
                        {'label': '3 points percentage', 'value': 'FG3_PCT'},
                        {'label': 'Free Throws percentage', 'value': 'FT_PCT'},
                        {'label': 'Rebounds per games', 'value': 'RPG'},
                        {'label': 'Assists per games', 'value': 'APG'},
                        {'label': 'Steals per games', 'value': 'SPG'},
                        {'label': 'Blocks per games', 'value': 'BPG'},
                        {'label': 'Turnovers per games', 'value': 'TPG'},
                        {'label': 'Fouls per games', 'value': 'FPG'}

                    ],
                    value='PPG'
                ),

            ], className="four columns"),

            html.Div(children=[
                ], className="eight columns", id='output-container-button2')
                ], className="row"),

            html.Br(),
            html.Br(),
            html.Br(),

            html.H3(
                    children='Comparison of players stats during their careers',
                    style={
                    'textAlign': 'center'
                     },
            ),

            dcc.Markdown(children= explain_player_choice
            ),

            html.Br(),
            html.Br(),

            dcc.Input(id="input1", type="text", placeholder="Write Name"),
            dcc.Input(id="input2", type="text", placeholder="Write Name"),
            dcc.Input(id="input3", type="text", placeholder="Write Name"),
            dcc.Input(id="input4", type="text", placeholder="Write Name"),
            dcc.Input(id="input5", type="text", placeholder="Write Name"),

        html.Div([
            html.Div(children=[

                html.Br(),
                html.Br(),
                html.Br(),

                html.H3(
                  children='Choose your stat category',
                  style={
                     'textAlign': 'center'
                  }
                ),
                dcc.RadioItems(
                    id='stat_category3',
                    options=[
                        {'label': 'Minutes per games', 'value': 'MPG'},
                        {'label': 'Points per games', 'value': 'PPG'},
                        {'label': 'Field Goals percentage', 'value': 'FG_PCT'},
                        {'label': '3 points percentage', 'value': 'FG3_PCT'},
                        {'label': 'Free Throws percentage', 'value': 'FT_PCT'},
                        {'label': 'Rebounds per games', 'value': 'RPG'},
                        {'label': 'Assists per games', 'value': 'APG'},
                        {'label': 'Steals per games', 'value': 'SPG'},
                        {'label': 'Blocks per games', 'value': 'BPG'},
                        {'label': 'Turnovers per games', 'value': 'TPG'},
                        {'label': 'Fouls per games', 'value': 'FPG'}

                    ],
                    value='PPG'
                ),

             ], className="four columns"),

            html.Div(children=[
            ], className="eight columns", id='output-container-button3')
        ], className="row")

    ])

])

], style={'width': '75%', 'textAlign': 'center', 'margin-left':'12.5%', 'margin-right':'0'})

@app.callback(
    dash.dependencies.Output('output-container-button1', 'children'),
    [dash.dependencies.Input('position to predict', 'value'), dash.dependencies.Input('stat_category', 'value'), dash.dependencies.Input('my_slider', 'value')])
def pos_predict(value2, value3, value4):

        if len(value3) != 3:
            return "Please select at least 3 column"
        else:
            fig1 = px.scatter_3d(df_stat[df_stat["MPG"] > value4], x=value3[0], y=value3[1], z=value3[2], color=value2)
            fig1.update_layout(title_text='3D plot of stats in function of position', title_x=0.5)
        return html.Div([
            html.Br(),
            dcc.Graph(id='g1', figure=fig1)
        ])

@app.callback(
    dash.dependencies.Output('output-container-button2', 'children'),
    [dash.dependencies.Input('position to predict2', 'value'), dash.dependencies.Input('stat_category2', 'value')])
def pos_predict(value5, value6):

            fig2 = px.box(df_stat, y=value6, color=value5, points="all")
            fig2.update_layout(title_text='Stat Category in function of position', title_x=0.5)
            return html.Div([
            html.Br(),
            dcc.Graph(id='g2', figure=fig2)
        ])

@app.callback(
    dash.dependencies.Output('output-container-button3', 'children'),
    [dash.dependencies.Input('input1', 'value'), dash.dependencies.Input('input2', 'value'),
    dash.dependencies.Input('input3', 'value'), dash.dependencies.Input('input4', 'value'),
    dash.dependencies.Input('input5', 'value'), dash.dependencies.Input('stat_category3', 'value')])
def pos_predict(value7, value8, value9, value10, value11, value12):


    if value7 != None and value7.lower() not in list_name_lower.values:
        return ""
    elif value8 != None and value8.lower() not in list_name_lower.values:
        return ""
    elif value9 != None and value9.lower() not in list_name_lower.values:
        return ""
    elif value10 != None and value10.lower() not in list_name_lower.values:
        return ""
    elif value11 != None and value11.lower() not in list_name_lower.values:
        return ""
    elif value7 != None and value8 != None and value9 != None and value10 != None and value11 != None :
        return html.Div([
        html.Br(),
        dcc.Graph(id='g3', figure=fig3)
        ])
    else :
            fig3_1 = go.Figure()
            fig3_1.add_trace(go.Scatter(x=df[df["NAME"] == value7.lower()]["AGE"], y=df[df["NAME"] == value7.lower()][value12],
                                mode='lines+markers', name=value7))
            fig3_1.update_layout(title=dict(text = 'Comparison of players stats', x=0.5),
                               xaxis_title='Age', yaxis_title=value12)

            fig3_2 = go.Figure()
            fig3_2.add_trace(go.Scatter(x=df[df["NAME"] == value7.lower()]["AGE"], y=df[df["NAME"] == value7.lower()][value12],
                                mode='lines+markers', name=value7))
            fig3_2.add_trace(go.Scatter(x=df[df["NAME"] == value8.lower()]["AGE"], y=df[df["NAME"] == value8.lower()][value12],
                                mode='lines+markers', name=value8))
            fig3_2.update_layout(title=dict(text = 'Comparison of players stats', x=0.5),
                               xaxis_title='Age', yaxis_title=value12)

            fig3_3 = go.Figure()
            fig3_3.add_trace(go.Scatter(x=df[df["NAME"] == value7.lower()]["AGE"], y=df[df["NAME"] == value7.lower()][value12],
                                mode='lines+markers', name=value7))
            fig3_3.add_trace(go.Scatter(x=df[df["NAME"] == value8.lower()]["AGE"], y=df[df["NAME"] == value8.lower()][value12],
                                mode='lines+markers', name=value8))
            fig3_3.add_trace(go.Scatter(x=df[df["NAME"] == value9.lower()]["AGE"], y=df[df["NAME"] == value9.lower()][value12],
                                mode='lines+markers', name=value9))
            fig3_3.update_layout(title=dict(text = 'Comparison of players stats', x=0.5),
                               xaxis_title='Age', yaxis_title=value12)

            fig3_4 = go.Figure()
            fig3_4.add_trace(go.Scatter(x=df[df["NAME"] == value7.lower()]["AGE"], y=df[df["NAME"] == value7.lower()][value12],
                                mode='lines+markers', name=value7))
            fig3_4.add_trace(go.Scatter(x=df[df["NAME"] == value8.lower()]["AGE"], y=df[df["NAME"] == value8.lower()][value12],
                                mode='lines+markers', name=value8))
            fig3_4.add_trace(go.Scatter(x=df[df["NAME"] == value9.lower()]["AGE"], y=df[df["NAME"] == value9.lower()][value12],
                                mode='lines+markers', name=value9))
            fig3_4.add_trace(go.Scatter(x=df[df["NAME"] == value10.lower()]["AGE"], y=df[df["NAME"] == value10.lower()][value12],
                                mode='lines+markers', name=value10))
            fig3_4.update_layout(title=dict(text = 'Comparison of players stats', x=0.5),
                               xaxis_title='Age', yaxis_title=value12)

            fig3_5 = go.Figure()
            fig3_5.add_trace(go.Scatter(x=df[df["NAME"] == value7.lower()]["AGE"], y=df[df["NAME"] == value7.lower()][value12],
                                mode='lines+markers', name=value7))
            fig3_5.add_trace(go.Scatter(x=df[df["NAME"] == value8.lower()]["AGE"], y=df[df["NAME"] == value8.lower()][value12],
                                mode='lines+markers', name=value8))
            fig3_5.add_trace(go.Scatter(x=df[df["NAME"] == value9.lower()]["AGE"], y=df[df["NAME"] == value9.lower()][value12],
                                mode='lines+markers', name=value9))
            fig3_5.add_trace(go.Scatter(x=df[df["NAME"] == value10.lower()]["AGE"], y=df[df["NAME"] == value10.lower()][value12],
                                mode='lines+markers', name=value10))
            fig3_5.add_trace(go.Scatter(x=df[df["NAME"] == value11.lower()]["AGE"], y=df[df["NAME"] == value11.lower()][value12],
                                mode='lines+markers', name=value11))
            fig3_5.update_layout(title=dict(text = 'Comparison of players stats', x=0.5),
                               xaxis_title='Age', yaxis_title=value12)

            return html.Div([
            html.Br(),
            dcc.Graph(id='g3', figure=fig3)
        ])

if __name__ == '__main__':
    app.run_server(debug=True)
