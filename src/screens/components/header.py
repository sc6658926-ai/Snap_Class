from pathlib import Path
import streamlit as st
import base64

def header_home():

    logo_path = Path("static") / "img" / "logo.png"

    logo_base64 = base64.b64encode(
        logo_path.read_bytes()
    ).decode()

    st.markdown(f"""
    <div style="
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-top: 20px;
    ">
        <img
            src="data:image/png;base64,{logo_base64}"
            style="
                width: 120px;
                height: 120px;
                object-fit: contain;
                display: block;
            "
        >
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h1 style="
        text-align: center;
        color: #E0E3FF;
        margin-top: 10px;
    ">
        SNAP<br>CLASS
    </h1>
    """, unsafe_allow_html=True)
  
def header_dashboard():
    
  logo_path = Path("static") / "img" / "logo.png"
  logo_base64 = base64.b64encode(
          logo_path.read_bytes()
      ).decode()

  st.markdown(f"""
    <div style= "display:flex; align-items:center; justify-content:left;gap: 10px;">
    <img src='data:image/png;base64,{logo_base64}' style='height:80px;'/> 
    </div>
              
      """, unsafe_allow_html= True)
  
