import streamlit as st
from src.screens.ui.base_layout import style_background_dashboard, style_base_layout
from src.screens.components.header import header_dashboard
from src.screens.components.footer import footer_dashboard

from src.screens.database.db import check_teacher_exist,create_teacher,teacher_login,get_teacher_subjects,get_attendance_for_teacher
from src.screens.components.dialog_create_subj import  create_subject_dialog
from src.screens.components.subject_card import subject_card
from src.screens.components.dialog_share_subject import share_subject_dialog
from src.screens.components.dialog_add_photo import add_photos_dialog

from src.screens.pipelines.face_pipeline import predict_attendance
import numpy as np
import pandas as pd
from datetime import datetime
from src.screens.database.config import supabase
from src.screens.components.dialog_attendance_result import attendance_result_dialog
from src.screens.components.dialog_voice_attendance import voice_attendance_dialog



def Teachers_screen():

    style_background_dashboard()             
    style_base_layout()
    
    if "teacher_data" in st.session_state:
            teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type== "login":
           teacher_screen_login()
    elif st.session_state.teacher_login_type== "register":
            teacher_screen_register() 
            
            
def teacher_dashboard():  
 
     teacher_data = st.session_state.teacher_data
     
     c1,c2 = st.columns(2, vertical_alignment= 'center', gap= 'xxlarge')
             
     with c1:
        header_dashboard()
     with c2:
        st.subheader(f"""welcome,{teacher_data['name']}""")
        if st.button("Logout", type= 'secondary', key= 'loginbackbutton',shortcut= 'control+backspace'):
            st.session_state['login_type']= None
            del st.session_state.teacher_data
            st.rerun()
            
     st.space() 
     
     if "current_teacher_tab" not in st.session_state:
         st.session_state.current_teacher_tab= 'take_attendance'
     
     tab1,tab2, tab3= st.columns(3)
     
     with tab1:
        type1="primary" if st.session_state.current_teacher_tab== 'take_attendance' else "tertiary"
        if st.button('Take Attendance',type=type1,width='stretch',icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab= 'take_attendance'
            st.rerun()
            
     with tab2:
        type2=  "primary" if st.session_state.current_teacher_tab== 'manage_subject' else "tertiary"
        if st.button('Manage Subject',type= type2, width='stretch', icon= ':material/book_ribbon:'):
            st.session_state.current_teacher_tab= 'manage_subject'
            st.rerun()
              
     with tab3:
        type3= "primary" if st.session_state.current_teacher_tab=='attendance_record' else "tertiary"
        if st.button('Attendance Record',type= type3,width= 'stretch',icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab= 'attendance_record'
            st.rerun()
            
     st.divider()
         
     if st.session_state.current_teacher_tab == "take_attendance":
         teacher_tab_take_attendance()
     if st.session_state.current_teacher_tab == "manage_subject":
         teacher_tab_manage_subject()
     if st.session_state.current_teacher_tab == "attendance_record":
         teacher_tab_attendance_record()
         
     footer_dashboard()
     
def teacher_tab_take_attendance():
    teacher_id= st.session_state.teacher_data['teacher_id']
    st.header('Take AI Attendance')
    
    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images= []
        
    subjects= get_teacher_subjects(teacher_id)
    
    if not subjects:
        st.warning("You haven't create any subjects yet! Please Create one to begin")
        return
    
    subject_options= {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}
    
    col1, col2 = st.columns([3,1], vertical_alignment='bottom') 
    
    with col1:
        selected_subject_label= st.selectbox('Select_Subject', options= list(subject_options.keys()))
        
    with col2:
       if st.button("Add Photos", icon= ':material/photo_prints:', width= 'stretch'):
          add_photos_dialog()
    # this is main id of subjects    
    selected_subject_id = subject_options[selected_subject_label] 
    
    st.divider() 
    
    if st.session_state.attendance_images:
        st.header('Added Photos')
        gallery_cols = st.columns(4)
        
        
        for idx,img  in enumerate(st.session_state.attendance_images):
            
            with gallery_cols[ idx % 4]:
                st.image(img, width= 'stretch', caption= f'Photo{idx+1}' )
    has_photos= bool(st.session_state.attendance_images)        
    c1,c2,c3 = st.columns(3)
    
    with c1:
       if st.button('Clear all photos',width='stretch', icon= ':material/delete:', type='tertiary'):
           st.session_state.attendance_images= []
           st.rerun()
           
    with c2:
        
        if st.button('Run Face Analysis', width='stretch', type='secondary', icon=':material/analytics:',disabled= not has_photos):
           with st.spinner("Deep scanning classroom Photos...."):
               all_detected_id= {}
               
               for idx,img in enumerate(st.session_state.attendance_images):
                # image ko numpy array main dalenge aur RGB main convert karenge taki easily process kar paye
                image_np= np.array(img.convert('RGB'))
                
                detected,_,_ = predict_attendance(image_np)
                
                if detected:
                   for sid in detected.keys():
                    student_id= int(sid)
                    
                    all_detected_id.setdefault(student_id, []).append(f'Photo{idx+1}') 
                    
                enroll_res= supabase.table('subjects_students').select("*, students(*)").eq('subject_id', selected_subject_id).execute()
                enrolled_students= enroll_res.data
                
                if not enrolled_students:
                    st.warning("No students enrolled in this course") 
                else:
                     results, attendance_to_logs= [],[]
                     
                     current_timestamp= datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                     
                     for node in enrolled_students: 
                         student= node['students']
                         sources= all_detected_id.get(int(student['student_id']), [])# fro multi sources we use [] student come twice in second image 
                         is_present= len(sources) > 0 # if photo more than 0 it means person present 
                         
                         results.append({
                             
                             "Name": student['name'],
                             "ID": student['student_id'],
                             "Source":",".join(sources) if  is_present else "-",
                             "Status": "✅Present" if is_present else "❌Absent"
                             
                           })
                         
                         attendance_to_logs.append({
                             'student_id': student['student_id'],
                             'subject_id': selected_subject_id,
                             'timestamp': current_timestamp,
                             'is_present': bool(is_present) 
                         })
# is dialog do chije denge wo results jo hume dikhane h pandas main dal denge taki easily wo table main dikha sake
                
                attendance_result_dialog(pd.DataFrame(results), attendance_to_logs)
    with c3:
        if st.button("Use voice attendance", width='stretch', icon=':material/mic:', type='primary'):
         voice_attendance_dialog(selected_subject_id)              
                                        
                
                
                
        
                          
    
    
def teacher_tab_manage_subject():
    teacher_id= st.session_state.teacher_data['teacher_id']
    c1,c2 = st.columns(2)
    
    with c1: 
     st.header('Manage subjects',width= 'stretch')
     
    with c2:
      if  st.button('Create New Subject', width='stretch'):
          create_subject_dialog(teacher_id)
          
# List all subjects
    subjects = get_teacher_subjects(teacher_id)
    if subjects:
     for sub in subjects:
        stats=[
            ("🫂:", "Students", sub['total_students']),
            ("🕰️:", "Classes", sub['total_classes'])  
        ]
     def share_btn():
        if st.button(f"Share code: {sub['name']}", key= f"share_{sub['subject_code']}", icon= ":material/share:"):
            share_subject_dialog(sub['name'], sub['subject_code'])   
            st.space()
        
     subject_card(
            name= sub['name'],
            code= sub['subject_code'],
            section= sub['section'],
            stats=stats,
            footer_callback=share_btn
        )
    else:
        st.info("NO SUBJECTS FOUND. CREATE ONE ABOVE") 
           
         
                  
         
def teacher_tab_attendance_record():
    st.header('Attendance Record') 
    
    teacher_id= st.session_state.teacher_data['teacher_id']
    
    records= get_attendance_for_teacher(teacher_id)
    
    if not records:
        return
    data= []
    
    for r in records:
      ts= r.get('timestamp')
      
      data.append({
          "its_group": ts.split(".")[0] if ts else None,
          "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N'A",
          "Subject":r['subjects']['name'],
          "Subject_code": r['subjects']['subject_code'],
          "is_present": bool(r.get('is_present', False))
        })
      # kitne total present h and kitni total classes h ye sari chije pandas main compute karenge isiliye isko hmne dataframe bana diya  
    df= pd.DataFrame(data)   
    
    
    
    
    summary= (
        # jb bhi groupby krte h to table ka structure kharab ho jata h usme new colms a jate h .reset_index() use hamare original formate main wapas le ata h
        df.groupby(['its_group','Time', 'Subject', 'Subject_code','is_present'])
        .agg(
            Present_count= ('is_present', 'sum'),
            Total_count= ('is_present', 'count'),
        ).reset_index()
    )
    
    summary ['Attendance stats']= (
        "✅"+ summary['Present_count'].astype(str) + " /"
        + summary['Total_count'].astype(str) + "Students"
        
    )
    
    display_df= ( summary.sort_values(groupby= 'its_group', ascending= False)
                 [['Time', "Subject", 'Subject_code', 'Attendance stats']]
                 
                 )
    
    st.dataframe(display_df, width='stretch', hide_index= True)
                     
              

       
def login_teacher(username,password): 
    if not username or not password:
        return False 
# ab database  wale ko yanha se call karenge
#thodi statement dalni hogi tbi identify kar payenge teacher ko
  
    teacher = teacher_login(username, password)
    
    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
        
        
    return False
    
      
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
     if st.button("Login", icon=':material/passkey:', shortcut='control+enter', width= 'stretch'):
        #if teacher_login(teacher_username,teacher_pass):
        if login_teacher(teacher_username,teacher_pass):
            st.toast("Welcome back!", icon="🖐️")
            import time
            time.sleep(1)
            st.rerun()
        else:
            st.error("Invalid Username! or password")
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
       create_teacher(teacher_username,teacher_name,teacher_pass)
       return True,"Sucessfully created! Login now"
    except Exception as e:
        return False,str(e)
    
    
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
           success, message = register_teacher(teacher_username,teacher_name, teacher_pass, confirm_pass)
           
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
    