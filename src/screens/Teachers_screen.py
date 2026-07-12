import streamlit as st
from src.screens.ui.base_layout import style_background_dashboard, style_base_layout
from src.screens.components.header import header_dashboard
from src.screens.components.footer import footer_dashboard

def Teachers_screen():

    style_background_dashboard()             
    style_base_layout()
    
    c1,c2 = st.button(2, vertical_alignment= 'center', gap= 'xxlarge')
        
    with c1:
        header_dashboard()
    with c2:
        st.button("Go back to Home", type= 'secondary', shortcut= 'control+backspace')
        
    st.header("Login using password", text_alignment= 'center')
    st.space()
    
    footer_dashboard()    
    