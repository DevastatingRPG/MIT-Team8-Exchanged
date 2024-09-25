import polars as pl
from dotenv import load_dotenv
import os
import requests
from datetime import datetime
from sklearn.preprocessing import StandardScaler, MinMaxScaler


load_dotenv()

api_key = os.getenv('API_KEY')
base_url = f'https://openexchangerates.org/api'
scaler = MinMaxScaler(feature_range=(0, 1))

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

    if base_currency != "USD" and base_currency in rates:
            base_rate = rates[base_currency]
            rates = {currency: rate / base_rate for currency, rate in rates.items()}
            rates[base_currency] = 1.0  # Set the base currency rate to 1

    rates_df = pl.DataFrame({"Currency": list(rates.keys()), "Rate": list(rates.values())})
    return rates_df

def get_currencies_list():
    url = base_url + '/currencies.json'
    currencies = fetchData(url)
    return list(currencies.keys())

def get_currencies_fx():
    url = base_url + '/currencies.json'
    currencies = fetchData(url)
    rates_df = get_fx_rates()
    rates_df = rates_df.with_columns(
        pl.col("Currency").map_elements(lambda x: currencies.get(x, "N/A"), return_dtype=pl.String).alias("Description")
    )
    rates_df = rates_df.select(["Currency", "Description", "Rate"])
    
    return rates_df
