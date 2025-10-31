from typing import Dict, Tuple

class GameState:
    """
    Represents the state of a single DynastAI game session.
    """

    def __init__(self):
        self.power = 50
        self.stability = 50
        self.piety = 50
        self.wealth = 50
        self.reign_year = 1
        self.current_card = None
        self.card_history = []
        self.choice_history = []
        self.previous_reigns = []
        self.category_counts = {'power': 0, 'stability': 0, 'piety': 0, 'wealth': 0}

    def get_metrics(self) -> Dict[str, int]:
        """Return the current game metrics"""
        return {'power': self.power, 'stability': self.stability, 'piety': self.piety, 'wealth': self.wealth, 'reign_year': self.reign_year}

    def get_category_counts(self) -> Dict[str, int]:
        """Return the count of cards played by category"""
        return self.category_counts

    def record_card_play(self, card, choice):
        """Record a card play and choice"""
        if card and 'category' in card:
            category = card['category']
            if category in self.category_counts:
                self.category_counts[category] += 1
        self.card_history.append(card)
        self.choice_history.append(choice)
        self.reign_year += 1