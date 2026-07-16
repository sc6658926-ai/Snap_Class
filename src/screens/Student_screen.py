import streamlit as st

from src.screens.ui.base_layout import style_background_dashboard, style_base_layout
from src.screens.components.header import header_dashboard
from src.screens.components.footer import footer_dashboard
 
def Student_screen():
    
    style_background_dashboard()
    style_base_layout()
 
    c1,c2 = st.columns(2, vertical_alignment= 'center', gap= 'xxlarge')
            
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type= 'secondary', key= 'loginbackbutton',shortcut= 'control+backspace'):
            st.session_state['login_type']= None
            st.rerun()
            
    st.header("Login using FACE_ID", text_alignment= 'center')
    st.space()
    st.space()
            
    st.camera_input("Position your face in the center")
            
    footer_dashboard()