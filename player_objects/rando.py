import random

from player_objects.abstract_player import Player


class Rando(Player):

    def __init__(self, id):
        super().__init__(id)

    def _strategy(self, players, game):
        """This strategy selects an action and action description completely at random. It's choices are bound by the
        current state of the game (e.g., it will not try to provide a hint if there are no more available hints). This
        method serves as a template for how a strategy is constructed.
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
