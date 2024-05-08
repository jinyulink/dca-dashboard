import streamlit as st
import pandas as pd
import numpy as np
from config import asset_map, time_map
from essential import displayEssential
from fetchPrice import fetchPrice

class DCADashboard:
    def __init__(self, asset_map, time_map):
        self.asset_map = asset_map
        self.time_map = time_map
        self.asset = None
        self.amount = None
        self.frequency = None
        self.startFrom = None
        self.compareWith = None
        self.calculateBtn = None

    def display_settings(self):
        with st.sidebar:
            st.title('Settings')
            self.asset = st.selectbox(
            'Select Purchase Asset',
            list(self.asset_map.keys()))  # Use the keys of the asset_map as options
            self.amount = st.number_input('Purchase Amount ($U.S. dollar)')
            self.frequency = st.selectbox(
            'Purchase Frequency',
            ('Weekly', 'Every 2 weeks', 'Monthly', 'Annually'))
            self.startFrom = st.selectbox(
            'Start From',
            list(self.time_map.keys()))
            self.compareWith = st.multiselect(
            'Compare with other assets?',
            [a for a in self.asset_map.keys() if a != self.asset],
            [])
            self.calculateBtn = st.button("Calculate", type="primary")

    def calculate(self):
        if self.calculateBtn:
            asset_data = fetchPrice(asset_map[self.asset], time_map[self.startFrom])
            
            if self.frequency == 'Weekly':
                purchase_dates = pd.date_range(start=asset_data.index[0], end=asset_data.index[-1], freq='W')
            elif self.frequency == 'Every 2 weeks':
                purchase_dates = pd.date_range(start=asset_data.index[0], end=asset_data.index[-1], freq='2W')
            elif self.frequency == 'Monthly':
                purchase_dates = pd.date_range(start=asset_data.index[0], end=asset_data.index[-1], freq='M')
            elif self.frequency == 'Annually':
                purchase_dates = pd.date_range(start=asset_data.index[0], end=asset_data.index[-1], freq='A')
            
            adjusted_purchase_dates = []
            for date in purchase_dates:
                while date not in asset_data.index and date <= asset_data.index[-1]:
                    date += pd.Timedelta(days=1)
                if date in asset_data.index:
                    adjusted_purchase_dates.append(date)
            purchase_dates = adjusted_purchase_dates
            
            total_purchase_amount = np.cumsum([self.amount / asset_data.loc[date, 'Close'] for date in purchase_dates]) # Amount of BTC purchased
            total_invest_usd = np.cumsum([self.amount for _ in purchase_dates]) # Total amount of USD invested
            total_asset_value = total_purchase_amount * asset_data.loc[purchase_dates, 'Close']
            # total_asset_value = []
            # for date in asset_data.index:
            #     asset_value = np.sum([self.amount / asset_data.loc[date, 'Close'] if date >= d else 0 for d in purchase_dates]) * asset_data.loc[date, 'Close']
            #     total_asset_value.append(asset_value)
            net_profit = total_asset_value - np.cumsum([self.amount for _ in purchase_dates])
            
            total_invested = round(self.amount * len(purchase_dates), 4)
            total_value = round(total_asset_value[-1], 4)
            total_profit = round(net_profit[-1], 4)

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Invested", '$' + str(total_invested))
            col2.metric("Total Value", '$' + str(total_value), str(round(total_value / total_invested - 1, 4) * 100) + '%')
            col3.metric("Net Profit", '$' + str(total_profit))

            data = pd.DataFrame({
                'Total Invested': total_invest_usd, 
                'Total Value': total_asset_value,
            }, index=purchase_dates)
            
            st.line_chart(data)

    def display(self):
        st.set_page_config(page_title="DCA Dashboard", page_icon="📈", layout="wide")
        st.title('DCA Dashboard')
        displayEssential()
        st.markdown('''
            DCA dashboard is a tool to help you track your investment performance.
            This dashboard is powered by Streamlit.
        ''')
        self.display_settings()
        self.calculate()

if __name__ == '__main__':
    dashboard = DCADashboard(asset_map, time_map).display()
        