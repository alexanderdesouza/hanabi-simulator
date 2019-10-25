import random

from objects.game_objects import GameState, Card
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
            player.hand = self.game.deck.deal(number_of_cards=self.game.hand_size)

    def _resolve_play(self, action):
        """First, remove the selected card from the players hand. Then determine which pile to add it to, and confirm
        that the card is being added in the correct sequence. If not, tally a mistake as having been made.
        """
        played_card = action.description
        self.players[action.player_id].hand.remove(played_card)

        pile = self.game.piles[played_card.suit()]
        latest_card = None if len(pile)==0 else pile[-1]
        expected_card = Card(played_card.suit(), 1) if latest_card is None else Card(latest_card.suit(), latest_card.value()+1)

        if played_card == expected_card:  # TODO: resolve comparisons with Rainbow cards; need to target piles
            self.game.piles[played_card.suit()].append(played_card)
            print(f'\tCorrectly played {played_card} to {played_card.suit()} pile.')
        else:
            self.game.discard_pile.append(played_card)
            self.game.mistakes -= 1
            print(f'\tMistake: Expected {expected_card}. Card is discarded.')

    def _resolve_discard(self, action):
        """Discard the selected card to the discard_pile object list."""
        self.players[action.player_id].hand.remove(action.description)
        self.game.discard_pile.append(action.description)

    def _resolve_hint(self, action):
        """Reduce the number of remaining hints by 1. Then, update the target player's hand with the information
        granted by the hint.
        """
        self.game.hints -= 1

        target_player_id = action.description.player_id
        for card in self.players[target_player_id].hand:
            if getattr(card, action.description.hint_type)() == action.description.hint_value:
                card.apply_hint(action.description)

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

                getattr(self, '_resolve_'+action.action)(action)  # calls the relevant action-resolution method

                self.game.evaluate_game_state(player)

                if self.game.is_game_over:
                    break

            print(f'{self.game.__str__()}')
            self.game.game_round += 1

            if self.is_test:
                self.game.is_game_over = True

        print('Game over!')
