class Player:
    def __init__(self, name, rounds):
        self.name = name
        self.score_total = 0
        self.scores = {}

        for i in range(0, rounds):
            self.scores[i] = -1

    def add_round(self, round_number, score):
        self.scores[round_number - 1] = score
        self.calculate_scores()

    def get_score(self, round_number):
        return self.scores[round_number - 1]

    def calculate_scores(self):
        total = 0

        for i in range(0, len(self.scores)):
            if self.scores[i] != -1:
                total += int(self.scores[i])

        self.score_total = total

    def get_total_score(self):
        return self.score_total

    def __lt__(self, other):
        return self.score_total < other.score_total
