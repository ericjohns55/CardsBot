import operator


class Game:
    def __init__(self, rounds, sort):
        self.rounds = rounds
        self.sort = sort
        self.players = {}
        self.started = False
        self.special_rule = ""

    def get_special_rule(self):
        return self.special_rule

    def set_special_rule(self, rule):
        self.special_rule = rule

    def add_player(self, name):
        self.players[name] = Player(name, self.rounds)

    def delete_player(self, name):
        self.players.pop(name)

    def list_players(self):
        names = ""

        for value in self.players.values():
            names += value.get_name().capitalize() + ", "

        return names

    def has_players(self):
        return len(self.players) != 0

    def has_player(self, name):
        return name in self.players

    def get_player(self, name):
        return self.players[name]

    def get_rounds(self):
        return self.rounds

    def is_started(self):
        return self.started

    def start_game(self):
        self.started = True

    def scores_in(self, round_number):
        scores_in = True

        for player in self.players:
            if self.players[player].get_score(round_number) == -1:
                scores_in = False

        return scores_in

    def sort_scores(self):
        reverse = True if self.sort.lower() == "high" else False

        scoreboard = []

        for player in (sorted(self.players.values(), key=operator.attrgetter('score_total'), reverse=reverse)):
            scoreboard.append(player.name)

        return scoreboard

    def get_score_breakdown(self):
        score_breakdown = "All Scores:\n"

        round_found = False

        for player in self.players:
            temp_player = self.players[player].get_name().capitalize() + ": "

            for round_num in range(self.rounds):
                if self.players[player].get_score(round_num + 1) != -1:
                    round_found = True
                    temp_player += str(self.players[player].get_score(round_num + 1)) + ", "

            if round_found:
                score_breakdown += temp_player[0:len(temp_player) - 2] + "\n"
            else:
                score_breakdown += "No rounds have been played yet."
                break

        return score_breakdown

    def get_average_score(self, round_number):
        total = 0

        for player in self.players:
            total += int(self.players[player].get_score(round_number))

        return float(total / len(self.players))


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

    def get_name(self):
        return self.name

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
