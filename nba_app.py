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
leader_2001 = pd.read_csv("data/leader_2001.csv")
leader_2002 = pd.read_csv("data/leader_2002.csv")
leader_2003 = pd.read_csv("data/leader_2003.csv")
leader_2004 = pd.read_csv("data/leader_2004.csv")
leader_2005 = pd.read_csv("data/leader_2005.csv")
leader_2006 = pd.read_csv("data/leader_2006.csv")
leader_2007 = pd.read_csv("data/leader_2007.csv")
leader_2008 = pd.read_csv("data/leader_2008.csv")
leader_2009 = pd.read_csv("data/leader_2009.csv")
leader_2010 = pd.read_csv("data/leader_2010.csv")
leader_2011 = pd.read_csv("data/leader_2011.csv")
leader_2012 = pd.read_csv("data/leader_2012.csv")
leader_2013 = pd.read_csv("data/leader_2013.csv")
leader_2014 = pd.read_csv("data/leader_2014.csv")
leader_2015 = pd.read_csv("data/leader_2015.csv")
leader_2016 = pd.read_csv("data/leader_2016.csv")
leader_2017 = pd.read_csv("data/leader_2017.csv")
leader_2018 = pd.read_csv("data/leader_2018.csv")
leader_2019 = pd.read_csv("data/leader_2019.csv")
leader_2020 = pd.read_csv("data/leader_2020.csv")

teams = pd.read_csv("data/team_season_comp.csv")
global_seas = pd.read_csv("data/seasons_global.csv")

