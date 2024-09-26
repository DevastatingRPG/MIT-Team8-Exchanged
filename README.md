# NorthernProject

#Currency Exchange Rate Dashboard Project Description

#This project is a dashboard for analyzing currency exchange rates using Python and Plotly Dash. It allows users to select time periods, display trends, and manage custom currency baskets. The dashboard can visualize historical data, making it easier to understand currency fluctuations over time.
#Features:

    Data Visualization: View exchange rates in weekly, monthly, quarterly, and annual charts.
    Peak and Low Rate Display: Easily identify the dates and values of the highest and lowest exchange rates.
    Custom Currency Baskets: Create and manage currency baskets with user-defined weights, calculating the aggregate value against a base currency.
    Risk Indicator: Monitor the volatility of selected currency pairs with a visual risk indicator.
    Information on Currency: View all currencies along with a short code, description, and current exchange rate against USD.
    Automated: Database is automatically updated with exchange rates.

#Setup Instructions

    Clone the repository:
        git clone <repository-url>
        cd currency-exchange-dashboard

    Set up a virtual environment (optional but recommended):
        For Python 3.x:
            python -m venv env
            source env/bin/activate (On Windows use env\Scripts\activate)

    Install required packages:
        pip install -r requirements.txt

    Create a .env file and add your API key:
        API_KEY=your_api_key_here

    Run the application:
        streamlit run app.py 
