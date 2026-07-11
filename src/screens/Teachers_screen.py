import streamlit as st
from src.screens.ui.base_layout import style_backround_dashboard, style_base_layout
from src.screens.components.header import header_dashboad
from src.screens.components.footer import footer_dashboard

def Teachers_screen():
    
 style_backround_dashboard()
 
 style_base_layout()
 
 teacher_screen_login()
 
 
def teacher_screen_login():
    c1,c2 = st.columns(2, vertical_alignment= 'center', gap= 'large')
    
    with c1:
        header_dashboad()
        
    with c2:
        st.button ("Go back to Home", type= 'secondary', shortcut= 'control+backspace')
        
    st.header("Login using password", text_alignment='center')
    st.space()
    teacher_username= st.text_input("Enter username", placeholder= '@shiva123')
    teacher_pass= st.text_input("Enter password", type= 'password', placeholder='Enter password')
        
    st.divider()
    
    footer_dashboard()

def teacher_screen_register():
    c1,c2= st.columns(2, vertical_alignment= 'center', gap= 'xxlarge') 
    
    with c1:
        st.button('Go back to Home', key= 'loginbackbutton', type='secondary', shortcut= 'control+backspace')
    st.header('register ')

         