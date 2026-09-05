import streamlit as st

def identification_complete():
    entreprise = st.session_state.get("entreprise", {})
    return bool(entreprise.get("nom"))

def reset():
    st.session_state.etape = "questionnaire"
    st.session_state.entreprise = {}
    st.session_state.profil = [1, 1, 1, 1, 1]
