import game


class Persist:
    game = None
    round = 1

    started = False
    looking_for_players = False

    shanghai = False

    shanghai_hands = ["two trips", "one trip and a run of four", "two runs of four", "three trips",
                      "one trip and a run of seven", "one trip and two runs of four", "three runs of four",
                      "three trips and a run of four", "one trip and a run of ten", "three runs of five"]