ml_pos = pd.read_csv("data/ml_position.csv")
ml_predict = pd.read_csv("data/ml_2001_results.csv")

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
I did a MinMax scaler for each season and each position.\n
Then I added the results of points, rebounds, assists, steals, blocks, field goals, 3 points field goals and free throws minus the score of turnovers and fouls.
This result is then multiplied by the result for minutes per games to normalize in function of the time played for these stats.\n
Finally, I made a last MinMax scaler from these results to have a final note from 0 to 10.
"""

age_range_explain = """
You can adapt the range of the players' age with the slider below.
"""

explain_ml_pos = """
To perform this Machine Learning exploration, for each players, I scaled all the datas with a MinMax scaler for the stats Points per games, Field Goals percentage,
3 points percentage, Free Throws percentage, Rebounds per games, Assists per games, Steals per games, Blocks per games, Turnovers per games and Fouls per games,
doing this for each season.\n
We will try to do this for the 5 positions (Point Guard, Shooting Guard, Small Forward, Power Forward and center) and for a generalisation of them
(Guard = point + shooting, Wing = Small Forward, Front = Center and Power Forward). \n
I tried these computations with and without Height and Weight, these stats being directly linked with the position.\n
Note : The Logistic regression is performed with a max_iter = 500 due to the size of the data.
"""

explain_ml_predict = """
To perform this Machine Learning exploration, for each players, I scaled all the datas with a MinMax scaler for the stats Height, Weight, Age,  Points per games,
Field Goals percentage, 3 points percentage, Free Throws percentage, Rebounds per games, Assists per games, Steals per games, Blocks per games, Turnovers per games
and Fouls per games, doing this for the 2001 season.\n
Then I have sorted these data by Teams, Minutes played per games (descending), number of games started (descending) and number of games played(descending).
For each Teams, I only keep the 10 "best" players sorted and, by team, I sort them again by generalized position (Guard, Wing, Front), and by minutes played per games
(descending). \n
The assertion of the machine learning process will be "The home team wins". So for each of the stats of the 10 players per team, I made a substraction of the home teams
player minus the away team player. I have here 10 "oppositions" with all the stats categories. \n
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
          children="Top Players for each year",
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

        html.H5(
          children="Select the year to check",
          style={
             'textAlign': 'center'
          }
        ),

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

        dcc.Markdown(children= explain_notes,style={
           'textAlign': 'left'}
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

                    html.Br(),
                    html.Br()


    ]), # end first tab Players Statistics #####################################################################

    dcc.Tab(label="Teams statistics", children=[

        html.H3(
          children='Teams stats during time',
          style={
             'textAlign': 'center'
          }
        ),


        html.Div([
            html.Div(children=[

                html.Br(),
                html.Br(),

                html.H5(
                  children='Select the team',
                  style={
                     'textAlign': 'center'
                  }
                ),

                html.Br(),

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

#################################################################################################################

        html.Br(),
        html.Br(),

        html.H3(
          children='General evolution of the game',
          style={
             'textAlign': 'center'
          }
        ),


        html.Div([
            html.Div(children=[

                html.Br(),
                html.Br(),

                html.H5(
                  children='Select the stat category',
                  style={
                     'textAlign': 'center'
                  }
                ),

                html.Br(),

            dcc.Dropdown(
                id='stat_select2',
                options=[
                    {'label': 'Points', 'value': 'PTS'},
                    {'label': 'Fiels Goals Made', 'value': 'FGM'},
                    {'label': 'Fiels Goals Attempts', 'value': 'FGA'},
                    {'label': 'Field Goals percentage', 'value': 'FG_PCT'},
                    {'label': '3 points Made', 'value': 'FG3M'},
                    {'label': '3 points Attempts', 'value': 'FG3A'},
                    {'label': '3 points percentage', 'value': 'FG3_PCT'},
                    {'label': 'Free Throws Made', 'value': 'FTM'},
                    {'label': 'Free Throws Attempts', 'value': 'FTA'},
                    {'label': 'Free Throws percentage', 'value': 'FT_PCT'},
                    {'label': 'Offensive Rebounds', 'value': 'OREB'},
                    {'label': 'Defensive Rebounds', 'value': 'DREB'},
                    {'label': 'Rebounds', 'value': 'REB'},
                    {'label': 'Assists', 'value': 'AST'},
                    {'label': 'Steals', 'value': 'STL'},
                    {'label': 'Blocks', 'value': 'BLK'},
                    {'label': 'Turnovers', 'value': 'TOV'},
                    {'label': 'Fouls', 'value': 'PF'}

                ], value='PTS'

            ),


            ], className="four columns"),

            html.Div(children=[
            ], className="eight columns", id='output-container-button8')
        ], className="row")

        ]), # end of the team statistics tab #############################################""



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

    if value17 == "2001":
        fig7 = go.Figure(data=[go.Table(
                header=dict(values=list(leader_2001.columns),
                align='center'),
                cells=dict(values=[leader_2001["SEASON"], leader_2001["STAT"],
                       leader_2001["NAME"], leader_2001["HEIGHT"],leader_2001["WEIGHT"], leader_2001["POST"], leader_2001["AGE"], leader_2001["TEAM"],
                       leader_2001["PPG"], leader_2001["FG_P"], leader_2001["FG3_P"], leader_2001["FT_P"], leader_2001["RPG"], leader_2001["APG"],
                       leader_2001["SPG"], leader_2001["BPG"]],
               align='center'))])

        return html.Div([
                   html.Br(),
                   dcc.Graph(id='g7', figure=fig7, style={
                       'height': 525})])

    elif value17 == "2002":
        fig7 = go.Figure(data=[go.Table(
                header=dict(values=list(leader_2002.columns),
                align='center'),
                cells=dict(values=[leader_2002["SEASON"], leader_2002["STAT"],
                       leader_2002["NAME"], leader_2002["HEIGHT"],leader_2002["WEIGHT"], leader_2002["POST"], leader_2002["AGE"], leader_2002["TEAM"],
                       leader_2002["PPG"], leader_2002["FG_P"], leader_2002["FG3_P"], leader_2002["FT_P"], leader_2002["RPG"], leader_2002["APG"],
                       leader_2002["SPG"], leader_2002["BPG"]],
               align='center'))])

        return html.Div([
                   html.Br(),
                   dcc.Graph(id='g7', figure=fig7, style={
                       'height': 525})])

    elif value17 == "2003":
        fig7 = go.Figure(data=[go.Table(
                header=dict(values=list(leader_2003.columns),
                align='center'),
                cells=dict(values=[leader_2003["SEASON"], leader_2003["STAT"],
                       leader_2003["NAME"], leader_2003["HEIGHT"],leader_2003["WEIGHT"], leader_2003["POST"], leader_2003["AGE"], leader_2003["TEAM"],
                       leader_2003["PPG"], leader_2003["FG_P"], leader_2003["FG3_P"], leader_2003["FT_P"], leader_2003["RPG"], leader_2003["APG"],
                       leader_2003["SPG"], leader_2003["BPG"]],
               align='center'))])

        return html.Div([
                   html.Br(),
                   dcc.Graph(id='g7', figure=fig7, style={
                       'height': 525})])

    elif value17 == "2004":
        fig7 = go.Figure(data=[go.Table(
                header=dict(values=list(leader_2004.columns),
                align='center'),
                cells=dict(values=[leader_2004["SEASON"], leader_2004["STAT"],
                       leader_2004["NAME"], leader_2004["HEIGHT"],leader_2004["WEIGHT"], leader_2004["POST"], leader_2004["AGE"], leader_2004["TEAM"],
                       leader_2004["PPG"], leader_2004["FG_P"], leader_2004["FG3_P"], leader_2004["FT_P"], leader_2004["RPG"], leader_2004["APG"],
                       leader_2004["SPG"], leader_2004["BPG"]],
               align='center'))])

        return html.Div([
                   html.Br(),
                   dcc.Graph(id='g7', figure=fig7, style={
                       'height': 525})])

    elif value17 == "2005":
        fig7 = go.Figure(data=[go.Table(
                header=dict(values=list(leader_2005.columns),
                align='center'),
                cells=dict(values=[leader_2005["SEASON"], leader_2005["STAT"],
                       leader_2005["NAME"], leader_2005["HEIGHT"],leader_2005["WEIGHT"], leader_2005["POST"], leader_2005["AGE"], leader_2005["TEAM"],
                       leader_2005["PPG"], leader_2005["FG_P"], leader_2005["FG3_P"], leader_2005["FT_P"], leader_2005["RPG"], leader_2005["APG"],
                       leader_2005["SPG"], leader_2005["BPG"]],
               align='center'))])

        return html.Div([
                   html.Br(),
                   dcc.Graph(id='g7', figure=fig7, style={
                       'height': 525})])

    elif value17 == "2006":
        fig7 = go.Figure(data=[go.Table(
                header=dict(values=list(leader_2006.columns),
                align='center'),
                cells=dict(values=[leader_2006["SEASON"], leader_2006["STAT"],
                       leader_2006["NAME"], leader_2006["HEIGHT"],leader_2006["WEIGHT"], leader_2006["POST"], leader_2006["AGE"], leader_2006["TEAM"],
                       leader_2006["PPG"], leader_2006["FG_P"], leader_2006["FG3_P"], leader_2006["FT_P"], leader_2006["RPG"], leader_2006["APG"],
                       leader_2006["SPG"], leader_2006["BPG"]],
               align='center'))])

        return html.Div([
                   html.Br(),
                   dcc.Graph(id='g7', figure=fig7, style={
                       'height': 525})])

    elif value17 == "2007":
        fig7 = go.Figure(data=[go.Table(
                header=dict(values=list(leader_2007.columns),
                align='center'),
                cells=dict(values=[leader_2007["SEASON"], leader_2007["STAT"],
                       leader_2007["NAME"], leader_2007["HEIGHT"],leader_2007["WEIGHT"], leader_2007["POST"], leader_2007["AGE"], leader_2007["TEAM"],
                       leader_2007["PPG"], leader_2007["FG_P"], leader_2007["FG3_P"], leader_2007["FT_P"], leader_2007["RPG"], leader_2007["APG"],
                       leader_2007["SPG"], leader_2007["BPG"]],
               align='center'))])

        return html.Div([
                   html.Br(),
                   dcc.Graph(id='g7', figure=fig7, style={
                       'height': 525})])

    elif value17 == "2008":
        fig7 = go.Figure(data=[go.Table(
                header=dict(values=list(leader_2008.columns),
                align='center'),
                cells=dict(values=[leader_2008["SEASON"], leader_2008["STAT"],
                       leader_2008["NAME"], leader_2008["HEIGHT"],leader_2008["WEIGHT"], leader_2008["POST"], leader_2008["AGE"], leader_2008["TEAM"],
                       leader_2008["PPG"], leader_2008["FG_P"], leader_2008["FG3_P"], leader_2008["FT_P"], leader_2008["RPG"], leader_2008["APG"],
                       leader_2008["SPG"], leader_2008["BPG"]],
               align='center'))])

        return html.Div([
                   html.Br(),
                   dcc.Graph(id='g7', figure=fig7, style={
                       'height': 525})])

    elif value17 == "2009":
        fig7 = go.Figure(data=[go.Table(
                header=dict(values=list(leader_2009.columns),
                align='center'),
                cells=dict(values=[leader_2009["SEASON"], leader_2009["STAT"],
                       leader_2009["NAME"], leader_2009["HEIGHT"],leader_2009["WEIGHT"], leader_2009["POST"], leader_2009["AGE"], leader_2009["TEAM"],
                       leader_2009["PPG"], leader_2009["FG_P"], leader_2009["FG3_P"], leader_2009["FT_P"], leader_2009["RPG"], leader_2009["APG"],
                       leader_2009["SPG"], leader_2009["BPG"]],
               align='center'))])

        return html.Div([
                   html.Br(),
                   dcc.Graph(id='g7', figure=fig7, style={
                       'height': 525})])

    elif value17 == "2010":
        fig7 = go.Figure(data=[go.Table(
                header=dict(values=list(leader_2010.columns),
                align='center'),
                cells=dict(values=[leader_2010["SEASON"], leader_2010["STAT"],
                       leader_2010["NAME"], leader_2010["HEIGHT"],leader_2010["WEIGHT"], leader_2010["POST"], leader_2010["AGE"], leader_2010["TEAM"],
                       leader_2010["PPG"], leader_2010["FG_P"], leader_2010["FG3_P"], leader_2010["FT_P"], leader_2010["RPG"], leader_2010["APG"],
                       leader_2010["SPG"], leader_2010["BPG"]],
               align='center'))])

        return html.Div([
                   html.Br(),
                   dcc.Graph(id='g7', figure=fig7, style={
                       'height': 525})])

    elif value17 == "2011":
        fig7 = go.Figure(data=[go.Table(
                header=dict(values=list(leader_2011.columns),
                align='center'),
                cells=dict(values=[leader_2011["SEASON"], leader_2011["STAT"],
                       leader_2011["NAME"], leader_2011["HEIGHT"],leader_2011["WEIGHT"], leader_2011["POST"], leader_2011["AGE"], leader_2011["TEAM"],
                       leader_2011["PPG"], leader_2011["FG_P"], leader_2011["FG3_P"], leader_2011["FT_P"], leader_2011["RPG"], leader_2011["APG"],
                       leader_2011["SPG"], leader_2011["BPG"]],
               align='center'))])

        return html.Div([
                   html.Br(),
                   dcc.Graph(id='g7', figure=fig7, style={
                       'height': 525})])

    elif value17 == "2012":
        fig7 = go.Figure(data=[go.Table(
                header=dict(values=list(leader_2012.columns),
                align='center'),
                cells=dict(values=[leader_2012["SEASON"], leader_2012["STAT"],
                       leader_2012["NAME"], leader_2012["HEIGHT"],leader_2012["WEIGHT"], leader_2012["POST"], leader_2012["AGE"], leader_2012["TEAM"],
                       leader_2012["PPG"], leader_2012["FG_P"], leader_2012["FG3_P"], leader_2012["FT_P"], leader_2012["RPG"], leader_2012["APG"],
                       leader_2012["SPG"], leader_2012["BPG"]],
               align='center'))])

        return html.Div([
                   html.Br(),
                   dcc.Graph(id='g7', figure=fig7, style={
                       'height': 525})])

    elif value17 == "2013":
        fig7 = go.Figure(data=[go.Table(
                header=dict(values=list(leader_2013.columns),
                align='center'),
                cells=dict(values=[leader_2013["SEASON"], leader_2013["STAT"],
                       leader_2013["NAME"], leader_2013["HEIGHT"],leader_2013["WEIGHT"], leader_2013["POST"], leader_2013["AGE"], leader_2013["TEAM"],
                       leader_2013["PPG"], leader_2013["FG_P"], leader_2013["FG3_P"], leader_2013["FT_P"], leader_2013["RPG"], leader_2013["APG"],
                       leader_2013["SPG"], leader_2013["BPG"]],
               align='center'))])

        return html.Div([
                   html.Br(),
                   dcc.Graph(id='g7', figure=fig7, style={
                       'height': 525})])

    elif value17 == "2014":
        fig7 = go.Figure(data=[go.Table(
                header=dict(values=list(leader_2014.columns),
                align='center'),
                cells=dict(values=[leader_2014["SEASON"], leader_2014["STAT"],
                       leader_2014["NAME"], leader_2014["HEIGHT"],leader_2014["WEIGHT"], leader_2014["POST"], leader_2014["AGE"], leader_2014["TEAM"],
                       leader_2014["PPG"], leader_2014["FG_P"], leader_2014["FG3_P"], leader_2014["FT_P"], leader_2014["RPG"], leader_2014["APG"],
                       leader_2014["SPG"], leader_2014["BPG"]],
               align='center'))])

        return html.Div([
                   html.Br(),
                   dcc.Graph(id='g7', figure=fig7, style={
                       'height': 525})])

    elif value17 == "2015":
        fig7 = go.Figure(data=[go.Table(
                header=dict(values=list(leader_2015.columns),
                align='center'),
                cells=dict(values=[leader_2015["SEASON"], leader_2015["STAT"],
                       leader_2015["NAME"], leader_2015["HEIGHT"],leader_2015["WEIGHT"], leader_2015["POST"], leader_2015["AGE"], leader_2015["TEAM"],
                       leader_2015["PPG"], leader_2015["FG_P"], leader_2015["FG3_P"], leader_2015["FT_P"], leader_2015["RPG"], leader_2015["APG"],
                       leader_2015["SPG"], leader_2015["BPG"]],
               align='center'))])

        return html.Div([
                   html.Br(),
                   dcc.Graph(id='g7', figure=fig7, style={
                       'height': 525})])

    elif value17 == "2016":
        fig7 = go.Figure(data=[go.Table(
                header=dict(values=list(leader_2016.columns),
                align='center'),
                cells=dict(values=[leader_2016["SEASON"], leader_2016["STAT"],
                       leader_2016["NAME"], leader_2016["HEIGHT"],leader_2016["WEIGHT"], leader_2016["POST"], leader_2016["AGE"], leader_2016["TEAM"],
                       leader_2016["PPG"], leader_2016["FG_P"], leader_2016["FG3_P"], leader_2016["FT_P"], leader_2016["RPG"], leader_2016["APG"],
                       leader_2016["SPG"], leader_2016["BPG"]],
               align='center'))])

        return html.Div([
                   html.Br(),
                   dcc.Graph(id='g7', figure=fig7, style={
                       'height': 525})])

    elif value17 == "2017":
        fig7 = go.Figure(data=[go.Table(
                header=dict(values=list(leader_2017.columns),
                align='center'),
                cells=dict(values=[leader_2017["SEASON"], leader_2017["STAT"],
                       leader_2017["NAME"], leader_2017["HEIGHT"],leader_2017["WEIGHT"], leader_2017["POST"], leader_2017["AGE"], leader_2017["TEAM"],
                       leader_2017["PPG"], leader_2017["FG_P"], leader_2017["FG3_P"], leader_2017["FT_P"], leader_2017["RPG"], leader_2017["APG"],
                       leader_2017["SPG"], leader_2017["BPG"]],
               align='center'))])

        return html.Div([
                   html.Br(),
                   dcc.Graph(id='g7', figure=fig7, style={
                       'height': 525})])

    elif value17 == "2018":
        fig7 = go.Figure(data=[go.Table(
                header=dict(values=list(leader_2018.columns),
                align='center'),
                cells=dict(values=[leader_2018["SEASON"], leader_2018["STAT"],
                       leader_2018["NAME"], leader_2018["HEIGHT"],leader_2018["WEIGHT"], leader_2018["POST"], leader_2018["AGE"], leader_2018["TEAM"],
                       leader_2018["PPG"], leader_2018["FG_P"], leader_2018["FG3_P"], leader_2018["FT_P"], leader_2018["RPG"], leader_2018["APG"],
                       leader_2018["SPG"], leader_2018["BPG"]],
               align='center'))])

        return html.Div([
                   html.Br(),
                   dcc.Graph(id='g7', figure=fig7, style={
                       'height': 525})])

    elif value17 == "2019":
        fig7 = go.Figure(data=[go.Table(
                header=dict(values=list(leader_2019.columns),
                align='center'),
                cells=dict(values=[leader_2019["SEASON"], leader_2019["STAT"],
                       leader_2019["NAME"], leader_2019["HEIGHT"],leader_2019["WEIGHT"], leader_2019["POST"], leader_2019["AGE"], leader_2019["TEAM"],
                       leader_2019["PPG"], leader_2019["FG_P"], leader_2019["FG3_P"], leader_2019["FT_P"], leader_2019["RPG"], leader_2019["APG"],
                       leader_2019["SPG"], leader_2019["BPG"]],
               align='center'))])

        return html.Div([
                   html.Br(),
                   dcc.Graph(id='g7', figure=fig7, style={
                       'height': 525})])

    elif value17 == "2020":
        fig7 = go.Figure(data=[go.Table(
                header=dict(values=list(leader_2020.columns),
                align='center'),
                cells=dict(values=[leader_2020["SEASON"], leader_2020["STAT"],
                       leader_2020["NAME"], leader_2020["HEIGHT"],leader_2020["WEIGHT"], leader_2020["POST"], leader_2020["AGE"], leader_2020["TEAM"],
                       leader_2020["PPG"], leader_2020["FG_P"], leader_2020["FG3_P"], leader_2020["FT_P"], leader_2020["RPG"], leader_2020["APG"],
                       leader_2020["SPG"], leader_2020["BPG"]],
               align='center'))])

        return html.Div([
            html.Br(),
            dcc.Graph(id='g7', figure=fig7, style={
                'height': 525})
        ])

@app.callback(
    dash.dependencies.Output('output-container-button7', 'children'),
    [dash.dependencies.Input('team_select', 'value'), dash.dependencies.Input('stat_select', 'value')])
def team_stats(value18, value19):

        fig8 = go.Figure()
        fig8.add_trace(go.Scatter(x=teams[teams["TEAM"] == value18]["SEASON"], y=teams[teams["TEAM"] == value18][value19],
                            mode='lines+markers', name=value18))
        fig8.update_layout(title=dict(text = 'Comparison of teams stats', x=0.5),
                           xaxis_title='Age', yaxis_title=value19)

        return html.Div([
        html.Br(),
        dcc.Graph(id='g8', figure=fig8)
        ])

@app.callback(
    dash.dependencies.Output('output-container-button8', 'children'),
    [dash.dependencies.Input('stat_select2', 'value')])
def global_team(value20):

        fig9 = go.Figure()
        fig9.add_trace(go.Scatter(x=global_seas["SEASON"], y=global_seas[value20],
                        mode='lines+markers'))
        fig9.update_layout(title=dict(text = 'Evolution of the game', x=0.5),
                       xaxis_title='Season', yaxis_title=value20)

        return html.Div([
        html.Br(),
        dcc.Graph(id='g9', figure=fig9)
        ])


if __name__ == '__main__':
    app.run_server(debug=True)
