import polars as pl
from dotenv import load_dotenv
import os
import requests
from datetime import datetime
from sklearn.preprocessing import StandardScaler


load_dotenv()

api_key = os.getenv('API_KEY')
base_url = f'https://openexchangerates.org/api'
scaler = StandardScaler()

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
    rates_df = pl.DataFrame({"Currency": list(rates.keys()), "Rate": list(rates.values())})
    return rates_df

def get_currencies():
    url = base_url + '/currencies.json'
    currencies = fetchData(url)
    rates_df = get_fx_rates()
    normalized_rates = scaler.fit_transform(rates_df['Rate'].to_numpy().reshape(-1, 1)).flatten()

    rates_df = rates_df.with_columns(
        [pl.col("Currency").map_elements(lambda x: currencies.get(x, "N/A"), return_dtype=pl.String).alias("Description"),
        pl.Series("Normalized_Rate", normalized_rates) ]
    )
    rates_df = rates_df.select(["Currency", "Description", "Rate"])
    # rates_df = rates_
    # rates_df = rates_df.with_columns(
    #     pl.col("Rate").map_elements(lambda x: scaler.fit_transform(x.reshape(-1, 1)).flatten(), return_dtype=pl.Float64).alias("Normalized_Rate")
    # )

    scaler.fit([rates_df['Rate']])
    
    return rates_df
