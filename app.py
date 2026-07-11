import streamlit as st

from src.screens.Teachers_screen import Teachers_screen
from src.screens.Student_screen import Student_screen
from src.screens.Home_screen import Home_screen
def main():
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None
        
    match st.session_state['login_type']:
        case 'Teachers':
         Teachers_screen()
        case 'Students':
         Student_screen()
        case None:
         Home_screen()
                
main()
