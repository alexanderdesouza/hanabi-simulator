import random

from objects.game_objects import Card
from objects.player_objects import Player, Action, Hint


class Rando(Player):

    def __init__(self, id):
        super().__init__(id)

    def _strategy(self, players, game):
        """This strategy selects an action and action description completely at random. It's choices are bound by the
        current state of the game (e.g., it will not try to provide a hint if there are no more available hints). This
        method serves as a template for how a strategy is constructed.
        """
        available_actions = ['play', 'discard']
        if game.hints > 0:
            available_actions.append('hint')
        action = random.choice(available_actions)

        if action in ['play', 'discard']:
            # select one card to play or discard at random
            description = random.choice(self.hand)

        elif action in ['hint']:
            # give hint to another randomly selected player
            target_player_id = random.choice([player.id for player in players if player.id != self.id])
            
            # select a random card from their hand and randomly decide to give a hint about that card's suit or value
            selected_card = random.choice(players[target_player_id].hand)
            hint_type = 'value' \
                if not game.rainbow_as_sixth and selected_card.suit() == 'Rainbow' \
                else random.choice(['suit', 'value'])
            hint_value = getattr(selected_card, hint_type)()
            
            # assemble the choices into the action's description
            description = Hint(target_player_id, hint_type, hint_value)

        return Action(self.id, action, description)
