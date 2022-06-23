from telegram.ext import CallbackContext
from telegram import Update
from cards_bot import Persist
from game import Game
import cards_bot


def create_command(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id

    if chat_id in Persist.games:
        update.message.reply_text("Two simultaneous games cannot exist in one chat.")
    else:
        args = update.message.text.replace("/create ", "").split(" ")

        if len(args) == 2 and cards_bot.is_integer(args[0]):
            Persist.games[chat_id] = Game(int(args[0]), args[1])
            update.message.reply_text("Created a game with {0} rounds, use /join or /add to join the game.".format(args[0]))
        else:
            update.message.reply_text("Invalid arguments, use /create <rounds> <low/high>")


def shanghai_command(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id

    if chat_id in Persist.games:
        update.message.reply_text("Two simultaneous games cannot exist in one chat.")
    else:
        Persist.games[chat_id] = Game(10, "low")
        Persist.games[chat_id].set_special_rule("shanghai")
        Persist.rounds[chat_id] = 1
        update.message.reply_text("Shanghai game created, use /join or /add to join the game.")

    return


def dominoes_command(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id

    if chat_id in Persist.games:
        update.message.reply_text("Two simultaneous games cannot exist in one chat.")
    else:
        Persist.games[chat_id] = Game(13, "low")
        Persist.games[chat_id].set_special_rule("dominoes")
        Persist.rounds[chat_id] = 1
        update.message.reply_text("Dominoes game created, use /join or /add to join the game.")
    return


def rummy_command(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id

    if chat_id in Persist.games:
        update.message.reply_text("Two simultaneous games cannot exist in one chat.")
    else:
        Persist.games[chat_id] = Game(100, "high")
        Persist.games[chat_id].set_special_rule("rummy")
        Persist.rounds[chat_id] = 1
        update.message.reply_text("Rummy game created, use /join or /add to join the game.")
    return


def start_command(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id

    if chat_id in Persist.games:
        if Persist.games[chat_id].is_started():
            update.message.reply_text("This game has already started")
        else:
            Persist.games[chat_id].start_game()

            message = "Now accepting scores for round " + str(Persist.rounds[chat_id])

            if Persist.games[chat_id].get_special_rule() == "shanghai":
                message = "The first shanghai hand is " + Persist.shanghai_hands[0] + "\n" + message

            update.message.reply_text(message)
    else:
        update.message.reply_text("You must create a game before you can start it.\nUse /create <rounds> <low/high> or /create shanghai")


def end_command(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id

    if chat_id in Persist.games:
        message = "Stopping the current game.\nThe final scores are as follows:" + cards_bot.get_scoreboard(chat_id)

        update.message.reply_text(message)

        Persist.games.pop(chat_id)
    else:
        update.message.reply_text("There is no active game right now.")


def add_player_command(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id

    if chat_id in Persist.games:
        if Persist.games[chat_id].is_started():
            update.message.reply_text("This game has already started.")
            return

        player_name = update.message.text.replace("/add ", "").lower()

        Persist.games[chat_id].add_player(player_name)
        update.message.reply_text("Added player {0} to the game.".format(player_name.capitalize()))
    else:
        update.message.reply_text("A game does not exist yet in this chat.")


def remove_player_command(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    player_name = update.message.text.replace("/remove ", "").lower()

    if chat_id in Persist.games:
        if Persist.games[chat_id].has_player(player_name):
            Persist.games[chat_id].delete_player(player_name)
            update.message.reply_text("Removed player {0} to the game.".format(player_name.capitalize()))
        else:
            update.message.reply_text("That player does not exist in the game.")
    else:
        update.message.reply_text("A game does not exist yet in this chat.")


def join_command(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    sender_name = update.message.from_user.first_name.lower()

    if chat_id in Persist.games:
        if Persist.games[chat_id].is_started():
            update.message.reply_text("This game has already started.")
            return

        Persist.games[chat_id].add_player(sender_name)
        update.message.reply_text("Added player {0} to the game.".format(sender_name.capitalize()))
    else:
        update.message.reply_text("A game does not exist yet in this chat.")


def leave_command(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    sender_name = update.message.from_user.first_name.lower()

    if chat_id in Persist.games:
        if Persist.games[chat_id].has_player(sender_name):
            Persist.games[chat_id].delete_player(sender_name)
            update.message.reply_text("Removed player {0} to the game.".format(sender_name.capitalize()))
        else:
            update.message.reply_text("That player does not exist in the game.")
    else:
        update.message.reply_text("A game does not exist yet in this chat.")


def score_command(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    sender_name = update.message.from_user.first_name.lower()
    args = update.message.text.replace("/score ", "").lower().split(" ")

    if chat_id not in Persist.games:
        update.message.reply_text("A game does not exist.")
        return

    if not Persist.games[chat_id].is_started():
        update.message.reply_text("This game has not started.")
        return

    player = sender_name
    score = args[0]

    if len(args) == 2:
        player = str(args[0])
        score = args[1]

    if not cards_bot.is_integer(score):
        update.message.reply_text("Invalid score")
        return

    if Persist.games[chat_id].has_player(player):
        Persist.games[chat_id].get_player(player).add_round(Persist.rounds[chat_id], score)

        if Persist.games[chat_id].scores_in(Persist.rounds[chat_id]):
            scoreboard = Persist.games[chat_id].sort_scores()
            average_score = str(round(Persist.games[chat_id].get_average_score(Persist.rounds[chat_id]), 2))

            full_scores = "All scores are in for this round.\nThe round average was {0} points.\n\nHere is the updated scoreboard:".format(average_score)
            full_scores += cards_bot.get_scoreboard(chat_id)

            update.message.reply_text(full_scores)

            if Persist.games[chat_id].get_rounds() == Persist.rounds[chat_id] or\
                    (Persist.games[chat_id].get_player(scoreboard[0]).get_total_score() >= 500 and
                     Persist.games[chat_id].get_special_rule() == "rummy"):
                update.message.reply_text("The game is over.\nThe winner is {0} with a score of {1} points"
                                          .format(scoreboard[0].capitalize(),
                                                  Persist.games[chat_id].get_player(scoreboard[0]).get_total_score()))

                Persist.games.pop(chat_id)
            else:
                Persist.rounds[chat_id] = Persist.rounds[chat_id] + 1

                message = "Now accepting scores for round {0}".format(Persist.rounds[chat_id])

                if Persist.games[chat_id].get_special_rule() == "shanghai":
                    message = "The upcoming shanghai hand is {0}\n\n".format(Persist.shanghai_hands[Persist.rounds[chat_id] - 1]) + message

                update.message.reply_text(message)
    else:
        update.message.reply_text("Player {0} does not exist.".format(player))


def update_score_command(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    args = update.message.text.replace("/update ", "").lower().split(" ")

    if len(args) != 3 or (not cards_bot.is_integer(args[1]) or not cards_bot.is_integer(args[2])):
        update.message.reply_text("Invalid arguments, use /update <player> <round> <score>")
        return

    if chat_id in Persist.games:
        if Persist.games[chat_id].is_started():
            if Persist.games[chat_id].has_player(args[0]):
                Persist.games[chat_id].get_player(args[0]).add_round(int(args[1]), int(args[2]))
            else:
                update.message.reply_text("This player does not exist.")
        else:
            update.message.reply_text("The game has not started yet.")
    else:
        update.message.reply_text("No game exists.")


def scoreboard_command(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id

    if chat_id in Persist.games:
        if Persist.games[chat_id].is_started():
            update.message.reply_text(cards_bot.get_scoreboard(chat_id))
        else:
            update.message.reply_text("The game has not started yet.")
    else:
        update.message.reply_text("No game exists.")


def players_command(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id

    if chat_id in Persist.games:
        if Persist.games[chat_id].has_players():
            players = "Current game players: " + Persist.games[chat_id].list_players()

            update.message.reply_text(players[0:len(players) - 2])
        else:
            update.message.reply_text("Nobody has joined the game yet.")
    else:
        update.message.reply_text("No game exists.")


def breakdown_command(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id

    if chat_id in Persist.games:
        if Persist.games[chat_id].is_started():
            update.message.reply_text(Persist.games[chat_id].get_score_breakdown())
        else:
            update.message.reply_text("The game has not started yet.")
    else:
        update.message.reply_text("No game exists.")
