import streamlit as st
from src.screens.ui.base_layout import style_background_dashboard, style_base_layout
from src.screens.components.header import header_dashboard
from src.screens.components.footer import footer_dashboard

from src.screens.database.db import check_teacher_exist,create_teacher,teacher_login

def Teachers_screen():

        style_background_dashboard()             
        style_base_layout()
    
        
        if 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type== "login":
           teacher_screen_login()
        elif st.session_state.teacher_login_type== "register":
            teacher_screen_register() 
            
    
    
def teacher_screen_login():       
    c1,c2 = st.columns(2, vertical_alignment= 'center', gap= 'xxlarge')
        
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type= 'secondary', key= 'loginbackbutton',shortcut= 'control+backspace'):
            st.session_state['login_type']= None
            st.rerun()
            
    st.header("Login using password", text_alignment= 'center')
    st.space()
        
    teacher_username = st.text_input("Enter username", placeholder= '@shiva123')
        
    teacher_pass = st.text_input("Enter password", type= 'password', placeholder='Enter password')
        
    st.divider()
    
    btnc1, btnc2= st.columns(2)
    
    with btnc1:
        st.button("Login", icon=':material/passkey:', shortcut='control+enter', width= 'stretch')
        if teacher_login(teacher_username,teacher_pass):
            st.toast("Welcome back!", icon="🖐️")
            import time
            st.time(1)
            st.rerun()
        else:
            st.error("Invalid Username or Password")
    with btnc2:
     if st.button("Register Instead", icon= ':material/passkey:',shortcut='control+k', width= 'stretch', type='primary'):
        st.session_state.teacher_login_type= 'register'
        
    
    footer_dashboard()
    
def register_teacher(teacher_username,teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_pass or not teacher_name or not teacher_username:
        return False, "All feilds are required!"
    
    if check_teacher_exist(teacher_username):
        return False, "Username already exist"
    if teacher_pass != teacher_pass_confirm:
        return False, "Password doesn't match"
    
    try:
       create_teacher(teacher_name,teacher_username,teacher_pass)
       return True,"Sucessfully created! Login now"
    except Exception as e:
        return False, "Unexpected Error!"
    
    
def teacher_screen_register():   
    c1,c2 = st.columns(2, vertical_alignment= 'center', gap= 'xxlarge')
        
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type= 'secondary', key= 'loginbackbutton',shortcut= 'control+backspace'):
            st.session_state['login_type']= None
            st.rerun()
            
    st.header("Register your teacher profile", text_alignment= 'center')
    
    st.space()
    st.space()
        
    teacher_username = st.text_input("Enter username", placeholder= '@shiva123')
    teacher_name = st.text_input("Enter name", placeholder= 'Shiva Chauhan')
        
    teacher_pass = st.text_input("Enter password", type= 'password', placeholder='Enter your password')
    confirm_pass= st.text_input("Confirm password", type='password', placeholder= 'confirm your password')
        
    st.divider()
    
    btnc1, btnc2= st.columns(2)
    
    with btnc1:
       if st.button("Register Now", icon=':material/passkey:', shortcut='control+enter', width= 'stretch', type='primary'):
           success, message = register_teacher(teacher_username,teacher_name, teacher_pass,teacher_pass_confirm)
           
           if success:
                st.success(message)
                import time
                time.sleep(2)
                
                st.session_state.teacher_login_type= "login"
                st.rerun()
           else:
                st.error(message)
        
    with btnc2:
        if st.button("Login Instead", icon= ':material/passkey:',shortcut='control+k', width= 'stretch'):
            st.session_state.teacher_login_type= 'login' 
    
    footer_dashboard()
    