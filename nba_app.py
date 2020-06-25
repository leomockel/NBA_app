from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import statsmodels
import numpy as np


app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

server = app.server

df = pd.read_csv("data/players_20years_change.csv")
list_name_lower = pd.read_csv("data/name_lower.csv")
df_stat = pd.read_csv("data/stat_mean.csv")
final_note = pd.read_csv("data/position_note_final_test.csv")
salary = pd.read_csv("data/salary_notes.csv")
season_leader = pd.read_csv("data/season_leaders.csv")
teams = pd.read_csv("data/team_season_comp.csv")

x1 = np.array([0, 2, 4, 6, 8, 10])
y1 = np.array([0, 8000000, 16000000, 24000000, 32000000, 40000000])


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

explain_notes = """
To get these notes, I splitted the computations in several steps :
First, for the (minutes, points, rebounds, assists, steals, blocks, turnovers, fouls) per games and the (field goals, 3 points field goals, free throws) percentage,
I did a MinMax scaler for each season and each position.
Then I added the results of points, rebounds, assists, steals, blocks, field goals, 3 points field goals and free throws minus the score of turnovers and fouls.
This result is then multiplied by the result for minutes per games to normalize in function of the time played for these stats.
Finally, I made a last MinMax scaler from these results to have a final note from 0 to 10.
"""

age_range_explain = """
You can adapt the range of the players' age with the slider below.
"""


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
    dcc.Tab(label="Players statistics", children=[

        html.H3(
          children="Top Players each years",
          style={
             'textAlign': 'center'
          }
        ),

        html.Div([
            html.Div(children=[

        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),


        dcc.Dropdown(
            id='year_stat1',
            options=[
                {'label': '2001', 'value': '2001'},
                {'label': '2002', 'value': '2002'},
                {'label': '2003', 'value': '2003'},
                {'label': '2004', 'value': '2004'},
                {'label': '2005', 'value': '2005'},
                {'label': '2006', 'value': '2006'},
                {'label': '2007', 'value': '2007'},
                {'label': '2008', 'value': '2008'},
                {'label': '2009', 'value': '2009'},
                {'label': '2010', 'value': '2010'},
                {'label': '2011', 'value': '2011'},
                {'label': '2012', 'value': '2012'},
                {'label': '2013', 'value': '2013'},
                {'label': '2014', 'value': '2014'},
                {'label': '2015', 'value': '2015'},
                {'label': '2016', 'value': '2016'},
                {'label': '2017', 'value': '2017'},
                {'label': '2018', 'value': '2018'},
                {'label': '2019', 'value': '2019'},
                {'label': '2020', 'value': '2020'}

            ],
            value='2001',
            style={
               'textAlign': 'center'
               }
            ),

            ], className="two columns"),

        html.Div(children=[
        ], className="ten columns", id='output-container-button6'),
        ], className="row"),

############################################################################################################

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

                html.H5(
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


                html.H5(
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
                multi=True,
                style={
                   'textAlign': 'left'
                }
                ),

                html.H5(
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

##########################################################################################################################

        html.Div([
            html.Div(children=[

                dcc.Markdown(children= explain_box_pos
                ),

                html.H5(
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


                html.H5(
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
                    value='PPG',
                    style={
                       'textAlign': 'left'
                    }
                ),

            ], className="four columns"),

            html.Div(children=[
                ], className="eight columns", id='output-container-button2')
                ], className="row"),

            html.Br(),
            html.Br(),
            html.Br(),

##########################################################################################################################

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

                html.H5(
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
                    value='PPG',
                    style={
                       'textAlign': 'left'
                    }
                ),

             ], className="four columns"),

            html.Div(children=[
            ], className="eight columns", id='output-container-button3')
        ], className="row"),

        html.Br(),
        html.Br(),

