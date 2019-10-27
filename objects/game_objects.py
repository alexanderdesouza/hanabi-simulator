import itertools
import random


class Card:
    
    def __init__(self, suit, value):

        self._true_suit = suit
        self._true_value = value

        self._suspected_suit = None
        self._suspected_value = None

    def __eq__(self, other):
        """Allows comparison of two instances of a card based on their true suits and values."""
        return self._true_suit == other._true_suit and self._true_value == other._true_value

    def __str__(self, is_visible=True):
        """Return a string representation of the card."""
        return f'{self.suit(is_visible)}-{self.value(is_visible)}'

    def suit(self, is_visible=True):
        """Look at the suit of a given card. A player looking at another player's card sees the card's true suit,
        whereas a player looking at one of their own cards sees only what they suspect about the card via potential
        hints.
            :param: is_visible: whether or not the card face is visible to the current player
        """
        return self._true_suit if is_visible == True else self._suspected_suit

    def value(self, is_visible=True):
        """Look at the value of a given card. A player looking at another player's card sees the card's true value,
        whereas a player looking at one of their own cards sees only what they suspect about the card via potential
        hints.
            :param: is_visible: whether or not the card face is visible to the current player
        """
        return self._true_value if is_visible == True else self._suspected_value

    def apply_hint(self, description):
        """Set the suit or value of a card in a given player's hand, usually after receiving a hint."""
        # getattr(self, '_suspected_'+description.hint_type) = description.hint_value  # TODO: is this possible?
        if description.hint_type == 'suit':
            self._suspected_suit = description.hint_value
        if description.hint_type == 'value':
            self._suspected_value = description.hint_value


class Deck:

    def __init__(self):

        self.CARD_VALUES_ARRAY = [1, 2, 3, 4, 5]
        self.CARD_FREQUENCY_ARRAY = [3, 2, 2, 2, 1]
        self.CARD_SINGLE_SUIT_ARRAY = [[v]*f for v, f in zip(self.CARD_VALUES_ARRAY, self.CARD_FREQUENCY_ARRAY)]
        self.CARD_SINGLE_SUIT_ARRAY = list(itertools.chain(*self.CARD_SINGLE_SUIT_ARRAY))  # flatten the above sequence
        self.CARD_SUIT_TYPE_ARRAY = ['Red', 'Yellow', 'Green', 'Blue', 'White', 'Rainbow']

        self.cards = [Card(suit, value) for value in self.CARD_SINGLE_SUIT_ARRAY for suit in self.CARD_SUIT_TYPE_ARRAY]

    def shuffle(self):
        """Shuffle the deck of card objects."""
        self.cards = random.sample(self.cards, len(self.cards))

    def deal(self, number_of_cards):
        """Distribute a fixed number of cards to a specific player."""
        return [self.cards.pop(0) for i in range(number_of_cards)]


class GameState:

    def __init__(self, player_count, rainbow_as_sixth=False, max_hints=8, max_mistakes=3):

        self.rainbow_as_sixth = rainbow_as_sixth

        self.deck = Deck()

        self.piles = {suit: [] for suit in self.deck.CARD_SUIT_TYPE_ARRAY}
        if not self.rainbow_as_sixth:
            del self.piles['Rainbow']

        self.discard_pile = []

        self.MAX_HINTS = max_hints
        self.MAX_MISTAKES = max_mistakes

        self.hints = self.MAX_HINTS
        self.mistakes = self.MAX_MISTAKES

        self.player_count = player_count
        self.hand_size = 5 if self.player_count in [2, 3] else 4

        self.game_round = 0
        self.is_game_over = False

    def __str__(self):
        """Return a string representation of the current game state."""
        return f'Game state: Round-{self.game_round}:\n' \
         + f'\tPiles: {self._piles_str()} \n' \
         + f'\tLatest discard: {None if len(self.discard_pile)==0 else self.discard_pile[-1]} \n' \
         + f'\tHints remaining: {self.hints}/{self.MAX_HINTS}\n' \
         + f'\tMistakes remaining: {self.mistakes}/{self.MAX_MISTAKES}'

    def _piles_str(self):
        """Return a string representation of the self.piles object, which is a dict of lists."""
        return ' '.join([f'{suit}: {[p.__str__() for p in pile]}' for suit, pile in self.piles.items()])

    def _are_all_piles_complete(self):
        """Iterate over the self.piles object, and determine if the cards for a each suit have been played
        sequentially.
        """
        for suit, pile in self.piles.items():
            if [card.value() for card in pile] != self.deck.CARD_VALUES_ARRAY:
                return False
        return True

    def evaluate_game_state(self, current_player):
        """Deal an additional card to a player if needed and check whether or not the deck has been expired or the
        players have collectively made too many mistakes. Then check the piles to see if they are complete.
        """
        if len(current_player.hand) < self.hand_size:
            if len(self.deck.cards) > 0 and current_player.is_final_turn == False:
                number_of_cards = self.hand_size-len(current_player.hand)
                current_player.hand += self.deck.deal(number_of_cards=number_of_cards)
            elif len(self.deck.cards) == 0 and current_player.is_final_turn == False:
                current_player.is_final_turn = True
            elif len(self.deck.cards) == 0 and current_player.is_final_turn == True:
                self.is_game_over = True

        if self.mistakes == 0:
            self.is_game_over = True

        if self._are_all_piles_complete():
            self.is_game_over = True
