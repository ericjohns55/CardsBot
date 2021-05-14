import time
import telepot
from persistence import Persist
from game import Game


def handle(msg):
    chat_id = msg['chat']['id']
    sender = msg['from']['first_name']
    command = msg['text']

    if not command.startswith("!"):
        return

    arguments = parse_arguments(command)

    if len(arguments) == 1:
        if arguments[0] == "!join":
            if Persist.looking_for_players:
                Persist.game.add_player(sender)
                bot.sendMessage(chat_id, sender + " joined the game")
            else:
                print("This game is not looking for players at this moment.")
        elif arguments[0] == "!leave":
            if Persist.game is not None:
                if Persist.game.has_player(sender):
                    Persist.game.delete_player(sender)
                    bot.sendMessage(chat_id, sender + " has quit the game!")
                else:
                    bot.sendMessage(chat_id, "You are not part of this game.")
            else:
                bot.sendMessage(chat_id, "You cannot quit a game that has not started!")
        elif arguments[0] == "!scores":
            if Persist.game is not None:
                if Persist.started:
                    bot.sendMessage(chat_id, "Current scores:" + get_scoreboard())
                else:
                    bot.sendMessage(chat_id, "The game has not started yet!")
            else:
                bot.sendMessage(chat_id, "Cannot calculate scores for a game that does not exist")
        elif arguments[0] == "!begin":
            if Persist.started:
                print("The game has already begun!")
            else:
                Persist.started = True
                Persist.looking_for_players = False
                first_message = "Starting the game.\nNow accepting scores for round " + str(Persist.round)

                if Persist.shanghai:
                    first_message += "\nThe first shanghai hand is " + Persist.shanghai_hands[0] + "."

                bot.sendMessage(chat_id, first_message)
    elif len(arguments) != 0:
        if arguments[1].lower() == "shanghai":
            Persist.game = Game(10, "asc")
            Persist.looking_for_players = True
            bot.sendMessage(chat_id, "Created a Shanghai game in the chat.")
        elif arguments[1].isdigit() and arguments[0] == "!score":
            if Persist.started:
                if Persist.game.has_player(sender):
                    # bot.sendMessage(chat_id, sender + ": " + arguments[1])
                    Persist.game.get_player(sender).add_round(Persist.round, arguments[1])

                    if Persist.game.scores_in(Persist.round):
                        scoreboard = Persist.game.sort_scores()

                        full_scores = "All scores are in for this round\n\nHere is the updated scoreboard:"
                        full_scores += get_scoreboard()

                        bot.sendMessage(chat_id, full_scores)

                        if Persist.round == Persist.game.rounds:
                            bot.sendMessage(chat_id, "The game is over!\n" + scoreboard[0] + " is the winner with " +
                                            str(Persist.game.get_player(scoreboard[0]).get_total_score()) + " points!")
                        else:
                            Persist.round = Persist.round + 1

                            next_round_message = "We are now accepting scores for round " + str(Persist.round)

                            if Persist.shanghai:
                                next_round_message += "\nThis upcoming shanghai hand is " + \
                                                      Persist.shanghai_hands[Persist.round - 1] + "."

                            bot.sendMessage(chat_id, next_round_message)
                else:
                    bot.sendMessage(chat_id, "You are not part of this game")
            else:
                bot.sendMessage(chat_id, "This game has not started yet")
        else:
            Persist.game = Game(int(arguments[1]), arguments[2])
            print(arguments)
    else:
        print("Invalid command")


def parse_arguments(command):
    if not command.startswith("!") and not command.isdigit():
        print("Invalid command")
        return []

    if command.isdigit():
        return [command]

    split = command.split(" ")

    valid_commands = ["!join", "!leave", "!scores", "!begin", "!score"]

    if split[0].lower() == "!startgame":
        if len(split) == 2 and split[1].lower() == "shanghai":
            Persist.shanghai = True
        elif len(split) == 3:
            if not (split[1].isdigit() and ("asc" in split[2] or "desc" in split[2])):
                split = []
        else:
            split = []
    elif split[0].lower() not in valid_commands:
        split = []

    return split


def get_scoreboard():
    scoreboard = Persist.game.sort_scores()

    full_scores = ""

    for i in range(len(scoreboard)):
        name = scoreboard[i]
        full_scores += "\n" + str(i + 1) + ": " + name + " (" + \
                       str(Persist.game.get_player(name).get_total_score()) + ")"

    return full_scores


if __name__ == '__main__':
    try:
        bot = telepot.Bot(open("api-key.txt", "r").read())
        bot.message_loop(handle)
        print('Listening')

        while 1:
            try:
                time.sleep(10)

            except KeyboardInterrupt:
                print('\n Program interrupted')
                exit()

    except FileNotFoundError:
        print("Could not read API key")
        quit()
