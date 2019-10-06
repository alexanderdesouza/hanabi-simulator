import random

from objects.game_objects import GameState
import player_types


class HanabiEngine:

    def __init__(self, players, rainbow_as_sixth):

        self.game = GameState(player_count=len(players), rainbow_as_sixth=rainbow_as_sixth)
        self.players = [getattr(getattr(player_types, p.lower()), p)(i) for i, p in enumerate(players)]

    def _setup(self):
        """Shuffle the deck and deal each player a hand of cards."""
        self.game.deck.shuffle()
        for player in self.players:
            player.hand = self.game.deck.deal(number_of_cards=self.game.hand_size, player_id=player.id)

    def run(self):
        """On their turn each player will look around to see what cards are visible in their companions' hands, make
        deductions based on the available information, and then take their turn (play, discard, or give a hint). The
        result of their turn is then evaluated to determine whether or not play proceeds.
        """
        self._setup()

        while not self.game.is_game_over:

            for player in self.players:

                print(f'Player-{player.id}\'s turn:')
                # TODO:
                action = player.take_turn(self.players, self.game)
                print(f'\t{action}')

                # TODO:
                # * update the game state based on the supplied action
                # * something like: self.game.update_game_state(action)

                self.game.evaluate_game_state(player)
                if self.game.is_game_over:
                    break

            self.game.print_game_state()
            self.game.game_round += 1

            self.game.is_game_over = True  # TODO: for testing only, causes a hard exit after one round

        print('Game over!')
