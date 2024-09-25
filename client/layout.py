from dash import html, dcc, dash_table
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')
currency_codes = ["USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", "SEK", "NZD"]

def create_layout():
    return html.Div([
        html.H1(children='Title of Dash App', style={'textAlign':'center'}),
        dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
        dcc.Graph(id='graph-content'),

        html.Label('Select Base Currency'),
        dcc.Dropdown(currency_codes, 'USD', id='base-currency-dropdown', style={'width': '50%'}),
        html.Label('Select Date Range'),
        dcc.DatePickerSingle(
            id='date-picker-single',
            date='2022-01-01',
            display_format='YYYY-MM-DD'
        ),
        dcc.Graph(id='fx-graph'),
        dash_table.DataTable(id='fx-table', columns=[
            {'name': 'Currency', 'id': 'Currency'},
            {'name': 'Rate', 'id': 'Rate'}
        ])


    ])