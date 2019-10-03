class Player:

    def __init__(self, id, strategy):

        self.id = id
        self.hand = []
        self._strategy = strategy

    def take_turn(self, players, game):
        """
        Called by the game engine to determine the current player's action. Which action is taken is determined
        following a call to the specified _strategy method.
        """
        action = self._strategy(self, players, game)

        return action
