
import streamlit as st
from datetime import date
from core.validation import email_valide

def afficher_identification():
    st.subheader("Identification de l'entreprise")
    with st.form("form_identification"):
        nom = st.text_input("Nom de l'entreprise")
        secteur = st.text_input("Secteur d'activité")
        taille = "PME"
        email = st.text_input("Email de contact")
        submit = st.form_submit_button("Valider ➜")

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