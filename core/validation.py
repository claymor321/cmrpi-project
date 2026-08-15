import re
PATTERN_EMAIL = r"^[\w\.-]+@[\w\.-]+\.\w+$"
def email_valide(adresse):
 return re.match(PATTERN_EMAIL, adresse.strip()) is not None
DOMAINES_AUTORISES = ("gmail.com", "outlook.com", "yahoo.com", "hotmail.com")
def domaine_autorise(adresse):
   if "@" not in adresse:
                        return False
   domaine = adresse.strip().lower().split("@")[-1]
   return domaine in DOMAINES_AUTORISES