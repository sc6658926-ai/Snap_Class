import streamlit as st
import segno
import io

@st.dialog("share class link")
def share_subject_dialog(subject_name, subject_code):
    app_domain="snapclass-main.streamlit.app"
    join_url= f"{app_domain}/?join_code={subject_code}"
    
    st.header("scan to join")
     
    qr= segno.make(join_url)
    
    out = io.BytesIO()
    qr.save(out, kind= 'png', border=1, scale=10)
    
    c1,c2= st.columns(2)
    
    with c1:
        st.markdown('### copy link')
        st.code(join_url, language= "text")
        st.code(subject_code, language="text")
        st.info("copy this link to share on whatsapp or Email")
        
    with c2:
        st.markdown('### scan to join')
        st.image(out.getvalue(), caption='QR_CODE for class joining')   