##########################################################################################################################

        html.H3(
                children='Experimentation : Give a general note for players to see the evolution over time',
                style={
                'textAlign': 'center'
                 },
        ),

        dcc.Markdown(children= explain_notes
        ),

        html.Br(),

        html.Div([
            html.Div(children=[

                html.Br(),
                html.Br(),

                html.H5(
                  children='Choose your Position',
                  style={
                     'textAlign': 'center'
                  }
                ),
                dcc.RadioItems(
                    id='position_category',
                    options=[
                        {'label': 'General', 'value': 'general'},
                        {'label': 'Center', 'value': 'C'},
                        {'label': 'Power Forward', 'value': 'PF'},
                        {'label': 'Small Forward', 'value': 'SF'},
                        {'label': 'Shooting Guard', 'value': 'SG'},
                        {'label': 'Point Guard', 'value': 'PG'},


                    ],
                    value='general',
                    style={
                       'textAlign': 'left'
                    }
                ),

                  html.Br(),

                  html.H5(
                    children='Minimum minutes played',
                    style={
                       'textAlign': 'center'
                    }
                  ),

                  dcc.Slider(
                        id='time_slider',
                        min=0,
                        max=30,
                        step=10,
                        value=0,
                        marks={
                            0: '0',
                            10: '10',
                            20: '20',
                            30: '30',

                        },
                )

             ], className="four columns"),



            html.Div(children=[
            ], className="eight columns", id='output-container-button4')
        ], className="row"),

            html.Br(),
            html.Br(),

