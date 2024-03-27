import streamlit as st
import pandas as pd
import numpy as np
from config import asset_map, time_map
from essential import displayEssential
from fetchPrice import fetchPrice

st.set_page_config(page_title="DCA Dashboard", page_icon="📈", layout="wide")
st.title('DCA Dashboard')
displayEssential()
st.markdown('''
    DCA dashboard is a tool to help you track your investment performance.
    This dashboard is powered by Streamlit.
''')

with st.sidebar:
    st.title('Settings')
    asset = st.selectbox(
    'Select Purchase Asset',
    list(asset_map.keys()))  # Use the keys of the asset_map as options
    amount = st.number_input('Purchase Amount ($U.S. dollar)')
    frequency = st.selectbox(
    'Purchase Frequency',
    ('Weekly', 'Every 2 weeks', 'Monthly', 'Annually'))
    startFrom = st.selectbox(
    'Start From',
    list(time_map.keys()))
    compareWith = st.multiselect(
    'Compare with other assets?',
    [a for a in asset_map.keys() if a != asset],
    [])
    calculateBtn = st.button("Calculate", type="primary")
    
if calculateBtn:
    asset_data = fetchPrice(asset_map[asset], time_map[startFrom])
    
    if frequency == 'Weekly':
        purchase_dates = pd.date_range(start=asset_data.index[0], end=asset_data.index[-1], freq='W')
    elif frequency == 'Every 2 weeks':
        purchase_dates = pd.date_range(start=asset_data.index[0], end=asset_data.index[-1], freq='2W')
    elif frequency == 'Monthly':
        purchase_dates = pd.date_range(start=asset_data.index[0], end=asset_data.index[-1], freq='M')
    elif frequency == 'Annually':
        purchase_dates = pd.date_range(start=asset_data.index[0], end=asset_data.index[-1], freq='A')
    
    adjusted_purchase_dates = []
    for date in purchase_dates:
        while date not in asset_data.index and date <= asset_data.index[-1]:
            date += pd.Timedelta(days=1)
        if date in asset_data.index:
            adjusted_purchase_dates.append(date)
    purchase_dates = adjusted_purchase_dates
    
    total_purchase_amount = np.cumsum([amount / asset_data.loc[date, 'Close'] for date in purchase_dates]) # Amount of BTC purchased
    total_asset_value = total_purchase_amount * asset_data.loc[purchase_dates, 'Close']
    net_profit = total_asset_value - np.cumsum([amount for _ in purchase_dates])
    
    total_invested = round(amount * len(purchase_dates), 4)
    total_value = round(total_asset_value[-1], 4)
    total_profit = round(net_profit[-1], 4)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Invested", '$' + str(total_invested))
    col2.metric("Total Value", '$' + str(total_value), str(round(total_value / total_invested - 1, 4) * 100) + '%')
    col3.metric("Net Profit", '$' + str(total_profit))

    data = pd.DataFrame({
        'Total Value': total_asset_value,
        'Net Profit': net_profit
    }, index=purchase_dates)
    
    st.line_chart(data)