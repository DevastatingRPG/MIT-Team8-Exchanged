import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_option_menu import option_menu
from pymongo import MongoClient

def render_footer():
    footer_html = """
    <style>
    .footer {
        position: relative;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #2C3E50; /* Darker background color */
        color: #ECF0F1; /* Light text color */
        text-align: center;
        padding: 20px 10px; /* Increased padding */
        font-size: 18px; /* Larger font size */
        font-family: 'Verdana', sans-serif; /* Different font */
        z-index: 1000;
    }
    .footer p {
        margin: 0;
    }
    .footer a {
        color: #ECF0F1; /* Consistent link color */
        text-decoration: none;
        margin: 0 15px; /* More space between links */
    }
    .footer a:hover {
        text-decoration: underline; /* Underline on hover */
        color: #3498DB; /* Change color on hover */
    }
    .footer-icons {
        margin-top: 15px; /* Increased spacing above icons */
    }
    .footer-icons img {
        width: 30px; /* Larger icon size */
        height: 30px; /* Larger icon size */
        margin: 0 10px; /* More space between icons */
        transition: transform 0.2s; /* Smooth scale on hover */
    }
    .footer-icons img:hover {
        transform: scale(1.1); /* Scale effect on hover */
    }
    </style>
    <div class="footer">
        <p>© 2024 Developed by Team 8</p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)


client = MongoClient('mongodb://localhost:27017/')
db = client['exchange_rate_database']
collections = db.list_collection_names()

dataframes = []

for collection_name in collections:
    collection = db[collection_name]
    fetched_df = pd.DataFrame(list(collection.find()))
    
   
    if '_id' in fetched_df.columns:
        fetched_df.drop('_id', axis=1, inplace=True)

    dataframes.append(fetched_df)

df = pd.concat(dataframes, ignore_index=True)

def calculate_hv(df, currency_col, period):
    df = df[['Date', currency_col]].dropna()
    df = df.set_index('Date')

    if period == 'monthly':
        returns = df[currency_col].resample('M').last().pct_change()
    elif period == 'quarterly':
        returns = df[currency_col].resample('Q').last().pct_change()
    elif period == 'weekly':
        returns = df[currency_col].resample('W').last().pct_change()
    else:
        returns = pd.DataFrame()

    if returns.empty:
        return None, pd.DataFrame()

    # Calculate volatility as the standard deviation of returns
    volatility = returns.std() * np.sqrt(len(returns))

    return volatility, returns

def modify_data(df):
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y')
    return df

exchange_rate_data = modify_data(df)

# def resample_data(df, currency_col, frequency):
#     sumofnulls = df[['Date', currency_col]].isnull().sum()
#     resampled_df = df[['Date', currency_col]].dropna()
#     resampled_df = resampled_df.resample(frequency, on='Date').mean().reset_index()
#     return resampled_df,sumofnulls

selected = option_menu(
    menu_title=None,
    options=["Exchange Rate Dashboard", "Custom Currency Basket", "Risk Factor"],
    icons=["graph-up-arrow", "basket", "graph-down"],
    default_index=0,
    orientation="horizontal",
)

if selected == "Exchange Rate Dashboard":
    st.title("Currency Exchange Rate Dashboard")

    currencies = exchange_rate_data.columns[1:] 
    currency_1 = st.selectbox("Select a Currency(to compare):", currencies)
    currency_2 = st.selectbox("Select Base Currency:", currencies)

    start_date = st.date_input("Start Date", value=exchange_rate_data['Date'].min().date())
    end_date = st.date_input("End Date", value=exchange_rate_data['Date'].max().date())
    filtered_data = exchange_rate_data[(exchange_rate_data['Date'] >= pd.to_datetime(start_date)) & 
                                       (exchange_rate_data['Date'] <= pd.to_datetime(end_date))]

    frequency_options = {'Weekly': 'W', 'Monthly': 'M', 'Quarterly': 'Q', 'Yearly': 'Y'}
    frequency_selected = st.selectbox("Select Chart Frequency:", list(frequency_options.keys()))

    
    resampled_data = filtered_data.resample(frequency_options[frequency_selected], on='Date').mean()

    
    resampled_data = resampled_data.reset_index()

    resampled_data['Currency 1 / Currency 2'] = resampled_data[currency_1] / resampled_data[currency_2]

    # Plotting the detailed chart
    fig = px.line(
        resampled_data, x='Date', y='Currency 1 / Currency 2',
        title=f'{currency_1} <br >                  vs <br>{currency_2} <br>Exchange Rate Trend', markers=True
    )

    # Customize layout
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title=f'{currency_1} <br>in terms of {currency_2}',
        title_x=0.5,  # Center title horizontally
        title_y=0.9,  # Adjust vertical title position (optional)
        title_font=dict(size=18),  # Adjust the title font size
        showlegend=True,
        xaxis=dict(showgrid=True),  # Show gridlines on x-axis
        yaxis=dict(showgrid=True),  # Show gridlines on y-axis
        hovermode='x unified',  # Unified hover effect
    )

    # Add annotations for highest and lowest rates
    if not resampled_data.empty:
        highest_rate = (resampled_data[currency_1] / resampled_data[currency_2]) .max()
        highest_rate_date = resampled_data[(resampled_data[currency_1] / resampled_data[currency_2]) == highest_rate]['Date'].iloc[0]
        fig.add_annotation(x=highest_rate_date, y=highest_rate,
                           text=f"Highest: {highest_rate}",
                           showarrow=True, arrowhead=2, ax=0, ay=-40, font=dict(color='green'))

        lowest_rate = (resampled_data[currency_1] / resampled_data[currency_2]).min()
        lowest_rate_date = resampled_data[(resampled_data[currency_1] / resampled_data[currency_2]) == lowest_rate]['Date'].iloc[0]
        fig.add_annotation(x=lowest_rate_date, y=lowest_rate,
                           text=f"Lowest: {lowest_rate}",
                           showarrow=True, arrowhead=2, ax=0, ay=40, font=dict(color='red'))

    st.plotly_chart(fig)

    if not resampled_data.empty:
        st.write(f"**Highest Rate**: {highest_rate} on {highest_rate_date.date()}")
        st.write(f"**Lowest Rate**: {lowest_rate} on {lowest_rate_date.date()}")


elif selected == "Custom Currency Basket":
    st.title("Custom Currency Basket")


    basket_size = st.number_input("Enter Basket Size:", min_value=1, max_value=1000, value=100, step=1)

    base_currency = st.selectbox("Select Base Currency", exchange_rate_data.columns[1:])

    basket_currencies = st.multiselect("Select Currencies for Basket", exchange_rate_data.columns[1:])
    
    basket_weights = {}
    
    for currency in basket_currencies:
        basket_weights[currency] = st.slider(f"Weight of {currency}:", 0, 100, 50)

    total_weight = sum(basket_weights.values())

    if total_weight > 100:
        st.error("Total weight exceeds 100%. Please adjust the weights.")
    else:
        st.success(f"Total weight: {total_weight}%")
        st.success(f"Total Basket Size: {basket_size}")

        if basket_currencies:
            st.write("Your custom basket is:")
            for currency, weight in basket_weights.items():
                st.write(f"- {currency}: {weight}%")

        st.write(f"Base Currency for the basket: {base_currency}")


elif selected == "Risk Factor":
    st.title("Risk Factor Analysis - Historic Volatility")

    currencies = exchange_rate_data.columns[1:]  # Get all available currencies
    currency_selected = st.selectbox("Select a Currency for HV Calculation:", currencies)

    date_selections = []
    year_selected = st.selectbox("Select Year for Volatility Analysis:", sorted(exchange_rate_data['Date'].dt.year.unique()))

    filtered_data = exchange_rate_data[exchange_rate_data['Date'].dt.year == year_selected]

    period_selected = st.selectbox("Select the Period:", ["monthly", "quarterly", "weekly"])

    # Calculating HV
    hv, returns = calculate_hv(filtered_data, currency_selected, period_selected)

    if hv is None or returns.empty:
        st.write(f"No sufficient data to calculate historical volatility for {currency_selected} in {year_selected}.")
    else:
        st.write(f"**Annualized Historical Volatility** for {currency_selected} in {year_selected} is: {hv:.2%}")

        # Plot returns only if available
        if not returns.empty:
            fig = px.line(
                x=returns.index,
                y=returns.values,
                title=f'Returns for {currency_selected} <br>            ({period_selected.capitalize()} data) in {year_selected}',
                labels={'x': 'Date', 'y': 'Returns'},
                markers=True
            )

            fig.update_layout(
                xaxis_title='Date',
                yaxis_title='Returns',
                title_x=0.5,  # Center the title
                showlegend=False,
                xaxis=dict(showgrid=True),  # Show gridlines on x-axis
                yaxis=dict(showgrid=True),  # Show gridlines on y-axis
                hovermode='x unified',  # Unified hover effect
            )

            st.plotly_chart(fig)


render_footer()