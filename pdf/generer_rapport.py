from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable)
from data.questionnaire import lesquestions,lesreponses,lesrecommandations
from io import BytesIO
from pdf.style_pdf import STYLE_PRIORITE,COULEUR_PDF,FOND_PDF


def generer_pdf_bytes(entreprise, profil):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=2 * cm, bottomMargin=2 * cm, leftMargin=2 * cm, rightMargin=2 * cm
    )
    styles = getSampleStyleSheet()

    style_titre = ParagraphStyle("TitrePrincipal", parent=styles["Title"], fontSize=20, spaceAfter=6)
    style_soustitre = ParagraphStyle("SousTitre", parent=styles["Normal"], fontSize=10.5,
                                     textColor=colors.HexColor("#5D6D7E"), spaceAfter=3)
    style_question = ParagraphStyle("Question", parent=styles["Heading2"], fontSize=13,
                                    textColor=colors.HexColor("#1A5276"), spaceBefore=16, spaceAfter=4)
    style_reponse = ParagraphStyle("Reponse", parent=styles["Normal"], fontSize=10.5,
                                   textColor=colors.HexColor("#145A32"), spaceAfter=8, leftIndent=2)
    style_reco = ParagraphStyle("Reco", parent=styles["Normal"], fontSize=9.5, leading=13,
                                textColor=colors.HexColor("#1C2833"), alignment=TA_JUSTIFY)
    style_meta = ParagraphStyle("Meta", parent=styles["Normal"], fontSize=8.3, leading=11,
                                textColor=colors.HexColor("#5D6D7E"))

    story = []
    story.append(Paragraph("Rapport d'audit de cybersécurité", style_titre))
    story.append(Paragraph("Basé sur le guide CMRPI/AUSIM", style_soustitre))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#D5D8DC"), spaceAfter=10))

    story.append(Paragraph(f"<b>Entreprise :</b> {entreprise['nom']}", style_soustitre))
    story.append(
        Paragraph(f"<b>Secteur :</b> {entreprise['secteur']} &nbsp;|&nbsp; <b>Taille :</b> {entreprise['taille']}",
                  style_soustitre))
    story.append(Paragraph(f"<b>Contact :</b> {entreprise['email_contact']}", style_soustitre))
    story.append(Paragraph(f"<b>Date de l'audit :</b> {entreprise['date_audit']}", style_soustitre))
    story.append(Spacer(1, 0.5 * cm))

    for num_q in range(1, 6):
        num_r = profil[num_q - 1]
        story.append(Paragraph(f"Q{num_q}. {lesquestions[num_q]}", style_question))
        story.append(Paragraph(f"Réponse choisie : <b>{lesreponses[num_q][num_r]}</b>", style_reponse))

        for rec in lesrecommandations[num_q][num_r - 1]:
            couleur = COULEUR_PDF.get(rec["priorite"], colors.HexColor("#7F8C8D"))
            fond = FOND_PDF.get(rec["priorite"], colors.HexColor("#F2F3F4"))

            contenu_cellule = [
                Paragraph(f"<b>{rec['recommandation']}</b>", style_reco),
                Paragraph(f"📘 Réf. guide CMRPI/AUSIM : {rec['guide']}", style_meta),
            ]
            if rec.get("Justification (texte du guide CMRPI/AUSIM)"):
                contenu_cellule.append(Paragraph(rec["Justification (texte du guide CMRPI/AUSIM)"], style_meta))

            tbl = Table(
                [[contenu_cellule, Paragraph(f"<b>{rec['priorite']}</b>", style_reco)]],
                colWidths=[13.5 * cm, 2.3 * cm],
            )
            tbl.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), fond),
                ("LINEBEFORE", (0, 0), (0, 0), 3, couleur),
                ("TEXTCOLOR", (1, 0), (1, 0), couleur),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 0), (1, 0), "CENTER"),
                ("LEFTPADDING", (0, 0), (0, 0), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (1, 0), (1, 0), 8),
            ]))
            story.append(tbl)
            story.append(Spacer(1, 0.25 * cm))

        story.append(Spacer(1, 0.3 * cm))

    doc.build(story)
    buffer.seek(0)
    return buffer
