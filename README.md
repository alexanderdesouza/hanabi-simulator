<p align="center">
  <img src="https://github.com/alexanderdesouza/hanabi-simulator/blob/master/hanabi-banner.jpg">
</p>

This is a simulator for playing Hanabi, the wonderful, co-operative card game by Antoine Bauza. The simulator is run
from the command-line as:
```
python hanabi.py [-h] [-r] [-p P]
```
The default game is configured with two automated-players that follow a simple strategy of randomly playing,
discarding, or giving each other hints. As usual, the rainbow colored cards can be used as wild-cards.

The rainbow colored cards can also be added as their own sixth suit by setting the `-r` option. Additional players, or
players with different strategies, can be added to the game by setting the `-p` option and then specifying a string
of the strategies of each player to be added to the game. For example, to setup and run a simulation of three players
following arbitrary strategies `S1`, `S1`, and `S4`, run:
```
python hanabi.py -p 'S1, S1, S4'
```
Player strategies are specified in `player_strategies.py`; examples are provided therein for how these should be
formatted.

Adapted from BoardGameGeek (https://boardgamegeek.com/boardgame/98778/hanabi):
> Hanabi—named for the Japanese word for "fireworks" (written as 花火, ideograms for flower and fire, respectively)—is
> a cooperative game in which players try to create a fireworks show by placing the cards on the table in the right
> order. The card deck consists of five different colors of cards, numbered 1–5 in each color. Sounds easy, right?
> Well, not quite, as in this game you hold your cards so that they're visible only to the other players. To assist
> other players in playing a card, you must give them hints regarding the numbers or the colors of their cards.
> Players must act as a team to avoid errors and to finish the fireworks display before they run out of cards.

The full, official, game rules are provided in `hanabi-rulebook.pdf`.
