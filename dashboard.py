import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from dash.dependencies import Input, Output
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('df4.csv')
df_m = df[df['Sex'] == 1]
df_f = df[df['Sex'] == 0]
sex_index = {1: 'Men', 0: 'Women'}
stylesheet = ["https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css"]
template = "plotly_dark"

def init_dash_app(flask_app):
    dash_app = dash.Dash(__name__, server=flask_app, url_base_pathname='/visualize/', external_stylesheets=stylesheet)

    df = pd.read_csv('df4.csv')

    fig = go.Figure()
    fig.add_trace(go.Histogram(x=df_m['TotalKg'],
                               # y=df_m['TotalKg'],
                               name='Men',
                               xbins=dict(size=1.5),
                               opacity=0.75,
                               marker=dict(
                                   color='#29A982',)
                               ))
    fig.add_trace(go.Histogram(x=df_f['TotalKg'],
                               # y=df_f['TotalKg'],
                               name='Women',
                               xbins=dict(size=1.5),
                               opacity=0.75,
                               marker=dict(
                                   color='#44367F',)
                               ))
    fig.update_layout(template=template)

    print(df.info())
    fig2 = go.Figure()

    fig2.add_trace(go.Scattergl(
        x=df_m["Age"],
        y=df_m["TotalKg"],
        mode='markers',
        marker=dict(color='#29A982',
                    size=1,
                    colorscale='Viridis')
    ))
    fig2.add_trace(go.Scattergl(
        x=df_f["Age"],
        y=df_f["TotalKg"],
        mode='markers',
        marker=dict(color='#44367F',
                    size=1,
                    colorscale='Viridis')
    ))
    fig2.update_layout(template=template)
    new_col_map = df['Sex'].map(sex_index)
    fig3 = px.box(df,
                  x="Equipment",
                  y="TotalKg",
                  color=new_col_map,
                  template=template)
    fig4 = go.Figure(data=go.Heatmap(
                z=df["TotalKg"],
                x=df["Equipment"],
                y=df["Age"],
                colorscale='Viridis'))
    fig4.update_layout(template=template)


    dash_app.layout = html.Div(
        style={'background-color':'rgb(17,17,17)', 'color':'grey'},
        children=[
        # All elements from the top of the page
        html.Div([
            html.Div([

                html.H1(children='Histogram'),

                html.Div(children='''
                    The distribution of the Big 3 lift performances for men and women.
                    Please select the lift you are interested in. 
                    '''),
                dcc.Dropdown(
                    searchable=False, clearable=False,
                    id='graph_1',
                    style={'width':'50%', 'background-color':'rgb(17,17,17)', 'color':'grey'},
                    options=[
                        {'label': 'Best Total', 'value': 'TotalKg'},
                        {'label': 'Squat', 'value': 'Best3SquatKg'},
                        {'label': 'Bench', 'value': 'Best3BenchKg'},
                        {'label': 'Deadlift', 'value': 'Best3DeadliftKg'},
                    ],
                    value='TotalKg'
                ),
                dcc.Graph(
                    id='graph1',
                    figure=fig
                ),
            ], className="col-6"),
            html.Div([
                html.H1(children='Hello Dash'),

                html.Div(children='''
                    Dash: A web application framework for Python.
                '''),
                dcc.Dropdown(
                    searchable=False, clearable=False,
                    id='graph_2',
                    style={'width': '50%', 'background-color': 'rgb(17,17,17)', 'color': 'grey'},
                    options=[
                        {'label': 'Best Total', 'value': 'TotalKg'},
                        {'label': 'Squat', 'value': 'Best3SquatKg'},
                        {'label': 'Bench', 'value': 'Best3BenchKg'},
                        {'label': 'Deadlift', 'value': 'Best3DeadliftKg'},
                    ],
                    value='TotalKg'
                ),
                dcc.Graph(
                    id='graph2',
                    figure=fig2
                ),
                dcc.RangeSlider(
                    id='range-slider',
                    min=0, max=100, step=1,
                    marks={0: '0', 10: '10', 20: '20', 30: '30', 40: '40', 50: '50',
                           60: '60', 70: '70', 80: '80', 90: '90', 100: '100'},
                    value=[0, 100]
                ),
            ], className="col-6"),
        ], className='row'),
        # New Div for all elements in the new 'row' of the page
        html.Div([
            html.Div([
                html.H1(children='Hello Dash'),

                html.Div(children='''
                    Dash: A web application framework for Python.
                '''),
                html.P("x-axis:"),
                dcc.Checklist(
                    id='x-axis',
                    options=[{'value': 0, 'label': 'Raw'},
                             {'value': 1, 'label': 'Single-Ply'},
                             {'value': 2, 'label': 'Wraps'},
                             {'value': 3, 'label': 'Multi-ply'}],
                    value=[0, 1, 2, 3],
                    labelStyle={'display': 'inline-block'}
                ),
                html.P("y-axis:"),
                dcc.Dropdown(
                    searchable=False, clearable=False,
                    id='y-axis',
                    style={'width': '50%', 'background-color': 'rgb(17,17,17)', 'color': 'grey'},
                    options=[
                        {'label': 'Best Total', 'value': 'TotalKg'},
                        {'label': 'Squat', 'value': 'Best3SquatKg'},
                        {'label': 'Bench', 'value': 'Best3BenchKg'},
                        {'label': 'Deadlift', 'value': 'Best3DeadliftKg'},
                    ],
                    value='TotalKg'
                ),
                dcc.Graph(
                    id='graph3',
                    figure=fig3
                ),
            ], className="col-6"),
            html.Div([
                html.H1(children='Hello Dash'),

                html.Div(children='''
                Dash: A web application framework for Python.
            '''),

                dcc.Graph(
                    id='graph4',
                    figure=fig4
                ),
            ], className="col-6"),
        ], className='row')])

    ################Callbacks#######################
    @dash_app.callback(
        dash.dependencies.Output('graph1', 'figure'),
        [dash.dependencies.Input('graph_1', 'value')])
    def update_bar_chart(value):
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=df_m[value],
                                   # y=df_m['TotalKg'],
                                   name='Men',
                                   xbins=dict(size=1.5),
                                   opacity=0.75,
                                   marker=dict(
                                       color='#29A982', )
                                   ))
        fig.add_trace(go.Histogram(x=df_f[value],
                                   # y=df_f['TotalKg'],
                                   name='Women',
                                   xbins=dict(size=1.5),
                                   opacity=0.75,
                                   marker=dict(
                                       color='#44367F', )
                                   ))
        fig.update_layout(template=template)
        return fig

    @dash_app.callback(
        dash.dependencies.Output('graph2', 'figure'),
        [dash.dependencies.Input('range-slider', 'value'),
         dash.dependencies.Input('graph_2', 'value')])
    def update_scatter(value, selection):
        lower = value[0]
        upper = value[1]
        current_data_m = df_m[(df_m["Age"] >= lower) & (df_m["Age"] <= upper)]
        current_data_f = df_f[(df_f["Age"] >= lower) & (df_f["Age"] <= upper)]
        fig2 = go.Figure()

        fig2.add_trace(go.Scattergl(
            x=current_data_m["Age"],
            y=current_data_m[selection],
            mode='markers',
            name='Men',
            marker=dict(color='#29A982',
                        size=10,
                        colorscale='Viridis')
        ))
        fig2.add_trace(go.Scattergl(
            x=current_data_f["Age"],
            y=current_data_f[selection],
            mode='markers',
            name='Women',
            marker=dict(color='#44367F',
                        size=10,
                        colorscale='Viridis')
        ))
        fig2.update_layout(template=template)

        return fig2

    @dash_app.callback(
        Output("graph3", "figure"),
        [Input("x-axis", "value"),
         Input("y-axis", "value")])
    def update_box_chart(equipment, lift):

        current_data = df[df['EquipFeat'].isin(equipment)]
        new_col_map = current_data['Sex'].map(sex_index)
        fig3 = px.box(current_data,
                      x=current_data['EquipFeat'],
                      y=current_data[lift],
                      color=new_col_map,
                      template=template)

        return fig3


