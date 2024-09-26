import pandas as pd
from sqlalchemy import create_engine
from typing import Dict

def fetch_table(username: str, password: str, host: str, port: str, dbname: str, table_name: str) -> pd.DataFrame:
    """
    Fetches a table from a MySQL database and returns it as a pandas DataFrame.

    Parameters:
    username (str): The username for the MySQL database.
    password (str): The password for the MySQL database.
    host (str): The host address of the MySQL database.
    port (str): The port number of the MySQL database.
    dbname (str): The name of the database.
    table_name (str): The name of the table to fetch.

    Returns:
    pd.DataFrame: The table data as a pandas DataFrame.
    """
    connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{dbname}'
    engine = create_engine(connection_string)
    df = pd.read_sql_table(table_name, con=engine)
    return df

def get_mean(df: pd.DataFrame, year: int, base_currency: str = 'USD') -> Dict[str, float]:
    """
    Calculates the mean exchange rate of all currency codes with respect to a given base currency.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the exchange rate data.
    year (int): The year for which to filter the data.
    base_currency (str): The base currency code to which all exchange rates should be converted. Default is 'USD'.

    Returns:
    dict: A dictionary where the key is the currency code and the value is the mean exchange rate with respect to the base currency.
    """
    # Filter the DataFrame based on the specified year
    filtered_df = df.loc[df['Year'] == year]
    
    # Calculate the mean of all columns except "Date" and "Year"
    mean_exchange_rates = filtered_df.drop(columns=['Date', 'Year']).mean()
    
    # Include USD with base USD (assuming USD is 1)
    mean_exchange_rates['USD'] = 1.0
    
    # Get the exchange rate of the base currency
    base_rate = mean_exchange_rates[base_currency]
    
    # Convert all exchange rates to the new base currency
    mean_exchange_rates = mean_exchange_rates / base_rate
    
    # Set the base currency exchange rate to 1
    mean_exchange_rates[base_currency] = 1.0
    
    return mean_exchange_rates.to_dict()
