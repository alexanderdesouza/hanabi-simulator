from abc import abstractmethod


class Player:

    def __init__(self, id):

        self.id = id
        self.hand = []

    @abstractmethod
    def _strategy(self, players, game):
        """
        Define the strategy of the player here: Under what conditions to play, discard, or provide hints to the
        other players.
        """
        pass

    def take_turn(self, players, game):
        """
        Called by the game engine to determine the current player's action. Which action is taken is determined
        following a call to the specified _strategy method.
        """
        action = self._strategy(players, game)

        return action
