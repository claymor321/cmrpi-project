from reportlab.lib import colors
STYLE_PRIORITE = {
    "Critique": {"bg": "#FDEDEC", "border": "#C0392B", "texte": "#922B21", "badge": "#C0392B"},
    "Elevee":   {"bg": "#FEF5E7", "border": "#E67E22", "texte": "#9C640C", "badge": "#E67E22"},
       "Moyenne":  {"bg": "#FEF9E7", "border": "#B7950B", "texte": "#7D6608", "badge": "#B7950B"},
}
TRANCHES_SCORE = [
    {"borne_min": 5, "borne_max": 10, "niveau": "Critique", "couleur": "#C0392B",
     "message": "Niveau de securite tres insuffisant : des mesures urgentes doivent etre mises en oeuvre."},
    {"borne_min": 11, "borne_max": 15, "niveau": "Moyen", "couleur": "#E67E22",
     "message": "Niveau de securite intermediaire : des ameliorations sont necessaires sur plusieurs axes."},
    {"borne_min": 16, "borne_max": 20, "niveau": "Satisfaisant", "couleur": "#27AE60",
     "message": "Bon niveau de securite : maintenez et consolidez les bonnes pratiques en place."},
]
# Couleurs pour le PDF 
COULEUR_PDF = {"Critique": colors.HexColor("#C0392B"), "Elevee": colors.HexColor("#E67E22"), "Moyenne": colors.HexColor("#B7950B")}
FOND_PDF = {"Critique": colors.HexColor("#FDEDEC"), "Elevee": colors.HexColor("#FEF5E7"), "Moyenne": colors.HexColor("#FEF9E7")}