def generer_pdf_bytes_ia(entreprise, profil, recommandations):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=2 * cm, bottomMargin=2 * cm, leftMargin=2 * cm, rightMargin=2 * cm
    )
    styles = getSampleStyleSheet()
    style_titre = ParagraphStyle("TitrePrincipal", parent=styles["Title"], fontSize=20, spaceAfter=6)
    style_soustitre = ParagraphStyle("SousTitre", parent=styles["Normal"], fontSize=10.5,
                                     textColor=colors.HexColor("#5D6D7E"), spaceAfter=3)
    style_priorite_titre = ParagraphStyle("PrioriteTitre", parent=styles["Heading2"], fontSize=13,
                                          spaceBefore=16, spaceAfter=4)
    style_reco = ParagraphStyle("Reco", parent=styles["Normal"], fontSize=9.5, leading=13,
                                textColor=colors.HexColor("#1C2833"), alignment=TA_JUSTIFY)
    style_meta = ParagraphStyle("Meta", parent=styles["Normal"], fontSize=8.3, leading=11,
                                textColor=colors.HexColor("#5D6D7E"))

    story = []
    story.append(Paragraph("Rapport de recommandations — Modèle IA", style_titre))
    story.append(Paragraph("Prédictions du réseau de neurones — guide CMRPI/AUSIM", style_soustitre))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#D5D8DC"), spaceAfter=10))

    # Bloc entreprise identique au rapport questionnaire
    story.append(Paragraph(f"<b>Entreprise :</b> {entreprise['nom']}", style_soustitre))
    story.append(
        Paragraph(f"<b>Secteur :</b> {entreprise['secteur']} &nbsp;|&nbsp; <b>Taille :</b> {entreprise['taille']}",
                  style_soustitre))
    story.append(Paragraph(f"<b>Contact :</b> {entreprise['email_contact']}", style_soustitre))
    story.append(Paragraph(f"<b>Date de l'audit :</b> {entreprise['date_audit']}", style_soustitre))
    story.append(Spacer(1, 0.5 * cm))

    # Regroupement par niveau de priorité (même ordre que l'affichage écran)
    for niveau_prio in ["Critique", "Elevee", "Moyenne"]:
        groupe = [r for r in recommandations if r["priorite"] == niveau_prio]
        if not groupe:
            continue

        couleur_titre = COULEUR_PDF.get(niveau_prio, colors.HexColor("#5D6D7E"))
        titre_style = ParagraphStyle(
            f"Titre_{niveau_prio}", parent=style_priorite_titre, textColor=couleur_titre
        )
        story.append(Paragraph(f"Priorité {niveau_prio} ({len(groupe)})", titre_style))

        for rec in groupe:
            couleur = COULEUR_PDF.get(rec["priorite"], colors.HexColor("#7F8C8D"))
            fond = FOND_PDF.get(rec["priorite"], colors.HexColor("#F2F3F4"))

            contenu_cellule = [
                Paragraph(f"<b>{rec['recommandation']}</b>", style_reco),
                Paragraph(f"📘 Réf. guide CMRPI/AUSIM : {rec['guide']}", style_meta),
            ]

            tbl = Table(
                [[contenu_cellule, Paragraph(f"<b>{rec['priorite']}</b>", style_reco)]],
                colWidths=[13.5 * cm, 2.3 * cm],
            )
            tbl.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), fond),
                ("LINEBEFORE", (0, 0), (0, 0), 3, couleur),
                ("TEXTCOLOR", (1, 0), (1, 0), couleur),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 0), (1, 0), "CENTER"),
                ("LEFTPADDING", (0, 0), (0, 0), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (1, 0), (1, 0), 8),
            ]))
            story.append(tbl)
            story.append(Spacer(1, 0.25 * cm))

        story.append(Spacer(1, 0.3 * cm))

    doc.build(story)
    buffer.seek(0)
    return buffer
"""def generer_pdf_bytes_ia(entreprise, profil, recommandations):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=2 * cm, bottomMargin=2 * cm, leftMargin=2 * cm, rightMargin=2 * cm
    )
    styles = getSampleStyleSheet()
    style_titre = ParagraphStyle("TitrePrincipal", parent=styles["Title"], fontSize=20, spaceAfter=6)
    style_soustitre = ParagraphStyle("SousTitre", parent=styles["Normal"], fontSize=10.5,
                                     textColor=colors.HexColor("#5D6D7E"), spaceAfter=3)
    style_reco = ParagraphStyle("Reco", parent=styles["Normal"], fontSize=9.5, leading=13,
                                textColor=colors.HexColor("#1C2833"), alignment=TA_JUSTIFY)
    style_meta = ParagraphStyle("Meta", parent=styles["Normal"], fontSize=8.3, leading=11,
                                textColor=colors.HexColor("#5D6D7E"))

    story = []
    story.append(Paragraph("Rapport de recommandations — Modèle IA", style_titre))
    story.append(Paragraph("Prédictions du réseau de neurones — guide CMRPI/AUSIM", style_soustitre))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#D5D8DC"), spaceAfter=10))
    story.append(Paragraph(f"<b>Entreprise :</b> {entreprise['nom']}", style_soustitre))
    story.append(Spacer(1, 0.5 * cm))

    for rec in recommandations:
        couleur = COULEUR_PDF.get(rec["priorite"], colors.HexColor("#7F8C8D"))
        fond = FOND_PDF.get(rec["priorite"], colors.HexColor("#F2F3F4"))
        contenu = [
            Paragraph(f"<b>{rec['recommandation']}</b>", style_reco),
            Paragraph(f"📘 Réf. guide CMRPI/AUSIM : {rec['guide']}", style_meta),
        ]
        tbl = Table([[contenu, Paragraph(f"<b>{rec['priorite']}</b>", style_reco)]],
                     colWidths=[13.5 * cm, 2.3 * cm])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), fond),
            ("LINEBEFORE", (0, 0), (0, 0), 3, couleur),
            ("TEXTCOLOR", (1, 0), (1, 0), couleur),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (1, 0), (1, 0), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 0.25 * cm))

    doc.build(story)
    buffer.seek(0)
    return buffer"""


