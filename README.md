
# CardsBot

A Telegram bot that tracks scores for any game with multiple rounds.

## Features
- Allows a player to join a game using their Telegram profile
- Let's the group add another player by name (without them being in the chat)
- Automatically ends the game and announces a winner once the last round ends
- Sends an average score per round after all scores are inputted
- Allows scores to be sorted in either ascending or descending order

## Commands
### /create \<rounds> \<low/high>
Creates a game with the specified number of rounds, and will sort the scores where the winner either has the lowest or highest score

### /start
Starts the game once all your players have joined

### /end
Manually ends the game if you do not get to the end

### /join
Joins the game using your Telegram username

### /leave
Leaves the game if you joined using the /join command

### /add \<name>
Adds a player with the provided name to a game

### /remove \<name>
Removes a player from the game

### /score \<number> OR /score \<name> \<number>
Sets your score for the round to the number provided, or sets another player's score to the number provided

### /update \<name> \<round> \<number>
Updates a player's score for any round given

### /scores
Shows the current scoreboard for the game

### /players
Lists all of the players in the game

### /breakdown
Lists a breakdown of all the scores in the game so far

### /rummy
Creates a predefined game of Rummy 500, where the game will automatically end once a player hits 500 points

### /dominoes
Creates a predefined game of dominoes with 13 rounds

### /shanghai
Creates a predefined game of Shanghai, where the next hand requirements are announced after each round
