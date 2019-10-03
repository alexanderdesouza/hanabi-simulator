import itertools
import random


class Card:
    
    def __init__(self, suit, value):

        self.player_id = None  # ID of the player currently in possession of this card; None otherwise

        self._true_suit = suit
        self._true_value = value

        self._suspected_suit = None
        self._suspected_value = None
    
    def suit(self, player_id):
        return self._suspected_suit if player_id == self.player_id else self._true_suit
    
    def value(self, player_id):
        return self._suspected_value if player_id == self.player_id else self._true_value
    
    def get_hint(self, **kwargs):
        self._suspected_suit = kwargs.get('suit', self._suspected_suit)
        self._suspected_value = kwargs.get('value', self._suspected_value)


class Deck:

    def __init__(self):

        self.CARD_VALUES_ARRAY = [1, 2, 3, 4, 5]
        self.CARD_FREQUENCY_ARRAY = [3, 2, 2, 2, 1]
        self.CARD_SINGLE_SUIT_ARRAY = [[v]*f for v, f in zip(self.CARD_VALUES_ARRAY, self.CARD_FREQUENCY_ARRAY)]
        self.CARD_SINGLE_SUIT_ARRAY = list(itertools.chain(*self.CARD_SINGLE_SUIT_ARRAY))  # flattens the above sequence
        self.CARD_SUIT_TYPE_ARRAY = ['Red', 'Yellow', 'Green', 'Blue', 'White', 'Rainbow']

        self.cards = [Card(suit, value) for value in self.CARD_SINGLE_SUIT_ARRAY for suit in self.CARD_SUIT_TYPE_ARRAY]

    def shuffle(self):
        self.cards = random.sample(self.cards, len(self.cards))

    def deal(self, number_of_cards, player_id):
        cards_to_deal = [self.cards.pop(0) for i in range(number_of_cards)]
        for c in cards_to_deal:
            c.player_id = player_id
        return cards_to_deal


class GameState:

    def __init__(self, player_count, rainbow_as_sixth=False, max_hints=8, max_mistakes=4):

        self.deck = Deck()

        self.piles = {suit: [] for suit in self.deck.CARD_SUIT_TYPE_ARRAY}
        if not rainbow_as_sixth:
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

    def print_game_state(self):
        """
        Prints the current game state to the terminal in a human readable format.
        """
        print(f'Game state at end of round-{self.game_round}:')
        print('\tPiles:')
        for suit, pile in self.piles.items():
            print(f'\t\t{suit}: {pile}')
        print(f'\tHints remaining: {self.hints}/{self.MAX_HINTS}')
        print(f'\tMistakes remaining: {self.mistakes}/{self.MAX_MISTAKES}')

    def _are_all_piles_complete(self):
        """
        Iterate over the self.piles object, and determine if the cards for a each suit have been played
        sequentially.
        """
        for suit, pile in self.piles.items():
            if [card.true_value for card in pile] != self.deck.CARD_VALUES_ARRAY:
                return False
        return True

    def evaluate_game_state(self, current_player):
        """
        Deal an additional card to a player if needed and check whether or not the deck has been expired
        or the players have collectively made too many mistakes. Then check the piles to see if they are
        complete.
        """
        if len(current_player.hand) < self.hand_size:
            if len(self.deck.cards) > 0:
                number_of_cards = self.hand_size-len(current_player.hand)
                current_player.hand += self.deck.deal(number_of_cards=number_of_cards, player_id=current_player.id)
            else:
                self.is_game_over = True

        if self.mistakes == 0:
            self.is_game_over = True

        if self._are_all_piles_complete():
            self.is_game_over = True
