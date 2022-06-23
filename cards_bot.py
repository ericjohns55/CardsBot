from telegram.ext import Updater, CommandHandler
import commands


if __name__ == '__main__':
    try:
        updater = Updater(open("api-key.txt", "r").read())

        updater.dispatcher.add_handler(CommandHandler("create", commands.create_command))
        updater.dispatcher.add_handler(CommandHandler("start", commands.start_command))
        updater.dispatcher.add_handler(CommandHandler("end", commands.end_command))
        updater.dispatcher.add_handler(CommandHandler("add", commands.add_player_command))
        updater.dispatcher.add_handler(CommandHandler("remove", commands.remove_player_command))
        updater.dispatcher.add_handler(CommandHandler("join", commands.join_command))
        updater.dispatcher.add_handler(CommandHandler("leave", commands.leave_command))
        updater.dispatcher.add_handler(CommandHandler("score", commands.score_command))
        updater.dispatcher.add_handler(CommandHandler("update", commands.update_score_command))
        updater.dispatcher.add_handler(CommandHandler("scores", commands.scoreboard_command))
        updater.dispatcher.add_handler(CommandHandler("players", commands.players_command))
        updater.dispatcher.add_handler(CommandHandler("breakdown", commands.breakdown_command))
        updater.dispatcher.add_handler(CommandHandler("shanghai", commands.shanghai_command))
        updater.dispatcher.add_handler(CommandHandler("dominoes", commands.dominoes_command))
        updater.dispatcher.add_handler(CommandHandler("rummy", commands.rummy_command))

        updater.start_polling(poll_interval=0.25)

        print("Successfully started CardsBot")

        updater.idle()
    except FileNotFoundError:
        print("Could not read API key")
        quit()


def get_scoreboard(chat_id):
    scoreboard = Persist.games[chat_id].sort_scores()

    full_scores = ""

    for i in range(len(scoreboard)):
        name = scoreboard[i]
        full_scores += "\n" + str(i + 1) + ": " + name.capitalize() + " (" + \
                       str(Persist.games[chat_id].get_player(name).get_total_score()) + " points)"

    return full_scores


def is_integer(string):
    integer = True

    try:
        int(string)
    except ValueError:
        integer = False

    return integer


class Persist:
    games = {}
    rounds = {}

    started = False
    looking_for_players = False

    shanghai_hands = ["two trips", "one trip and a run of four", "two runs of four", "three trips",
                      "one trip and a run of seven", "one trip and two runs of four", "three runs of four",
                      "three trips and a run of four", "one trip and a run of ten", "three runs of five"]
