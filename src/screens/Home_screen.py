import streamlit as st
from src.screens.components.header import header_home
from src.screens.ui.base_layout import style_background_home, style_base_layout
from src.screens.components.footer import footer_home


def Home_screen():
    st.header('')
    
    header_home()
    style_base_layout()
    style_background_home()

    
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.header("I'm student")
        st.image("https://i.pinimg.com/1200x/85/49/0f/85490f3eb7408f88b97bc98c229e65e9.jpg", width= 120)
        if st.button('Student_portal', type= 'primary', icon= ':material/arrow_outward:', icon_position= 'right'):
            st.session_state['login_type'] = 'Students'
            st.rerun()
            
    with col2:
        st.header("I'm teacher")
        st.image("https://i.pinimg.com/736x/00/75/92/0075928b52ae2130d04b471ccf2608fd.jpg", width= 120)
        if st.button('Teachers_portal',type= 'primary', icon=':material/arrow_outward:', icon_position= 'right'):
            st.session_state['login_type'] ='Teachers'
            st.rerun()
            
    footer_home()
            
            
   
            
    
            
         