import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

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

    num_of_comp = 1
    max_slider_value = 4
    current_df = df[['Sex','Age','EquipFeat','TotalKg']]
    scaler = StandardScaler()
    scaler.fit(current_df)
    scaled_data = scaler.transform(current_df)
    pca = PCA(n_components=num_of_comp)
    pca.fit(scaled_data)
    x_pca = pca.transform(scaled_data)
    df_comp = pd.DataFrame(pca.components_, columns=current_df.columns)
    fig4 = px.imshow(df_comp)
    fig4.update_layout(template=template)



    dash_app.layout = html.Div(
        style={'background-color':'rgb(17,17,17)', 'color':'grey'},
        children=[
        # All elements from the top of the page
        html.Div([
            dbc.NavbarSimple(
                children=[
                dbc.NavItem(dbc.NavLink("Go Home", href="/", external_link=True)),
            ],
            brand="Data Exploration Dashboard",
            brand_href="/",
            color='#44367F',
            dark=True,

        )
        ], className='row'),
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
                html.H1(children='Scatter'),

                html.Div(children='''
                    You can select a lift and narrow the view by selecting an age range of interest. 
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
                html.H1(children='Box Plot'),

                html.Div(children='''
                    Here you can visualize the percentiles of lifting performances against equipment used for men and 
                    women.
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
                html.H1(children='Heatmap for Principal Component Analysis'),

                html.Div(children='''
                This graph describes how Principal Components correlate with distinct features in the dataset. 
            '''),
                html.P("Features for comparison:"),
                dcc.Checklist(
                    id='feature_list',
                    options=[{'value': 'Sex', 'label': 'Sex'},
                             {'value': 'Age', 'label': 'Age'},
                             {'value': 'EquipFeat', 'label': 'Equipment'},
                             {'value': 'BodyweightKg', 'label': 'Weight'},
                             {'value': 'Best3SquatKg', 'label': 'Squat'},
                             {'value': 'Best3BenchKg', 'label': 'Bench'},
                             {'value': 'Best3DeadliftKg', 'label': 'Deadlift'},
                             {'value': 'TotalKg', 'label': 'TotalKG'}
                             ],
                    value=['Sex','Age','EquipFeat','TotalKg'],
                    labelStyle={'display': 'inline-block'}
                ),
                dcc.Graph(
                    id='graph4',
                    figure=fig4
                ),
                dcc.Slider(
                    id='slider',
                    min=1, max=max_slider_value, step=1,
                    marks={1: '1', 2: '2', 3: '3', 4: '4', 5: '5',
                           6: '6', 7: '7', 8: '8'},
                    value=1
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
#
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
                      template=template,
                      color_discrete_sequence=['#44367F','#29A982'])

        return fig3

    @dash_app.callback(
         dash.dependencies.Output('slider', component_property='value'),
        [dash.dependencies.Input('slider', 'value'),
         dash.dependencies.Input('feature_list', 'value')])
    def update_slider_value(value, features):
        if len(features)<value:
            new_slider_value = len(features)
        else:
            new_slider_value = value

        return new_slider_value


    @dash_app.callback(
        [dash.dependencies.Output('graph4', 'figure'),
         dash.dependencies.Output('slider', component_property='max')],
        [dash.dependencies.Input('slider', 'value'),
         dash.dependencies.Input('feature_list', 'value')])
    def update_pca(value, features):
        num_of_comp = value
        current_df = df[features]
        scaler = StandardScaler()
        scaler.fit(current_df)
        scaled_data = scaler.transform(current_df)
        pca = PCA(n_components=num_of_comp)

        pca.fit(scaled_data)

        x_pca = pca.transform(scaled_data)
        df_comp = pd.DataFrame(pca.components_, columns=current_df.columns)
        fig4 = px.imshow(df_comp)
        fig4.update_layout(template=template)


        return fig4, len(features)