##########################################################################################################################

        html.H3(
                children='Comparison of the notes with the salary',
                style={
                'textAlign': 'center'
                 },
        ),

        html.Br(),

        html.Div([
            html.Div(children=[

                html.Br(),
                html.Br(),

                html.H5(
                  children='Choose the year of the salary',
                  style={
                     'textAlign': 'center'
                  }
                ),
                dcc.RadioItems(
                    id='Year',
                    options=[
                        {'label': '2020', 'value': '2020'},
                        {'label': '2021', 'value': '2021'},
                        {'label': '2022', 'value': '2022'},
                        {'label': '2023', 'value': '2023'},

                    ],
                    value='2020',
                    style={
                       'textAlign': 'center'
                    }
                ),

                html.Br(),
                html.Br(),

                dcc.Markdown(children= age_range_explain
                )


             ], className="four columns"),


            html.Div(children=[
            ], className="eight columns", id='output-container-button5')
        ], className="row"),

            html.Div([

                html.H5(
                  children='Age Range',
                  style={
                     'textAlign': 'center'
                  }
                ),

                dcc.RangeSlider(
                      id='age_slider',
                      count=1,
                      min=17,
                      max=45,
                      step=1,
                      value=[22, 37],
                      marks={
                          19: '19',
                          20: '20',
                          21: '21',
                          22: '22',
                          23: '23',
                          24: '24',
                          25: '25',
                          26: '26',
                          27: '27',
                          28: '28',
                          29: '29',
                          30: '30',
                          31: '31',
                          32: '32',
                          33: '33',
                          34: '34',
                          35: '35',
                          36: '36',
                          37: '37',
                          38: '38',
                          39: '39',
                          40: '40',
                          41: '41',
                          42: '42',
                          43: '43'
                      },
                )
                ]),



    ]), # end first tab Players Statistics #####################################################################

    dcc.Tab(label="Teams statistics", children=[

        html.Div([
            html.Div(children=[

                html.Br(),
                html.Br(),

                html.H5(
                  children='Teams stats during time',
                  style={
                     'textAlign': 'center'
                  }
                ),


            dcc.Dropdown(
                id='team_select',
                options=[
                    {'label': 'Atlanta', 'value': 'ATL'},
                    {'label': 'Boston', 'value': 'BOS'},
                    {'label': 'Charlotte/New Orleans', 'value': 'NOP'},
                    {'label': 'Chicago', 'value': 'CHI'},
                    {'label': 'Cleveland', 'value': 'CLE'},
                    {'label': 'Dallas', 'value': 'DAL'},
                    {'label': 'Denver', 'value': 'DEN'},
                    {'label': 'Detroit', 'value': 'DET'},
                    {'label': 'Golden State', 'value': 'GSW'},
                    {'label': 'Houston', 'value': 'HOU'},
                    {'label': 'LA Clippers', 'value': 'LAC'},
                    {'label': 'LA Lakers', 'value': 'LAL'},
                    {'label': 'Miami', 'value': 'MIA'},
                    {'label': 'Milwaukee', 'value': 'MIL'},
                    {'label': 'Minnesota', 'value': 'MIN'},
                    {'label': 'New Jersey/Brooklyn', 'value': 'BKN'},
                    {'label': 'New York', 'value': 'NYK'},
                    {'label': 'Orlando', 'value': 'ORL'},
                    {'label': 'Philadelphia', 'value': 'PHI'},
                    {'label': 'Phoenix', 'value': 'PHX'},
                    {'label': 'Portland', 'value': 'POR'},
                    {'label': 'Sacramento', 'value': 'SAC'},
                    {'label': 'San Antonio', 'value': 'SAS'},
                    {'label': 'Seattle/Oklahoma City', 'value': 'OKC'},
                    {'label': 'Toronto', 'value': 'TOR'},
                    {'label': 'Vancouver/Memphis', 'value': 'MEM'},
                    {'label': 'Washington', 'value': 'WAS'},
                    {'label': 'Charlotte', 'value': 'CHA'},

                ], value='ATL',

            ),

                dcc.RadioItems(
                        id='stat_select',
                            options=[
                                {'label': 'Points per games', 'value': 'PPG'},
                                {'label': 'Field Goals percentage', 'value': 'FG_PCT'},
                                {'label': '3 points percentage', 'value': 'FG3_PCT'},
                                {'label': 'Free Throws percentage', 'value': 'FT_PCT'},
                                {'label': 'Offensive Rebs per games', 'value': 'ORPG'},
                                {'label': 'Defensive Rebs per games', 'value': 'DRPG'},
                                {'label': 'Rebounds per games', 'value': 'RPG'},
                                {'label': 'Assists per games', 'value': 'APG'},
                                {'label': 'Steals per games', 'value': 'SPG'},
                                {'label': 'Blocks per games', 'value': 'BPG'},
                                {'label': 'Turnovers per games', 'value': 'TPG'},
                                {'label': 'Fouls per games', 'value': 'FPG'},
                                {'label': 'Win Percentage', 'value': 'WIN_PCT'},

                            ],
                            value='PPG',
                            style={
                                'textAlign': 'left'
                            }
                    ),


            ], className="four columns"),

            html.Div(children=[
            ], className="eight columns", id='output-container-button7')
        ], className="row"),

        ]),

    dcc.Tab(label="Machine Learning", children=[


    ]),


]) # end of the Tabs ##########################################################################################

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
def pos_predict2(value5, value6):

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
def players_career(value7, value8, value9, value10, value11, value12):


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
    elif value7 != None and value8 == None and value9 == None and value10 == None and value11 == None :
        fig3_1 = go.Figure()
        fig3_1.add_trace(go.Scatter(x=df[df["LOWER_NAME"] == value7.lower()]["AGE"], y=df[df["LOWER_NAME"] == value7.lower()][value12],
                            mode='lines+markers', name=value7))
        fig3_1.update_layout(title=dict(text = 'Comparison of players stats', x=0.5),
                           xaxis_title='Age', yaxis_title=value12)
        return html.Div([
        html.Br(),
        dcc.Graph(id='g3', figure=fig3_1)
        ])

    elif value7 != None and value8 != None and value9 == None and value10 == None and value11 == None :
        fig3_2 = go.Figure()
        fig3_2.add_trace(go.Scatter(x=df[df["LOWER_NAME"] == value7.lower()]["AGE"], y=df[df["LOWER_NAME"] == value7.lower()][value12],
                            mode='lines+markers', name=value7))
        fig3_2.add_trace(go.Scatter(x=df[df["LOWER_NAME"] == value8.lower()]["AGE"], y=df[df["LOWER_NAME"] == value8.lower()][value12],
                            mode='lines+markers', name=value8))
        fig3_2.update_layout(title=dict(text = 'Comparison of players stats', x=0.5),
                           xaxis_title='Age', yaxis_title=value12)

        return html.Div([
        html.Br(),
        dcc.Graph(id='g3', figure=fig3_2)
        ])

    elif value7 != None and value8 != None and value9 != None and value10 == None and value11 == None :
        fig3_3 = go.Figure()
        fig3_3.add_trace(go.Scatter(x=df[df["LOWER_NAME"] == value7.lower()]["AGE"], y=df[df["LOWER_NAME"] == value7.lower()][value12],
                            mode='lines+markers', name=value7))
        fig3_3.add_trace(go.Scatter(x=df[df["LOWER_NAME"] == value8.lower()]["AGE"], y=df[df["LOWER_NAME"] == value8.lower()][value12],
                            mode='lines+markers', name=value8))
        fig3_3.add_trace(go.Scatter(x=df[df["LOWER_NAME"] == value9.lower()]["AGE"], y=df[df["LOWER_NAME"] == value9.lower()][value12],
                            mode='lines+markers', name=value9))
        fig3_3.update_layout(title=dict(text = 'Comparison of players stats', x=0.5),
                           xaxis_title='Age', yaxis_title=value12)

        return html.Div([
        html.Br(),
        dcc.Graph(id='g3', figure=fig3_3)
        ])

    elif value7 != None and value8 != None and value9 != None and value10 != None and value11 == None :
        fig3_4 = go.Figure()
        fig3_4.add_trace(go.Scatter(x=df[df["LOWER_NAME"] == value7.lower()]["AGE"], y=df[df["LOWER_NAME"] == value7.lower()][value12],
                            mode='lines+markers', name=value7))
        fig3_4.add_trace(go.Scatter(x=df[df["LOWER_NAME"] == value8.lower()]["AGE"], y=df[df["LOWER_NAME"] == value8.lower()][value12],
                            mode='lines+markers', name=value8))
        fig3_4.add_trace(go.Scatter(x=df[df["LOWER_NAME"] == value9.lower()]["AGE"], y=df[df["LOWER_NAME"] == value9.lower()][value12],
                            mode='lines+markers', name=value9))
        fig3_4.add_trace(go.Scatter(x=df[df["LOWER_NAME"] == value10.lower()]["AGE"], y=df[df["LOWER_NAME"] == value10.lower()][value12],
                            mode='lines+markers', name=value10))
        fig3_4.update_layout(title=dict(text = 'Comparison of players stats', x=0.5),
                           xaxis_title='Age', yaxis_title=value12)

        return html.Div([
        html.Br(),
        dcc.Graph(id='g3', figure=fig3_4)
        ])

    elif value7 != None and value8 != None and value9 != None and value10 != None and value11 != None :
        fig3_5 = go.Figure()
        fig3_5.add_trace(go.Scatter(x=df[df["LOWER_NAME"] == value7.lower()]["AGE"], y=df[df["LOWER_NAME"] == value7.lower()][value12],
                            mode='lines+markers', name=value7))
        fig3_5.add_trace(go.Scatter(x=df[df["LOWER_NAME"] == value8.lower()]["AGE"], y=df[df["LOWER_NAME"] == value8.lower()][value12],
                            mode='lines+markers', name=value8))
        fig3_5.add_trace(go.Scatter(x=df[df["LOWER_NAME"] == value9.lower()]["AGE"], y=df[df["LOWER_NAME"] == value9.lower()][value12],
                            mode='lines+markers', name=value9))
        fig3_5.add_trace(go.Scatter(x=df[df["LOWER_NAME"] == value10.lower()]["AGE"], y=df[df["LOWER_NAME"] == value10.lower()][value12],
                            mode='lines+markers', name=value10))
        fig3_5.add_trace(go.Scatter(x=df[df["LOWER_NAME"] == value11.lower()]["AGE"], y=df[df["LOWER_NAME"] == value11.lower()][value12],
                            mode='lines+markers', name=value11))
        fig3_5.update_layout(title=dict(text = 'Comparison of players stats', x=0.5),
                           xaxis_title='Age', yaxis_title=value12)

        return html.Div([
        html.Br(),
        dcc.Graph(id='g3', figure=fig3_5)
    ])

