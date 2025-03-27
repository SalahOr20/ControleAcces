from ...src.porte import Porte


class PorteDeTest(Porte):
    def __init__(self):
        self.signal_ouverture_reçu = False

    def demander_ouverture(self):
        self.signal_ouverture_reçu = True