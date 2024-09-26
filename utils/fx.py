import polars as pl
import pandas as pd
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
    return rates_df.to_pandas(), rates

def get_currencies_list():
    url = base_url + '/currencies.json'
    currencies = fetchData(url)
    return list(currencies.keys())

def get_currencies_fx():
    url = base_url + '/currencies.json'
    currencies = fetchData(url)
    rates_df, _ = get_fx_rates()
    
    # Add the Description column by mapping the Currency column to the currencies dictionary
    rates_df['Description'] = rates_df['Currency'].map(currencies).fillna('N/A')
    
    # Select only the required columns
    rates_df = rates_df[['Currency', 'Description', 'Rate']]
    
    return rates_df

def update_df_with_latest_fx(df: pd.DataFrame) -> pl.DataFrame:
    """
    Checks if the current date is in the given DataFrame, and if it isn't, adds an entry using the API.

    Parameters:
    df (pl.DataFrame): The DataFrame containing the FX rates.
    base_currency (str): The base currency code to which all exchange rates should be converted. Default is 'USD'.

    Returns:
    pl.DataFrame: The updated DataFrame with the latest FX rates if the current date was not present.
    """
    base_currency = "USD"
    today_date = datetime.today().strftime('%Y-%m-%d')
    current_year = datetime.today().year
    # Check if the current date is in the DataFrame
    if today_date not in df['Date'].to_list():
        # Fetch the latest FX rates
        _, latest_fx_dict = get_fx_rates(base_currency=base_currency)
        # Create a dictionary with Date and Year
        latest_fx_dict.update({'Date': today_date, 'Year': current_year})
        
        # Create a new row with only the columns that exist in the original DataFrame
        new_row = {col: latest_fx_dict.get(col, None) for col in df.columns}
        
        # Convert the dictionary to a DataFrame with one row
        latest_fx_row = pd.DataFrame([new_row])
        latest_fx_row['Date'] = pd.to_datetime(latest_fx_row['Date'], format='%Y-%m-%d')

        # Concatenate the new row to the existing DataFrame
        df = pd.concat([df, latest_fx_row], ignore_index=True)

    return df