@app.callback(
    dash.dependencies.Output('output-container-button4', 'children'),
    [dash.dependencies.Input('position_category', 'value'), dash.dependencies.Input('time_slider', 'value')])
def corr_notes(value13, value14):

        if value13 == "general":
            fig4 = px.box(x=final_note[final_note["MPG_REAL"] > value14]["AGE"],
                          y=final_note[final_note["MPG_REAL"] > value14]["NOTE_m_sc"])

            fig4.update_layout(title=dict(text = 'Evolution of Players notes', x=0.5),
                               xaxis_title='Age',
                               yaxis_title='Notes')

            return html.Div([
                html.Br(),
                dcc.Graph(id='g4', figure=fig4)
            ])

        else:
            fig5 = px.box(x=final_note[(final_note["POSITION"] == value13) & (final_note["MPG_REAL"] > value14)]["AGE"],
                          y=final_note[(final_note["POSITION"] == value13) & (final_note["MPG_REAL"] > value14)]["NOTE_m_sc"])

            fig5.update_layout(title=dict(text = 'Evolution of Players notes', x=0.5),
                               xaxis_title='Age',
                               yaxis_title='Notes')

            return html.Div([
                html.Br(),
                dcc.Graph(id='g5', figure=fig5)
            ])

@app.callback(
    dash.dependencies.Output('output-container-button5', 'children'),
    [dash.dependencies.Input('Year', 'value'), dash.dependencies.Input('age_slider', 'value')])
