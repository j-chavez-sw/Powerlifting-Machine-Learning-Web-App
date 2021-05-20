import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


stylesheet = ["https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css"]

def init_dash_app(flask_app):
    dash_app = dash.Dash(__name__, server=flask_app, url_base_pathname='/visualize/', external_stylesheets=stylesheet)

    df_bar = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    })

    df = pd.read_csv('df4.csv')

    # fig = px.bar(df_bar, x="Fruit", y="Amount", color="City", barmode="group")
    print(df.info())
    fig = px.bar(df, x="Age", y="TotalKg", color="Equipment", barmode="group")
    fig2 = px.scatter(df, x="Age", y="TotalKg", color="Equipment", opacity=0.1)
    fig3 = px.box(df, x="Equipment", y="TotalKg")
    fig4 = go.Figure(data=go.Heatmap(
                z=df["TotalKg"],
                x=df["Equipment"],
                y=df["Age"],
                colorscale='Viridis'))


    dash_app.layout = html.Div(children=[
        # All elements from the top of the page
        html.Div([
            html.Div([
                html.H1(children='Hello Dash'),

                html.Div(children='''
                    Dash: A web application framework for Python.
                '''),

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

                dcc.Graph(
                    id='graph2',
                    figure=fig2
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