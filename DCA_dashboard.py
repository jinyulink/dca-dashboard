import streamlit as st
import pandas as pd
import numpy as np
from essential import displayEssential

st.set_page_config(page_title="DCA Dashboard", page_icon="📈", layout="wide")
st.title('DCA Dashboard')
displayEssential()
st.markdown('''
    DCA dashboard is a tool to help you track your investment performance.
    This dashboard is powered by Streamlit.
''')


col1, col2, col3 = st.columns(3)
col1.metric("Total Invested", "$27,300", "1.2 °F")
col2.metric("Gross Earnings", "$11,300", "62%")
col3.metric("Humidity", "86%", "4%")

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["BTC", "S&P 500", "Gold"])

st.line_chart(chart_data)
