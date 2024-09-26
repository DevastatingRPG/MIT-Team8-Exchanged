# fx_rate.py
import streamlit as st
import plotly.express as px
from utils import fx
import datetime

def get_user_inputs() -> tuple[str, datetime.date]:
    """
    Get user inputs for base currency and date.

    Returns:
        tuple: A tuple containing the selected base currency (str) and the selected date (datetime.date).
    """
    col1, col2 = st.columns(2)

    with col1:
        currencies_list = fx.get_currencies_list()
        base_currency = st.selectbox("Select Base Currency:", currencies_list, index=currencies_list.index("USD"))

    with col2:
        selected_date = st.date_input("Select Date", value=datetime.date.today(), max_value=datetime.date.today())

    return base_currency, selected_date

def fetch_and_display_rates(base_currency: str, selected_date: datetime.date):
    """
    Fetch and display the exchange rates based on user inputs.

    Args:
        base_currency (str): The base currency for the exchange rates.
        selected_date (datetime.date): The date for which to fetch the exchange rates.
    """
    rates, _ = fx.get_fx_rates(base_currency=base_currency, date=selected_date.strftime('%Y-%m-%d'))
    st.dataframe(rates, use_container_width=True)

    fig = px.bar(rates, x='Rate', y='Currency', title=f'Currency Exchange Rates (Base: {base_currency})', labels={'Rate': 'Exchange Rate'}, height=800)
    
    fig.update_layout(
        yaxis=dict(
            range=[0, 10],
            autorange=False
        ),
        xaxis=dict(
            fixedrange=True
        ),
        dragmode='pan',
        height=800
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_fx_rate():
    """
    Main function to show FX Rate page.
    """
    st.title("FX Rate")

    base_currency, selected_date = get_user_inputs()
    if st.button("Fetch Rates"):
        fetch_and_display_rates(base_currency, selected_date)

