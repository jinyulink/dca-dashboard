import streamlit as st
from essential import displayEssential

st.set_page_config(page_title="Info", page_icon="📊", layout="wide")
st.title('Info')
st.markdown('''
        #### DCA dashboard is a tool to help you track your investment performance of Dollar Cost Averaging (DCA).
        This website is my final project for a Python programming course. 
        
        The main purpose of creating this site is to help me calculate which asset's return on investment will be the highest through dollar-cost averaging (DCA). 
        
        Python is well-suited for chart plotting and visualization, and upon discovering Streamlit, a convenient web framework for data presentation, I decided to utilize this framework as the interface for displaying charts.
        
        ###### This dashboard is create by Jinlk and powered by Streamlit.
    ''')
displayEssential()