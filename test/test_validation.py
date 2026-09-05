import unittest
from core.validation import email_valide


class TestValidationEmail(unittest.TestCase):

    def test_emails_valides(self):
        self.assertTrue(email_valide("contact@entreprise.com"))
        self.assertTrue(email_valide("j.dupont@sous-domaine.entreprise.co.ma"))
        self.assertTrue(email_valide("  contact@entreprise.com  "))

    def test_emails_invalides(self):
        self.assertFalse(email_valide(""))
        self.assertFalse(email_valide("pas-un-email"))
        self.assertFalse(email_valide("contact@"))
        self.assertFalse(email_valide("@entreprise.com"))
        self.assertFalse(email_valide("contact@entreprise"))


if __name__ == "__main__":
    unittest.main()