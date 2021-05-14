from player import Player
import operator


class Game:
    def __init__(self, rounds, sort):
        self.rounds = rounds
        self.sort = sort
        self.players = {}

    def add_player(self, name):
        self.players[name] = Player(name, self.rounds)

    def delete_player(self, name):
        self.players.pop(name)

    def has_player(self, name):
        return name in self.players

    def get_player(self, name):
        return self.players[name]

    def scores_in(self, round_number):
        scores_in = True

        for player in self.players:
            if self.players[player].get_score(round_number) == -1:
                scores_in = False

        return scores_in

    def sort_scores(self):
        index = 0

        reverse = True if self.sort.lower() == "desc" else False

        scoreboard = []

        for player in (sorted(self.players.values(), key=operator.attrgetter('score_total'), reverse=reverse)):
            scoreboard.append(player.name)
            index += 0

        return scoreboard

    def get_rounds(self):
        return self.rounds
