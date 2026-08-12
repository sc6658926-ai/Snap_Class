import streamlit as st

from src.screens.Teachers_screen import Teachers_screen
from src.screens.Student_screen import Student_screen
from src.screens.Home_screen import Home_screen
from src.screens.components.dialog_auto_enroll import auto_enroll_dialog

def main():
    st.set_page_config(
        page_title= 'SnapClass- Making Attendance faster using AI',
        page_icon='https://media.licdn.com/dms/image/v2/C4D12AQGMQqI0E9Cw7g/article-cover_image-shrink_720_1280/article-cover_image-shrink_720_1280/0/1520204388026?e=2147483647&v=beta&t=YQGbmT7i56gXsiE8IXyb4jXZnvBXbUGuGfioOXLRIVU'
    )
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None
        
    match st.session_state['login_type']:
        case 'Teachers':
         Teachers_screen()
        case 'Students':
         Student_screen()
        case None:
         Home_screen()
         
    join_code= st.query_params.get('join_code')
     
    if join_code:
       if st.session_state.get('login_type') != 'Students':
           st.session_state['login_type']= 'Students'
           st.rerun()
       if st.session_state.get('is_logged_in') and st.session_state.get('user_role')=='student':
           auto_enroll_dialog(join_code)       
                
main()



