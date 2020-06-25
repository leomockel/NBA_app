from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash
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



df = px.data.iris()

fig = go.Figure(data=[go.Table(
    header=dict(values=list(df.columns),
                align='left'),
    cells=dict(values=[df.sepal_length, df.sepal_width, df.petal_length, df.petal_width, df.species, df.species_id],
               align='left'))
])


app.title = "20 Years of NBA Statistics"
markdown_text = """
This app is a data student project. Most of the informations for the statistics comes from an API named nba-api 1.1.8,
enriched with a scraping of the website www.basketball-reference.com.
"""

markdown_text2 = """
In this section, we automatically fit a Support Vector Machine using the columns and the parameters specified in the left columns.
The reusults are displayed int the right column.
"""

# All our figures

fig1 = px.scatter(df, x="sepal_width", y="sepal_length",
            color="species", size='petal_length',
            hover_data=['petal_width'])

fig2 = px.scatter_3d(df, x='sepal_length', y='sepal_width',z='petal_width', color='species')

fig3 = px.violin(df, y="sepal_width", color="species_id",
                box=True, points="all", hover_data=df.columns)

fig4 = px.parallel_coordinates(df, color="species_id",
                              color_continuous_scale=px.colors.diverging.Tealrose,
                              color_continuous_midpoint=2)

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
          children='Dataset',
          style={
             'textAlign': 'center'
          }
        ),

        dcc.Graph(figure=fig),

        html.H3(
          children='Scatterplot',
          style={
             'textAlign': 'center'
          }
        ),

        dcc.Graph(figure=fig1),

        # Two columns charts
        html.Div([
            html.Div([
                html.H3(
                  children='3D-plot',
                  style={
                     'textAlign': 'center'
                  }
                ),

                dcc.Graph(figure=fig2)

            ], className="six columns"),

            html.Div([
                html.H3(
                  children='Violin-plot',
                  style={
                     'textAlign': 'center'
                  }
                ),

                dcc.Graph(figure=fig3)

            ], className="six columns"),
        ], className="row"),

        html.H3(
          children='Parallel Coordinates',
          style={
             'textAlign': 'center'
          }
        ),

        dcc.Graph(figure=fig4)

    ]),

    dcc.Tab(label="3D-Graphs", children=[
        html.Div([
            html.Div(children=[
                html.H3(
                  children='Columns to plot',
                  style={
                     'textAlign': 'center'
                  }
                ),
                dcc.Dropdown(
                    id='dropdown3d',
                    options=[
                        {'label': 'Sepal Length', 'value': 'sepal_length'},
                        {'label': 'Sepal Width', 'value': 'sepal_width'},
                        {'label': 'Petal Length', 'value': 'petal_length'},
                        {'label': 'Petal Width', 'value': 'petal_width'}

                ],
                value=['sepal_length', 'petal_length', 'petal_width'],
                multi=True
                )
            ], className="three columns"),

            html.Div(children=[
            ], className="nine columns", id='output-3d-button')
        ], className="row")
    ]),


    dcc.Tab(label="Model Prediction", children=[
        html.Div([
            html.Div(children=[

                dcc.Markdown(children= markdown_text2
                ),

                html.H3(
                  children='Model to use',
                  style={
                     'textAlign': 'center'
                  }
                ),

                dcc.Dropdown(
                    id='model',
                    options=[
                            {'label': 'KNN', 'value': 'KNN'},
                            {'label': 'SVC', 'value': 'SVC'}
                            ],
                            value='KNN'
                ),

                html.H3(
                  children='Columns to predict',
                  style={
                     'textAlign': 'center'
                  }
                ),

                dcc.Dropdown(
                    id='columns to predict',
                    options=[
                            {'label': 'Species Id', 'value': 'species_id'},
                            {'label': 'Sepal Length', 'value': 'sepal_length', "disabled": True},
                            {'label': 'Sepal Width', 'value': 'sepal_width', "disabled": True},
                            {'label': 'Petal Length', 'value': 'petal_length', "disabled": True},
                            {'label': 'Petal Width', 'value': 'petal_width', "disabled": True}
                            ],
                            value='species_id'
                ),

                html.H3(
                  children='Feature Columns',
                  style={
                     'textAlign': 'center'
                  }
                ),
                dcc.Dropdown(
                    id='demo-dropdown1',
                    options=[
                        {'label': 'Species Id', 'value': 'species_id', "disabled": True},
                        {'label': 'Sepal Length', 'value': 'sepal_length'},
                        {'label': 'Sepal Width', 'value': 'sepal_width'},
                        {'label': 'Petal Length', 'value': 'petal_length'},
                        {'label': 'Petal Width', 'value': 'petal_width'}

                ],
                value=['sepal_length', 'sepal_width', 'petal_length', 'petal_width'],
                multi=True
                ),

                html.H3(
                  children='Test size',
                  style={
                     'textAlign': 'center'
                  }
                ),

                dcc.Slider(
                    id='my_slider',
                    min=0.1,
                    max=0.5,
                    step=0.05,
                    value=0.25,
                    marks={
                        0.10: '0.1',
                        0.20: '0.2',
                        0.30: '0.3',
                        0.40: '0.4',
                        0.50: '0.5'
                        },
                )

     ], className="six columns"),

    html.Div(children=[
    html.H3('SVM Model training'),
    ], className="six columns", id='output-container-button')
], className="row")

    ])
])

], style={'width': '75%', 'textAlign': 'center', 'margin-left':'12.5%', 'margin-right':'0'})

@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('demo-dropdown1', 'value'), dash.dependencies.Input('my_slider', 'value'), dash.dependencies.Input('model', 'value')])
def train_model(value2, value3, value4):

        if len(value2) < 1:
            return "Please select at least 1 column"
        else:
            X_train, X_test, y_train, y_test = train_test_split(df[value2], df['species'], test_size=value3)

            if value4 == "KNN":
                clf = KNN()

            elif value4 == "SVC":
                clf = SVC(gamma='auto', probability=True)

            clf.fit(X_train, y_train)
            pred = clf.predict(X_test)
            acc = np.round(accuracy_score(pred, y_test),3)

            fig5 = px.scatter_3d(x=clf.predict_proba(X_test)[:,0], y=clf.predict_proba(X_test)[:,1], z=clf.predict_proba(X_test)[:,2], color=clf.predict(X_test))

            return html.Div([
                html.Br(),
                html.H6('Model accuracy %s'%str(acc)),
                html.Br(),
                dcc.Graph(id='g5', figure=fig5)
            ])

@app.callback(
    dash.dependencies.Output('output-3d-button', 'children'),
    [dash.dependencies.Input('dropdown3d', 'value')])
def viz_3d(values):
    if len(values) != 3:
        return "Please, select 3 columns"
    else:
        fig6 = px.scatter_3d(df, x=values[0], y=values[1], z=values[2], color='species')

        fig6.update_layout(
                autosize=True,
                height=500
            )

        return html.Div([
            html.Br(),
            dcc.Graph(id='g6', figure=fig6)
        ])


if __name__ == '__main__':
    app.run_server(debug=True)
