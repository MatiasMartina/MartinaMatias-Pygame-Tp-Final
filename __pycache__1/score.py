class GameManager:
    def __init__(self):
        self.score = 0
        self.high_score = 0

    def increase_score(self, points):
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score

    def decrease_score(self, points):
        self.score -= points
        if self.score < 0:
            self.score = 0  # Asegurarse de que el puntaje no sea negativo

    def get_score(self):
        return self.score

    def get_high_score(self):
        return self.high_score