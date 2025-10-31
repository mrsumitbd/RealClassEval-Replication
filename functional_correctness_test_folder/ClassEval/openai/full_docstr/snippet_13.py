
import random


class BlackjackGame:
    """
    This is a class representing a game of blackjack, which includes creating a deck, calculating the value of a hand,
    and determine the winner based on the hand values of the player and dealer.
    """

    def __init__(self):
        """
        Initialize the Blackjack Game with the attribute deck, player_hand and dealer_hand.
        While initializing deck attribute, call the create_deck method to generate.
        The deck stores 52 rondom order poker with the Jokers removed, format is ['AS', '2S', ...].
        player_hand is a list which stores player's hand cards.
        dealer_hand is is a list which stores dealer's hand cards.
        """
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []

    def create_deck(self):
        """
        Create a deck of 52 cards, which stores 52 rondom order poker with the Jokers removed.
        :return: a list of 52 rondom order poker with the Jokers removed, format is ['AS', '2S', ...].
        >>> black_jack_game = BlackjackGame()
        >>> black_jack_game.create_deck()
        ['QD', '9D', 'JC', 'QH', '2S', 'JH', '7D', '6H', '9S', '5C', '7H', 'QS', '5H',
        '6C', '7C', '3D', '10C', 'AD', '4C', '5D', 'AH', '2D', 'QC', 'KH', '9C', '9H',
        '4H', 'JS', '6S', '8H', '8C', '4S', '3H', '10H', '7S', '6D', '3C', 'KC', '3S',
        '2H', '10D', 'KS', '4D', 'AC', '10S', '2C', 'KD', '5S', 'JD', '8S', 'AS', '8D']
        """
        ranks = ['2', '3', '4', '5', '6', '7',
                 '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['S', 'H', 'D', 'C']
        deck = [rank + suit for rank in ranks for suit in suits]
        random.shuffle(deck)
        return deck

    def calculate_hand_value(self, hand):
        """
        Calculate the value of the poker cards stored in hand list according to the rules of the Blackjack Game.
        If the card is a digit, its value is added to the total hand value.
        Value of J, Q, or K is 10, while Aces are worth 11.
        If the total hand value exceeds 21 and there are Aces present, one Ace is treated as having a value of 1 instead of 11,
        until the hand value is less than or equal to 21, or all Aces have been counted as value of 1.
        :param hand: list
        :return: the value of the poker cards stored in hand list, a number.
        >>> black_jack_game.calculate_hand_value(['QD', '9D', 'JC', 'QH', 'AS'])
        40
        """
        total = 0
        aces = 0
        for card in hand:
            rank = card[:-1]  # everything except the suit
            if rank.isdigit():
                total += int(rank)
            elif rank in ('J', 'Q', 'K'):
                total += 10
            elif rank == 'A':
                total += 11
                aces += 1
        # Adjust for aces if bust
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def check_winner(self, player_hand, dealer_hand):
        """
        Determines the winner of a game by comparing the hand values of the player and dealer.
        rule:
        If both players have hand values that are equal to or less than 21, the winner is the one whose hand value is closer to 21.
        Otherwise, the winner is the one with the lower hand value.
        :param player_hand: list
        :param dealer_hand: list
        :return: the result of the game, only two certain str: 'Dealer wins' or 'Player wins'
        >>> black_jack_game.check_winner(['QD', '9D', 'JC', 'QH', 'AS'], ['QD', '9D', 'JC', 'QH', '2S'])
        'Player wins'
        """
        player_val = self.calculate_hand_value(player_hand)
        dealer_val = self.calculate_hand_value(dealer_hand)

        # Both <= 21: higher value wins
        if player_val <= 21 and dealer_val <= 21:
            if player_val > dealer_val:
                return 'Player wins'
            elif dealer_val > player_val:
                return 'Dealer wins'
            else:
                # tie case – dealer wins by default
                return 'Dealer wins'

        # One busts, the other doesn't
        if player_val <= 21 and dealer_val > 21:
            return 'Player wins'
        if dealer_val <= 21 and player_val > 21:
            return 'Dealer wins'

        # Both bust: lower value wins
        if player_val < dealer_val:
            return 'Player wins'
        else:
            return 'Dealer wins'
