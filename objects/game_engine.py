import random

from objects.game_objects import GameState
import player_types


class HanabiEngine:

    def __init__(self, players, rainbow_as_sixth, is_test=False):

        self.game = GameState(player_count=len(players), rainbow_as_sixth=rainbow_as_sixth)
        self.players = [getattr(getattr(player_types, p.lower()), p)(i) for i, p in enumerate(players)]
        
        self.is_test = is_test

    def _setup(self):
        """Shuffle the deck and deal each player a hand of cards."""
        self.game.deck.shuffle()
        for player in self.players:
            player.hand = self.game.deck.deal(number_of_cards=self.game.hand_size, player_id=player.id)

    def _update_game_objects(self, action):
        """Update the game and player objects based on the supplied Action."""
        if action.action == 'play':
            self.players[action.player_id].hand.remove(action.action_description)
            # TODO: logic around where this card was played
        elif action.action == 'discard':
            self.players[action.player_id].hand.remove(action.action_description)
            self.game.discard_pile.append(action.action_description)
        elif action.action in ['hint']:
            # TODO: logic around digesting the hint
            pass

    def run(self):
        """On their turn each player will look around to see what cards are visible in their companions' hands, make
        deductions based on the available information, and then take their turn (play, discard, or give a hint). The
        result of their turn is then evaluated to determine whether or not play proceeds.
        """
        self._setup()

        while not self.game.is_game_over:

            for player in self.players:

                action = player.take_turn(self.players, self.game)
                print(f'{action.__str__()}')

                self._update_game_objects(action)

                self.game.evaluate_game_state(player)

                if self.game.is_game_over:
                    break

            print(f'{self.game.__str__()}')
            self.game.game_round += 1

            if self.is_test:
                self.game.is_game_over = True

        print('Game over!')
