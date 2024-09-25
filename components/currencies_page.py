# currencies.py
import streamlit as st
import plotly.express as px
from utils import fx

def show_currencies():
    """
    Main function to show the Currencies page.
    """
    if st.button("Fetch Rates"):
        rates = fx.get_currencies_fx()
        st.dataframe(rates, use_container_width=True)

        fig = px.bar(rates, x='Rate', y='Currency', title='Currency Exchange Rates', labels={'Rate': 'Exchange Rate'}, height=800)
        
        fig.update_layout(
            yaxis=dict(
                range=[0, 10],  
                autorange=False
            ),
            dragmode='pan' 
        )
        
        st.plotly_chart(fig, use_container_width=True)