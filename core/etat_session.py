import streamlit as st

def reset():
    st.session_state.etape = "identification"
    st.session_state.entreprise = {}
    st.session_state.profil = [1, 1, 1, 1, 1]
