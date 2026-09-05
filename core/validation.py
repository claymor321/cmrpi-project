import re
PATTERN_EMAIL = r"^[\w\.-]+@[\w\.-]+\.\w+$"
def email_valide(adresse):
 return re.match(PATTERN_EMAIL, adresse.strip()) is not None
