import streamlit as st
from src.screens.database.config import supabase
from src.screens.database.db import create_attendance


def show_attendance_results(df,logs):
    st.write('Please review attendance before confirming.')
    st.dataframe(df,hide_index=True, width='stretch')
    col1, col2= st.columns(2)
        
    with col1:
           if st.button('Discard',width='stretch'):
             st.session_state.voice_attendance_results= None
             st.session_state.attendance_images= [] 
             st.rerun()
            
    with col2:
           if  st.button('Confirm & Save', width='stretch',type='primary'):
               #agar database query fail hoti h to
               try:
                   # isme sari attendance bhej denge
                   create_attendance(logs)
                   st.toast("Attendance Taken")
                   #jo stakes the jisme images rkhi thi attendance images khali kar denge 
                   st.session_state.attendance_images= []
                   st.session_state.voice_attendance_results= None 
                   st.rerun()
               except Exception as e:
                    st.error("sync failed!")
                    
     
@st.dialog("Attendance Results")                
def attendance_result_dialog(df,logs):
     show_attendance_results(df,logs)

            
              
                        