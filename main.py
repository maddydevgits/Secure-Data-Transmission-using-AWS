import app1
import streamlit as st
import app2

PAGES = {
    "Secure Data Transmission": app1,
    "Receiver Side": app2
}

st.sidebar.title('Dashboard')
selection=st.sidebar.radio("Go to",list(PAGES.keys()))
page=PAGES[selection]
page.app()