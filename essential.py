import streamlit as st

def displayEssential():
    footer='''
        <div class="footer" style="position: fixed; bottom: 10px; width: 100%; left: 0px; text-align: center;">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
            <center>
                <a href="https://github.com/jinyulink" style="color: inherit;"><div><i class="fa fa-github" style="font-size:24px"></i></div></a>
                <div style="font-size: 14px;"><a href="https://blog.jinlk.dev/" style="color: inherit; text-decoration: none;">Copyright © 2024 Jim</a></div>
                <div style="font-size: 14px;">DCA Dashboard | Powered by Streamlit</div>
            </center>
        </div>
        '''
    st.markdown(footer,unsafe_allow_html=True)