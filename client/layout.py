from dash import html, dcc
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

def create_layout():
    return html.Div([
        html.H1(children='Title of Dash App', style={'textAlign':'center'}),
        dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
        dcc.Graph(id='graph-content')
    ])