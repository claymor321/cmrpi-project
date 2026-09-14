
import streamlit as st
from datetime import date
from core.validation import email_valide

def afficher_identification():
    st.markdown("""
    <style>
    [data-testid="stForm"] {
        background-color: #14294A;
        padding: 30px;
        border-radius: 16px;
        border: 1px solid #3d3d4d;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    [data-testid="stForm"] * {
        color: #ffffff !important;
    }
    [data-testid="stForm"] input {
        background-color: #1e1e2e !important;
        border-radius: 8px !important;
        border: 1px solid #3d3d4d !important;
    }
    div[data-testid="stFormSubmitButton"] button {
        background-color: #6C63FF;
        color: white !important;
        border-radius: 10px;
        width: 100%;
        font-weight: 600;
        padding: 10px 0;
        border: none;
        margin-top: 10px;
    }
    div[data-testid="stFormSubmitButton"] button:hover {
        background-color: #574fd6;
    }
    </style>
    """, unsafe_allow_html=True)
    st.subheader("Identification de l'entreprise")
    with st.form("form_identification"):
        nom = st.text_input("Nom de l'entreprise")
        secteur = st.text_input("Secteur d'activité")
        taille = "PME"
        email = st.text_input("Email de contact")
        submit = st.form_submit_button("Valider ➜")
    st.markdown(
        """
        <style>
        div[data-testid="stFormSubmitButton"] button {
            background: linear-gradient(135deg, #d9a441, #b3812f);
            color: #1c1408;
            font-weight: 700;
            border: none;
            border-radius: 8px;
            padding: 10px 22px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.35);
            transition: transform 0.08s ease, filter 0.15s ease;
        }
        div[data-testid="stFormSubmitButton"] button:hover {
            filter: brightness(1.1);
        }
        div[data-testid="stFormSubmitButton"] button:active {
            transform: translateY(1px);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    if submit:
        if not nom.strip():
            st.error("Merci de renseigner le nom de l'entreprise.")
        elif not secteur.strip():
            st.error("Merci de renseigner le secteur d'activité.")
        elif not email_valide(email):
            st.error("Merci de renseigner un email valide.")
        else:
            st.session_state.entreprise = {
                "nom": nom.strip(),
                "secteur": secteur.strip(),
                "taille": taille,
                "email_contact": email.strip(),
                "date_audit": date.today().isoformat(),
            }
            st.rerun()