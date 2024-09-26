import pandas as pd
from sqlalchemy import create_engine

def fetch_table(username, password, host, port, dbname, table_name):
    connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{dbname}'
    engine = create_engine(connection_string)
    df = pd.read_sql_table(table_name, con=engine)
    return df

def get_mean(df, year, base_currency='USD'):
    filtered_df = df.loc[df['Year'] == year]
    mean_exchange_rates = filtered_df.drop(columns=['Date', 'Year']).mean()
    
    # Include USD with base USD (assuming USD is 1)
    mean_exchange_rates['USD'] = 1.0
    
    # Get the exchange rate of the base currency
    base_rate = mean_exchange_rates[base_currency]
    
    # Convert all exchange rates to the new base currency
    mean_exchange_rates = mean_exchange_rates / base_rate
    
    # Set the base currency exchange rate to 1
    mean_exchange_rates[base_currency] = 1.0
    # print(mean_exchange_rates)
    return mean_exchange_rates.to_dict()

