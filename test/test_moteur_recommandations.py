import unittest
from core.moteur_recommandation import moteur_recommandations


class TestMoteurRecommandation(unittest.TestCase):

    def test_resultats_tries_par_priorite(self):
        recos = moteur_recommandations([1, 1, 1, 1, 1])
        ordre = {"Critique": 0, "Elevee": 1, "Moyenne": 2}
        valeurs = [ordre[r["priorite"]] for r in recos]
        self.assertEqual(valeurs, sorted(valeurs))

    def test_chaque_recommandation_a_les_champs_attendus(self):
        recos = moteur_recommandations([2, 3, 1, 4, 2])
        for r in recos:
            for champ in ("question", "reponse", "recommandation", "priorite", "guide"):
                self.assertIn(champ, r)

    def test_meilleur_profil_donne_moins_de_recommandations(self):
        recos_faible = moteur_recommandations([1, 1, 1, 1, 1])
        recos_fort = moteur_recommandations([4, 4, 4, 4, 4])
        self.assertGreater(len(recos_faible), len(recos_fort))

    def test_toutes_les_priorites_sont_valides(self):
        recos = moteur_recommandations([1, 2, 3, 4, 1])
        priorites_valides = {"Critique", "Elevee", "Moyenne"}
        for r in recos:
            self.assertIn(r["priorite"], priorites_valides)

    def test_profil_avec_5_reponses_exactement(self):
        with self.assertRaises(Exception):
            moteur_recommandations([1, 1, 1, 1])


if __name__ == "__main__":
    unittest.main()