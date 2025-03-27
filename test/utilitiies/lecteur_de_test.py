from ...src.lecteur import Lecteur


class LecteurDeTest(Lecteur):
    def __init__(self):
        self.__numero_badge_detecte = None

    def poll(self) -> int | None:
        numero_detecte = self.__numero_badge_detecte
        self.__numero_badge_detecte = None
        return numero_detecte

    def simuler_detection_badge(self):
        self.__numero_badge_detecte = 0