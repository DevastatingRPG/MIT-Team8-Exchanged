from dash import callback, Output, Input
import plotly.express as px
import pandas as pd
import polars as pl
from dotenv import load_dotenv, find_dotenv
import os
import requests
from datetime import datetime

# Load environment variables from .env file
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
# print(f"Loaded dotenv path: {dotenv_path}")

# Access the API key
api_key = os.getenv('API_KEY')
# print(api_key)
base_url = f'https://openexchangerates.org/api'

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

def fetchData(url):
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def get_fx_rates(base_currency="USD", date=None):
    today_date = datetime.today().strftime('%Y-%m-%d')

    if date == today_date or date == None:
        url = base_url + f"/latest.json?app_id={api_key}"
    else:
        url = base_url + f"/historical/{date}.json?app_id={api_key}"
    rates = fetchData(url)['rates']
    table_data = [{'Currency': currency, 'Rate': rate} for currency, rate in rates.items()]
    table_df = pd.DataFrame(table_data)
    return table_df

def get_currencies():
    url = base_url + '/currencies.json'
    currencies = fetchData(url)
    rates = get_fx_rates()
    rates['Description'] = rates['Currency'].map(currencies)
    return rates
    
    
        

def register_callbacks(app):
    @app.callback(
        Output('graph-content', 'figure'),
        Input('dropdown-selection', 'value')
    )
    def update_graph(value):
        dff = df[df.country == value]
        return px.line(dff, x='year', y='pop')
    
    @app.callback(
        Output('fx-table', 'data'),
        [Input('base-currency-dropdown', 'value'), Input('date-picker-single', 'date')]
    )
    def update_fx_graph(base, date):
        rates = get_fx_rates(base, date)
    
        get_currencies()
        # print(get_currencies())
        return rates.to_dict(orient='records')