def salary_predict(value15, value16):

        fig6 = px.scatter(x=salary[(salary[f"{value15}"] > 0) & (salary["AGE"] > value16[0]) & (salary["AGE"] < value16[1])]["NOTE_2020"],
                          y=salary[(salary[f"{value15}"] > 0) & (salary["AGE"] > value16[0]) & (salary["AGE"] < value16[1])][f"{value15}"],
                          color=salary[(salary[f"{value15}"] > 0) & (salary["AGE"] > value16[0]) & (salary["AGE"] < value16[1])]["PLAYER_NAME"])
        fig6.add_trace(go.Line(x=x1, y=y1, mode = "lines", line=dict(color='red', width=4)))

        fig6.update_layout(title=dict(text = "Player's salary in function of their notes", x=0.5),
                           xaxis_title='Notes',
                           yaxis_title='Salary')

        return html.Div([
            html.Br(),
            dcc.Graph(id='g6', figure=fig6)
        ])

@app.callback(
    dash.dependencies.Output('output-container-button6', 'children'),
    [dash.dependencies.Input('year_stat1', 'value')])
def leaders(value17):

        fig7 = go.Figure(data=[go.Table(
                header=dict(values=list(season_leader.columns),
                align='center'),
                cells=dict(values=[season_leader["SEASON"], season_leader["CATEGORY"],
                       season_leader["NAME"], season_leader["HEIGHT"],
                       season_leader["WEIGHT"], season_leader["POST"],
                       season_leader["AGE"], season_leader["TEAM"],
                       season_leader["PPG"], season_leader["FG_P"],
                       season_leader["FG3_P"], season_leader["FT_P"],
                       season_leader["RPG"], season_leader["APG"],
                       season_leader["SPG"], season_leader["BPG"]],
               align='center'))])

        return html.Div([
            html.Br(),
            dcc.Graph(id='g7', figure=fig7, style={
                'height': 525})
        ])

@app.callback(
    dash.dependencies.Output('output-container-button7', 'children'),
    [dash.dependencies.Input('team_select', 'value'), dash.dependencies.Input('stat_select', 'value')])
def pos_predict(value18, value19):

        fig8 = go.Figure()
        fig8.add_trace(go.Scatter(x=teams[teams["TEAM"] == value18]["SEASON"], y=teams[teams["TEAM"] == value18][value19],
                            mode='lines+markers', name=value18))
        fig8.update_layout(title=dict(text = 'Comparison of teams stats', x=0.5),
                           xaxis_title='Age', yaxis_title=value19)

        return html.Div([
        html.Br(),
        dcc.Graph(id='g8', figure=fig8)
        ])

if __name__ == '__main__':
    app.run_server(debug=True)
