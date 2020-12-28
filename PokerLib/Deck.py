# -*- coding: utf-8 -*-
"""
Created on January 1 2020

@author: Hari Vidharth
"""

from PokerLib.Card import *
import random
class Deck:
    """
    Deck class builds the deck of cards consisting of card objects in straight
    and/or shuffle format.
    """

    def __init__(self):
        self.cards = []

    def build_deck(self):
        """
        Builds the deck of cards in straight format.
        """
        for suit in ["♣", "♦", "♥", "♠"]:
            for value in range(2, 15):
                if value == 11:
                    value = "J"
                elif value == 12:
                    value = "Q"
                elif value == 13:
                    value = "K"
                elif value == 14:
                    value = "A"
                self.cards.append(Card(value, suit))

    def shuffle_deck(self):
        """
        Shuffles the deck of cards in a random format.
        """
        for _ in range(0, len(self.cards)):
            random_card = random.randint(0, len(self.cards) - 1)
            (self.cards[_], self.cards[random_card]) = (
                self.cards[random_card], self.cards[_])

    def return_deck(self):
        """
        Returns the deck of card objects in a list in straight and/or shuffle
        format.
        """
        return_deck = []
        for _ in self.cards:
            return_deck.append(_.return_card())
        return return_deck
