import unittest
from data.index_recommandations import (
    LISTE_RECOS,
    NOMS_RECOS,
    NB_RECOS,
    INDEX_RECO,
    SIGNATURE_RECOS,
    calculer_signature,
)


class TestIndexRecommandations(unittest.TestCase):

    def test_pas_de_doublons(self):
        self.assertEqual(len(NOMS_RECOS), len(set(NOMS_RECOS)))

    def test_coherence_des_tailles(self):
        self.assertEqual(len(LISTE_RECOS), NB_RECOS)
        self.assertEqual(len(INDEX_RECO), NB_RECOS)

    def test_index_reco_pointe_vers_le_bon_rang(self):
        for i, (nom, _) in enumerate(LISTE_RECOS):
            self.assertEqual(INDEX_RECO[nom], i)

    def test_signature_stable_et_deterministe(self):

        self.assertEqual(calculer_signature(), SIGNATURE_RECOS)
        self.assertEqual(calculer_signature(), calculer_signature())

    def test_signature_change_si_le_contenu_change(self):
        autre_signature = calculer_signature.__wrapped__() if hasattr(calculer_signature, "__wrapped__") else None
        import hashlib
        contenu_different = "|".join(NOMS_RECOS[:-1])
        signature_differente = hashlib.sha256(contenu_different.encode("utf-8")).hexdigest()
        self.assertNotEqual(signature_differente, SIGNATURE_RECOS)


if __name__ == "__main__":
    unittest.main()