import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from utils import fx


def load_data(file_path):
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y')
    return df

file_path = 'data/Exchange_Rate_Report_2012.csv' #For testing. Here, actual fetching from database will take place
exchange_rate_data = load_data(file_path)

def resample_data(df, currency_col, frequency):
    resampled_df = df[['Date', currency_col]].dropna()
    resampled_df = resampled_df.resample(frequency, on='Date').mean().reset_index()
    return resampled_df

# Top Navigation Bar
selected = option_menu(
    menu_title=None,  # No title for the menu
    options=["Exchange Rate Dashboard", "Custom Currency Basket", "Currencies"],  # Menu options
    icons=["graph-up-arrow", "basket"],  # Icons for each menu option
    default_index=0,  # Which option is selected by default
    orientation="horizontal",  # Horizontal menu
)

if selected == "Exchange Rate Dashboard":
    st.title("Currency Exchange Rate Dashboard")

    currencies = exchange_rate_data.columns[1:]  # Skip 'Date' column
    currency_selected = st.selectbox("Select a Currency:", currencies)

    start_date = st.date_input("Start Date", value=exchange_rate_data['Date'].min().date())
    end_date = st.date_input("End Date", value=exchange_rate_data['Date'].max().date())
    filtered_data = exchange_rate_data[(exchange_rate_data['Date'] >= pd.to_datetime(start_date)) & 
                                       (exchange_rate_data['Date'] <= pd.to_datetime(end_date))]


    frequency_options = {'Weekly': 'W', 'Monthly': 'M', 'Quarterly': 'Q', 'Yearly': 'Y'}
    frequency_selected = st.selectbox("Select Chart Frequency:", list(frequency_options.keys()))


    resampled_data = resample_data(filtered_data, currency_selected, frequency_options[frequency_selected])

    fig = px.line(resampled_data, x='Date', y=currency_selected, title=f'{currency_selected} Exchange Rate Trend')
    st.plotly_chart(fig)

    if not resampled_data.empty:
        highest_rate = resampled_data[currency_selected].max()
        highest_rate_date = resampled_data[resampled_data[currency_selected] == highest_rate]['Date'].iloc[0]
        
        lowest_rate = resampled_data[currency_selected].min()
        lowest_rate_date = resampled_data[resampled_data[currency_selected] == lowest_rate]['Date'].iloc[0]
        
        st.write(f"**Highest Rate**: {highest_rate} on {highest_rate_date.date()}")
        st.write(f"**Lowest Rate**: {lowest_rate} on {lowest_rate_date.date()}")

elif selected == "Custom Currency Basket":
    st.title("Custom Currency Basket")

    basket_currencies = st.multiselect("Select Currencies for Basket", exchange_rate_data.columns[1:])
    basket_weights = {}
    
    for currency in basket_currencies:
        basket_weights[currency] = st.slider(f"Weight of {currency}:", 0, 100, 50)

    total_weight = sum(basket_weights.values())

    if total_weight > 100:
        st.error("Total weight exceeds 100%. Please adjust the weights.")
    else:
        st.success(f"Total weight: {total_weight}%")

        if basket_currencies:
            st.write("Your custom basket is:")
            for currency, weight in basket_weights.items():
                st.write(f"- {currency}: {weight}%")

elif selected == "Currencies":
    rates = fx.get_currencies()
    st.dataframe(rates, use_container_width=True)

    fig = px.bar(rates, x='Currency', y='Rate', title='Currency Exchange Rates', labels={'Rate': 'Exchange Rate'})
    st.plotly_chart(fig, use_container_width=True)
    pass
