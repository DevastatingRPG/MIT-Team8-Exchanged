from dash import callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

def register_callbacks(app):
    @app.callback(
        Output('graph-content', 'figure'),
        Input('dropdown-selection', 'value')
    )
    def update_graph(value):
        dff = df[df.country == value]
        return px.line(dff, x='year', y='pop')