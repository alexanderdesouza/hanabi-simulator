import random

from player_objects.abstract_player import Player


class Rando(Player):

    def __init__(self, id):
        super().__init__(id)

    def _strategy(self, players, game):
        """
        This strategy selects an action and action description completely at random. It's choices are bound only by the
        current state of the game (e.g., it will not try to provide a hint if there are no more available hints).

        For the 'play' and 'discard' actions, the action description must be a single integer representing the position of
        the card to be played or discarded in the acting player's hand.

        For the 'hint' action, the action description consists of a dict whose key is the integer player-ID to whom the
        hint is being given. The value is another dict, whose own key is a string, either a number or color (represented by
        a single letter), and the value is a list of integers representing the position of the cards in the other player's
        hand to which the hint applies.

        Use this method as a template for how a strategy is constructed and for how the return object must be constructed.
        """
        available_actions = ['play', 'discard']
        # if game.hints > 0:
        #     available_actions.append('hint')
        action = random.choice(available_actions)

        if action in ['play', 'discard']:
            # select one card to play or discard at random
            action_description = random.choice(self.hand)

        elif action in ['hint']:
            # give hint to another player selected at random
            player_id_to_get_hint = random.choice([player.id for player in players if player.id != self.id])
            
            # select a random card from their hand and randomly decide to give a hint about that card's suit or value
            card = random.choice(players[player_id_to_get_hint].hand)
            if not game.rainbow_as_sixth and card.suit(self.id) == 'Rainbow':
                hint = card.value(self.id)
            else:
                hint = random.choice([card.suit(self.id), card.value(self.id)])
            
            # assemble the choices into the action_description, which for 
            action_description = {}  # TODO: Finish writing action description for hinting

        return {action: action_description}
