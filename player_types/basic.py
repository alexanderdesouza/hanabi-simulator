import random

from objects.game_objects import Card
from objects.player_objects import Player, Action, Hint


class Basic(Player):

    def __init__(self, id):
        super().__init__(id)

    def _play(self, players, game):
        """Play the lowest valued card possible from amongst those cards whose suit and value you know."""
        self.hand = self._arrange_hand_by_value(self.hand)

        expected_cards = [pile[-1] if pile else Card(suit, 1) for suit, pile in game.piles.items()]
        playable_cards = [card for card in self.hand \
                          if card.suit(is_visible=False) \
                          and card.value(is_visible=False) \
                          and card in expected_cards]

        if playable_cards:
            return playable_cards[0]
        else:
            return None

    def _discard(self, players, game):
        """Discards the lowest valued card in-hand compared to those that have already been played successfully, or the
        oldest card in-hand if forced to discard an unknown card. It is assumed that the player's hand has been
        arranged; see the _arrange_hand() method."""
        self.hand = self._arrange_hand_by_information(self.hand)

        for card in self.hand:
            for suit, pile in game.piles.items():
                if card.suit(is_visible=False) \
                   and card.value(is_visible=False) \
                   and card in pile:
                    return card
                elif (card.suit(is_visible=False)==suit \
                     or (card.suit(is_visible=False)=='Rainbow' and ~game.rainbow_as_sixth)) \
                     and not card.value(is_visible=False) \
                     and game._is_suit_complete(pile):
                    return card
                elif not card.suit(is_visible=False) \
                     and card.value(is_visible=False) \
                     and pile and card.value(is_visible=False) <= pile[-1].value():
                    return card
                elif not card.suit(is_visible=False) \
                     and not card.value(is_visible=False):
                    return card
        
        # discard the lowest valued card in hand if no other criteria has been met
        return self._arrange_hand_by_value(self.hand)[0]

    def _arrange_hand_by_information(self, hand):
        """Arrange a hand of cards in descending order of the amount of information known per card."""
        # arrange those cards for which all information about them is known
        known_cards = [card for card in hand
                       if card.suit(is_visible=False) and card.value(is_visible=False)]
        arranged_hand = sorted(known_cards, key=lambda c: c.value())

        # arrange those cards for which only the card's suit is known
        suit_only_cards = [card for card in hand if card.suit(is_visible=False) \
                                                    and not card.value(is_visible=False) \
                                                    and card not in arranged_hand]
        arranged_hand += suit_only_cards

        # arrange those cards for which only the value of the card is known
        value_only_cards = [card for card in hand if not card.suit(is_visible=False) \
                                                     and card.value(is_visible=False) \
                                                     and card not in arranged_hand]
        arranged_hand += sorted(value_only_cards, key=lambda c: c.value())

        # append all those remaining cards for which nothing about them is known
        arranged_hand += [card for card in hand if card not in arranged_hand]

        return arranged_hand

    def _arrange_hand_by_value(self, hand):
        """Arrange cards in hand by value for cards for which that is known."""
        return sorted(self.hand, key=lambda c: c.value(is_visible=False) if c.value(is_visible=False) is not None else 6)

    def _strategy(self, players, game):
        """This strategy prioritizes playing as follows: play a card if able; give a hint to another player if unable
        to play; discard if otherwise. Each of these options has its own set of priorities to optimize play.
        Will hint to the player that can play the lowest valued card of any suit if hinting.
        """
        for action in ['play', 'discard']:
            description = getattr(self, f'_{action}')(players, game)
            if description:
                break

        return Action(self.id, action, description)
