import unittest


from .utilitiies.lecteur_de_test import LecteurDeTest
from .utilitiies.porte_de_test import PorteDeTest
from ..src.controleur_acces import ControleurAcces


class ControleurAccesTests(unittest.TestCase):

    def test_cas_nominal(self):
        lecteur = LecteurDeTest()
        lecteur.simuler_detection_badge()
        porte = PorteDeTest()
        ControleurAcces(porte, lecteur).interroger_lecteur()
        self.assertTrue(porte.signal_ouverture_reçu)

    def test_sans_detection(self):
        lecteur = LecteurDeTest()
        porte = PorteDeTest()
        ControleurAcces(porte, lecteur).interroger_lecteur()
        self.assertFalse(porte.signal_ouverture_reçu)

    def test_sans_interrogation(self):
        lecteur = LecteurDeTest()
        lecteur.simuler_detection_badge()
        porte = PorteDeTest()
        ControleurAcces(porte, lecteur)
        self.assertFalse(porte.signal_ouverture_reçu)

    def test_detection_multiple_badges(self):
        lecteur = LecteurDeTest()
        porte = PorteDeTest()
        controleur = ControleurAcces(porte, lecteur)
        for _ in range(3):
            lecteur.simuler_detection_badge()
            controleur.interroger_lecteur()
        self.assertTrue(porte.signal_ouverture_reçu)

    def test_porte_ne_souvre_pas_sans_badge(self):
        lecteur = LecteurDeTest()
        porte = PorteDeTest()
        controleur = ControleurAcces(porte, lecteur)
        controleur.interroger_lecteur()
        self.assertFalse(porte.signal_ouverture_reçu)

    def test_reset_signal_ouverture(self):
        lecteur = LecteurDeTest()
        lecteur.simuler_detection_badge()
        porte = PorteDeTest()
        controleur = ControleurAcces(porte, lecteur)
        controleur.interroger_lecteur()
        self.assertTrue(porte.signal_ouverture_reçu)
        porte.signal_ouverture_reçu = False
        self.assertFalse(porte.signal_ouverture_reçu)

    def test_lecture_sans_detection_apres_utilisation(self):
        lecteur = LecteurDeTest()
        lecteur.simuler_detection_badge()
        porte = PorteDeTest()
        controleur = ControleurAcces(porte, lecteur)
        controleur.interroger_lecteur()
        self.assertTrue(porte.signal_ouverture_reçu)
        porte.signal_ouverture_reçu = False
        controleur.interroger_lecteur()
        self.assertFalse(porte.signal_ouverture_reçu)

    def test_interrogation_frequente(self):
        lecteur = LecteurDeTest()
        porte = PorteDeTest()
        controleur = ControleurAcces(porte, lecteur)
        for _ in range(10):
            controleur.interroger_lecteur()
        self.assertFalse(porte.signal_ouverture_reçu)

    def test_badge_reset_apres_lecture(self):
        lecteur = LecteurDeTest()
        porte = PorteDeTest()
        controleur = ControleurAcces(porte, lecteur)
        lecteur.simuler_detection_badge()
        controleur.interroger_lecteur()
        self.assertTrue(porte.signal_ouverture_reçu)
        porte.signal_ouverture_reçu = False
        controleur.interroger_lecteur()
        self.assertFalse(porte.signal_ouverture_reçu)

    def test_reaction_si_lecteur_est_null(self):
        porte = PorteDeTest()
        with self.assertRaises(AttributeError):
            ControleurAcces(porte, None).interroger_lecteur()

    def test_lecteur_detection_alternée(self):
        lecteur = LecteurDeTest()
        porte = PorteDeTest()
        controleur = ControleurAcces(porte, lecteur)
        lecteur.simuler_detection_badge()
        controleur.interroger_lecteur()
        self.assertTrue(porte.signal_ouverture_reçu)
        porte.signal_ouverture_reçu = False
        controleur.interroger_lecteur()
        self.assertFalse(porte.signal_ouverture_reçu)
        lecteur.simuler_detection_badge()
        controleur.interroger_lecteur()
        self.assertTrue(porte.signal_ouverture_reçu)

    def test_porte_recoit_signal_apres_lecture_valide(self):
        lecteur = LecteurDeTest()
        porte = PorteDeTest()
        controleur = ControleurAcces(porte, lecteur)
        lecteur.simuler_detection_badge()
        controleur.interroger_lecteur()
        self.assertTrue(porte.signal_ouverture_reçu)

    def test_aucune_detection_apres_lecture(self):
        lecteur = LecteurDeTest()
        porte = PorteDeTest()
        controleur = ControleurAcces(porte, lecteur)
        lecteur.simuler_detection_badge()
        controleur.interroger_lecteur()
        self.assertTrue(porte.signal_ouverture_reçu)
        lecteur.poll()
        self.assertIsNone(lecteur.poll())

    # Ajout de 15 tests supplémentaires ici
    def test_signal_ouverture_initialement_faux(self):
        porte = PorteDeTest()
        self.assertFalse(porte.signal_ouverture_reçu)

    def test_multiple_lectures_sans_interrogation(self):
        lecteur = LecteurDeTest()
        porte = PorteDeTest()
        controleur = ControleurAcces(porte, lecteur)
        for _ in range(5):
            lecteur.simuler_detection_badge()
        self.assertFalse(porte.signal_ouverture_reçu)

    def test_porte_ne_souvre_pas_sans_lecteur(self):
        # ETANT DONNE une porte sans lecteur associé
        porte = PorteDeTest()

        # QUAND on tente de créer un contrôleur avec un lecteur inexistant
        with self.assertRaises(AttributeError):
            ControleurAcces(porte, None).interroger_lecteur()

    def test_lecture_apres_signal_recu(self):
        # ETANT DONNE un lecteur ayant détecté un badge
        lecteur = LecteurDeTest()
        lecteur.simuler_detection_badge()

        # ET une porte
        porte = PorteDeTest()

        # ET un contrôleur
        controleur = ControleurAcces(porte, lecteur)

        # QUAND le contrôleur interroge le lecteur
        controleur.interroger_lecteur()

        # ALORS la porte reçoit un signal d'ouverture
        self.assertTrue(porte.signal_ouverture_reçu)

        # ET QUAND on interroge une nouvelle fois le lecteur
        porte.signal_ouverture_reçu = False
        controleur.interroger_lecteur()

        # ALORS la porte ne s'ouvre pas
        self.assertFalse(porte.signal_ouverture_reçu)

    def test_detection_tardive(self):
        # ETANT DONNE un lecteur sans badge détecté initialement
        lecteur = LecteurDeTest()
        porte = PorteDeTest()
        controleur = ControleurAcces(porte, lecteur)

        # QUAND on interroge le lecteur sans badge détecté
        controleur.interroger_lecteur()

        # ALORS la porte ne reçoit pas de signal d'ouverture
        self.assertFalse(porte.signal_ouverture_reçu)

        # ET QUAND un badge est détecté ensuite
        lecteur.simuler_detection_badge()
        controleur.interroger_lecteur()

        # ALORS la porte reçoit un signal d'ouverture
        self.assertTrue(porte.signal_ouverture_reçu)

    def test_signal_ouverture_reset_apres_temps(self):
        # ETANT DONNE un lecteur ayant détecté un badge
        lecteur = LecteurDeTest()
        lecteur.simuler_detection_badge()

        # ET une porte
        porte = PorteDeTest()

        # ET un contrôleur
        controleur = ControleurAcces(porte, lecteur)

        # QUAND on interroge le lecteur
        controleur.interroger_lecteur()

        # ALORS la porte s'ouvre
        self.assertTrue(porte.signal_ouverture_reçu)

        # ET QUAND on attend un certain temps avant de réinterroger le lecteur
        porte.signal_ouverture_reçu = False  # Supposons que la porte se referme après un moment
        controleur.interroger_lecteur()

        # ALORS la porte ne se réouvre pas
        self.assertFalse(porte.signal_ouverture_reçu)

    def test_interrogation_sans_detection_et_avec_detection_apres(self):
        # ETANT DONNE un lecteur sans badge détecté
        lecteur = LecteurDeTest()
        porte = PorteDeTest()
        controleur = ControleurAcces(porte, lecteur)

        # QUAND on interroge le lecteur
        controleur.interroger_lecteur()

        # ALORS la porte ne reçoit pas de signal
        self.assertFalse(porte.signal_ouverture_reçu)

        # ET QUAND un badge est détecté après coup
        lecteur.simuler_detection_badge()
        controleur.interroger_lecteur()

        # ALORS la porte s'ouvre
        self.assertTrue(porte.signal_ouverture_reçu)



    def test_deux_controleurs_avec_meme_lecteur(self):
        # ETANT DONNE un lecteur et une porte
        lecteur = LecteurDeTest()
        porte = PorteDeTest()

        # ET deux contrôleurs
        controleur1 = ControleurAcces(porte, lecteur)
        controleur2 = ControleurAcces(porte, lecteur)

        # QUAND un badge est détecté
        lecteur.simuler_detection_badge()

        # ET les deux contrôleurs interrogent
        controleur1.interroger_lecteur()
        controleur2.interroger_lecteur()

        # ALORS la porte s'ouvre
        self.assertTrue(porte.signal_ouverture_reçu)

    def test_porte_souvre_une_seule_fois_par_badge(self):
        # ETANT DONNE un lecteur ayant détecté un badge
        lecteur = LecteurDeTest()
        lecteur.simuler_detection_badge()

        # ET une porte
        porte = PorteDeTest()

        # ET un contrôleur
        controleur = ControleurAcces(porte, lecteur)

        # QUAND le contrôleur interroge le lecteur
        controleur.interroger_lecteur()

        # ALORS la porte reçoit un signal d'ouverture
        self.assertTrue(porte.signal_ouverture_reçu)

        # ET QUAND on réinterroge le lecteur sans nouvelle détection
        porte.signal_ouverture_reçu = False
        controleur.interroger_lecteur()

        # ALORS la porte ne se rouvre pas
        self.assertFalse(porte.signal_ouverture_reçu)



if __name__ == '__main__':
    unittest.main()
