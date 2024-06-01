import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
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
            all_dates = pd.date_range(start=asset_data.index[0], end=asset_data.index[-1], freq='D')

            if self.frequency == 'Weekly':
                purchase_dates = pd.date_range(start=asset_data.index[0], end=asset_data.index[-1], freq='W')
            elif self.frequency == 'Every 2 weeks':
                purchase_dates = pd.date_range(start=asset_data.index[0], end=asset_data.index[-1], freq='2W')
            elif self.frequency == 'Monthly':
                purchase_dates = pd.date_range(start=asset_data.index[0], end=asset_data.index[-1], freq='M')
            elif self.frequency == 'Annually':
                purchase_dates = pd.date_range(start=asset_data.index[0], end=asset_data.index[-1], freq='A')

            total_purchase_amount = 0
            total_invest_usd = 0
            total_invest_value = np.zeros(len(all_dates))
            total_asset_value = np.zeros(len(all_dates))
            net_profit = np.zeros(len(all_dates))

            for i, date in enumerate(all_dates):
                d = date
                while d not in asset_data.index:
                    d -= pd.Timedelta(days=1)
                price = asset_data.loc[d, 'Close']
                if date in purchase_dates:
                    total_purchase_amount += self.amount / price
                    total_invest_usd += self.amount

                total_asset_value[i] = total_purchase_amount * price
                net_profit[i] = total_asset_value[i] - total_invest_usd
                total_invest_value[i] = total_invest_usd

            st.markdown(f"""
                #### Starting from **{self.startFrom}**, investing **${self.amount}** on a **{self.frequency}** basis in **{self.asset}** :
            """)

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Invested", '$' + str(total_invest_usd))
            col2.metric("Total Value", '${:.4f}'.format(total_asset_value[-1]), '{:.4f}%'.format((total_asset_value[-1] / total_invest_usd - 1) * 100))
            col3.metric("Net Profit", '${:.4f}'.format(net_profit[-1]))

            chart_data = pd.DataFrame({
                self.asset: total_asset_value,
                'Total Invested': total_invest_value
            }, index=all_dates)

            # Display return rates for the selected asset
            return_rates = {self.asset: ((total_asset_value[-1] / total_invest_usd - 1) * 100)}

            if len(self.compareWith) > 0:
                for i in self.compareWith:
                    compare_asset_data = fetchPrice(asset_map[i], time_map[self.startFrom])
                    compare_asset_value = np.zeros(len(all_dates))
                    compare_total_invest_usd = 0
                    compare_total_purchase_amount = 0
                    for j, date in enumerate(all_dates):
                        dd = date
                        while dd not in compare_asset_data.index:
                            dd -= pd.Timedelta(days=1)
                        price = compare_asset_data.loc[dd, 'Close']
                        if date in purchase_dates:
                            compare_total_purchase_amount += self.amount / price
                            compare_total_invest_usd += self.amount
                        compare_asset_value[j] = compare_total_purchase_amount * price

                    chart_data[i] = compare_asset_value
                    return_rates[i] = ((compare_asset_value[-1] / compare_total_invest_usd - 1) * 100)

            # Create a DataFrame for the return rates and sort by return rates in descending order
            return_rates_df = pd.DataFrame.from_dict(return_rates, orient='index', columns=['Return Rate'])
            return_rates_df.reset_index(inplace=True)
            return_rates_df.rename(columns={'index': 'Asset'}, inplace=True)
            return_rates_df = return_rates_df.sort_values(by='Return Rate', ascending=False)
            return_rates_df['Return Rate'] = return_rates_df['Return Rate'].apply(lambda x: f'{x:.2f}%')

            # Use Plotly to create a bar chart with percentage labels
            fig = px.bar(return_rates_df, x='Asset', y='Return Rate', text='Return Rate')
            fig.update_traces(texttemplate='%{text}', textposition='outside')
            fig.update_layout(title='Return Rates of Different Assets', yaxis_title='Return Rate (%)')

            st.line_chart(chart_data.iloc[:-1])
            
            st.plotly_chart(fig)

    def display(self):
        st.set_page_config(page_title="DCA Dashboard", page_icon="📈", layout="wide")
        st.title('DCA Dashboard')
        displayEssential()
        self.display_settings()
        self.calculate()

if __name__ == '__main__':
    dashboard = DCADashboard(asset_map, time_map).display()
