import time
import telepot


def handle(msg):
    sender = msg['from']['first_name']
    command = msg['text']

    arguments = parse_arguments(command)

    if len(arguments) == 1:
        if arguments[0] == "!join":
            print(sender + " joined the game")
        elif arguments[0] == "!leave":
            print(sender + " left the game")
        elif arguments[0] == "!scores":
            print("SCOREBOARD HERE")
        else:
            print(sender + ": " + arguments[0])
    elif len(arguments) != 0:
        if arguments[1].lower() == "shanghai":
            print(sender + ": shanghai start")

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

    valid_commands = ["!join", "!leave", "!scores"]

    if split[0].lower() == "!startgame":
        if len(split) == 2 and split[1].lower() == "shanghai":
            print("Shanghai selected")
        elif len(split) == 3:
            if not (split[1].isdigit() and ("asc" in split[2] or "desc" in split[2])):
                split = []
        else:
            split = []
    elif split[0].lower() not in valid_commands:
        split = []

    return split


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
