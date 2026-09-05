import unittest
from statistique.score import (
    score_risque_global,
    score_maturite,
    classifier_niveau_risque,
    compter_priorites,
    score_risque_par_question,
    comparaison_meilleur_cas,
    question_prioritaire,
    analyser_priorites_du_profil,
)


class TestScoreRisque(unittest.TestCase):

    def test_pire_cas_risque_maximal(self):
        risque = score_risque_global([1, 1, 1, 1, 1])
        self.assertAlmostEqual(risque["pct_risque"], 100.0, places=1)

    def test_meilleur_cas_risque_minimal(self):
        risque = score_risque_global([4, 4, 4, 4, 4])
        self.assertLess(risque["pct_risque"], 20)

    def test_risque_decroit_quand_les_reponses_s_ameliorent(self):
        faible = score_risque_global([1, 1, 1, 1, 1])["pct_risque"]
        moyen = score_risque_global([2, 2, 2, 2, 2])["pct_risque"]
        fort = score_risque_global([4, 4, 4, 4, 4])["pct_risque"]
        self.assertGreater(faible, moyen)
        self.assertGreater(moyen, fort)

    def test_score_par_question_a_5_entrees(self):
        scores = score_risque_par_question([1, 2, 3, 4, 1])
        self.assertEqual(len(scores), 5)
        for num_q in range(1, 6):
            self.assertIn(num_q, scores)


class TestMaturite(unittest.TestCase):

    def test_maturite_est_complement_du_risque(self):
        profil = [2, 3, 1, 4, 2]
        risque = score_risque_global(profil)
        maturite = score_maturite(profil)
        self.assertAlmostEqual(maturite, round(100 - risque["pct_risque"], 1))

    def test_comparaison_meilleur_cas_marge_positive_ou_nulle(self):
        comparaison = comparaison_meilleur_cas([1, 1, 1, 1, 1])
        self.assertGreaterEqual(comparaison["marge_de_progression"], 0)
        self.assertGreaterEqual(
            comparaison["maturite_max_atteignable"], comparaison["maturite_actuelle"]
        )


class TestClassification(unittest.TestCase):

    def test_classification_coherente_avec_pct(self):
        self.assertEqual(classifier_niveau_risque(80), "Risque critique")
        self.assertEqual(classifier_niveau_risque(50), "Risque élevé")
        self.assertEqual(classifier_niveau_risque(25), "Risque modéré")
        self.assertEqual(classifier_niveau_risque(5), "Risque maîtrisé")

    def test_bornes_de_classification(self):
        self.assertEqual(classifier_niveau_risque(70), "Risque critique")
        self.assertEqual(classifier_niveau_risque(69.9), "Risque élevé")
        self.assertEqual(classifier_niveau_risque(45), "Risque élevé")
        self.assertEqual(classifier_niveau_risque(20), "Risque modéré")


class TestCompterPriorites(unittest.TestCase):

    def test_compter_priorites_total_correct(self):
        recs = [{"priorite": "Critique"}, {"priorite": "Moyenne"}, {"priorite": "Critique"}]
        compte = compter_priorites(recs)
        self.assertEqual(compte["Critique"], 2)
        self.assertEqual(compte["Moyenne"], 1)
        self.assertEqual(compte["Elevee"], 0)
        self.assertEqual(compte["total"], 3)

    def test_liste_vide(self):
        compte = compter_priorites([])
        self.assertEqual(compte["total"], 0)


class TestAnalyseEtQuestionPrioritaire(unittest.TestCase):

    def test_question_prioritaire_retourne_un_numero_valide(self):
        num_q, score, texte = question_prioritaire([1, 4, 1, 4, 1])
        self.assertIn(num_q, range(1, 6))
        self.assertIsInstance(texte, str)

    def test_analyser_priorites_repartition_par_question(self):
        par_question, total_global = analyser_priorites_du_profil([1, 1, 1, 1, 1])
        self.assertEqual(len(par_question), 5)
        somme_critique = sum(par_question[q]["Critique"] for q in par_question)
        self.assertEqual(somme_critique, total_global["Critique"])


if __name__ == "__main__":
    unittest.main()