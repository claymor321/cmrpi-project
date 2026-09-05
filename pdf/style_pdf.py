from reportlab.lib import colors
STYLE_PRIORITE = {
    "Critique": {"bg": "#FDEDEC", "border": "#C0392B", "texte": "#922B21", "badge": "#C0392B"},
    "Elevee":   {"bg": "#FEF5E7", "border": "#E67E22", "texte": "#9C640C", "badge": "#E67E22"},
       "Moyenne":  {"bg": "#FEF9E7", "border": "#B7950B", "texte": "#7D6608", "badge": "#B7950B"},
}
# Couleurs pour le PDF 
COULEUR_PDF = {"Critique": colors.HexColor("#C0392B"), "Elevee": colors.HexColor("#E67E22"), "Moyenne": colors.HexColor("#B7950B")}
FOND_PDF = {"Critique": colors.HexColor("#FDEDEC"), "Elevee": colors.HexColor("#FEF5E7"), "Moyenne": colors.HexColor("#FEF9E7")}