import streamlit as st
from streamlit_extras.app_logo import add_logo

def displayEssential():
    footer='''
        <div class="footer" style="position: fixed; bottom: 10px; width: 100%; left: 0px; text-align: center;">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
            <center>
                <a href="https://github.com/jinyulink" style="color: inherit;"><div><i class="fa fa-github" style="font-size:20px"></i></div></a>
                <div style="font-size: 12px;"><a href="https://blog.jinlk.dev/" style="color: inherit; text-decoration: none;">Copyright © 2024 Jim</a></div>
                <div style="font-size: 12px;">DCA Dashboard | Made in Streamlit</div>
            </center>
        </div>
        '''
        # &nbsp<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="10">
    st.markdown(footer,unsafe_allow_html=True)
    add_logo("https://blog.jinlk.dev/images/avatar.png") # https://discuss.streamlit.io/t/streamlit-sidebar-logo/49735/4