from abc import abstractmethod


class Hint:

    def __init__(self, player_id, hint_type, value):

        self.player_id = player_id
        self.hint_type = hint_type
        self.hint_value = value

    def __str__(self):
        """Return a string representation of the Hint object."""
        return f'Player-{self.player_id} learns which of their cards are {self.hint_value}(s).'


class Action:

    def __init__(self, player_id, action, description):

        self.player_id = player_id
        self.action = action
        self.description = description

    def __str__(self):
        """Return a string representation of the Action object."""
        return f'Player-{self.player_id}\'s action:\n\t{self.action.capitalize()}: {self.description.__str__()}'


class Player:

    def __init__(self, id):

        self.id = id
        self.hand = []

    @abstractmethod
    def _strategy(self, players, game):
        """Define the strategy of the player here: Under what conditions to play, discard, or provide hints to the other
        players.
        """
        pass

    def take_turn(self, players, game):
        """Called by the game engine to determine the current player's action. Which action is taken is determined
        following a call to the specified _strategy method.
        """
        action = self._strategy(players, game)

        return action
