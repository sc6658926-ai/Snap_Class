import streamlit as st

def header_home():

  logo_url = "https://media.licdn.com/dms/image/v2/C4D12AQGMQqI0E9Cw7g/article-cover_image-shrink_720_1280/article-cover_image-shrink_720_1280/0/1520204388026?e=2147483647&v=beta&t=YQGbmT7i56gXsiE8IXyb4jXZnvBXbUGuGfioOXLRIVU"
  
  st.markdown(f"""
    <div style= "display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bttom: 100px; margin-top: 30px;">
        <img src = '{logo_url}' style='height: 100px;'/>
        <h1 style =text-align:center; color:#E0E3FF> SNAP</br> CLASS</h1>
    </div>
              
      """, unsafe_allow_html= True)
  
  
def header_dashboad():
    
  logo_url = "https://media.licdn.com/dms/image/v2/C4D12AQGMQqI0E9Cw7g/article-cover_image-shrink_720_1280/article-cover_image-shrink_720_1280/0/1520204388026?e=2147483647&v=beta&t=YQGbmT7i56gXsiE8IXyb4jXZnvBXbUGuGfioOXLRIVU"
  
  st.markdown(f"""
    <div style= "display:flex; align-items:center; justify-content:center;gap: 10px; margin-top: 30px;">
        <img src = '{logo_url}' style='height: 80px;'/>
        <h2 style =text-align:center; color:#5865F2> SNAP</br> CLASS</h1>
    </div>
              
      """, unsafe_allow_html= True)
  
