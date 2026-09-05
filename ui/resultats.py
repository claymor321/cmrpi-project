import streamlit as st
from pdf.generer_rapport import generer_pdf_bytes
from core.etat_session import reset
from data.questionnaire import lesquestions,lesreponses
from pdf.style_pdf import STYLE_PRIORITE
from core.moteur_recommandation import moteur_recommandations

def afficher_resultats():
    entreprise = st.session_state.entreprise
    profil = st.session_state.profil

    st.subheader("3. Rapport d'audit")
    st.markdown(
        f"""
        **Entreprise :** {entreprise['nom']}
        **Secteur :** {entreprise['secteur']} &nbsp;|&nbsp; **Taille :** {entreprise['taille']}
        **Contact :** {entreprise['email_contact']}
        **Date de l'audit :** {entreprise['date_audit']}
        """
    )
    st.divider()

    recos = moteur_recommandations(profil)

    # Indicateurs synthétiques
    nb_critique = sum(1 for r in recos if r["priorite"] == "Critique")
    nb_elevee = sum(1 for r in recos if r["priorite"] == "Elevee")
    nb_moyenne = sum(1 for r in recos if r["priorite"] == "Moyenne")

    col1, col2, col3 = st.columns(3)
    col1.metric("🔴 Critique", nb_critique)
    col2.metric("🟠 Elevée", nb_elevee)
    col3.metric("🟡 Moyenne", nb_moyenne)

    st.divider()

    # Regrouper par question pour l'affichage
    for num_q in range(1, 6):
        num_r = profil[num_q - 1]
        recs_question = [r for r in recos if r["question"] == lesquestions[num_q]]

        with st.expander(f"Q{num_q}. {lesquestions[num_q]}  — Reponse :  {lesreponses[num_q][num_r]}", expanded=True):
            for r in recs_question:
                s = STYLE_PRIORITE.get(r["priorite"], {"bg": "#F2F3F4", "border": "#7F8C8D", "texte": "#2C3E50", "badge": "#7F8C8D"})
                st.markdown(
                    f"""
                    <div style="border-left:5px solid {s['border']}; border-radius:6px;
                                padding:12px 16px; margin-bottom:10px; background-color:{s['bg']};">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                            <span style="font-weight:700; color:#1C2833; font-size:1.02em;">{r['recommandation']}</span>
                            <span style="background-color:{s['badge']}; color:#FFFFFF; font-weight:700;
                                         font-size:0.78em; padding:3px 10px; border-radius:12px; white-space:nowrap; margin-left:10px;">
                                {r['priorite']}
                            </span>
                        </div>
                        <div style="font-size:0.85em; color:{s['texte']}; font-weight:600; margin-bottom:4px;">
                            📘 Réf. guide CMRPI/AUSIM : {r['guide']}
                        </div>
                        <div style="font-size:0.85em; color:#4A4A4A;"><b>Justification (texte du guide CMRPI/AUSIM) :</b> 
                            {r['Justification (texte du guide CMRPI/AUSIM)']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.divider()
    pdf_buffer = generer_pdf_bytes(entreprise, profil)

    st.download_button(
        "📄 Télécharger le rapport (PDF)",
        data=pdf_buffer,
        file_name=f"rapport_{entreprise['nom'].replace(' ', '_')}.pdf",
        mime="application/pdf",
    )

    if st.button("🔄 Nouvel audit"):
        reset()
        st.rerun()
