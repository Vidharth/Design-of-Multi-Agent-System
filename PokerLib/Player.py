# -*- coding: utf-8 -*-
"""
Created on January 1 2020

@author: Hari Vidharth
"""

class Player:
    """
    Class to manually add players to the poker game and draw and returns the
    players's hand cards.
    """

    def __init__(self):
        self.hand = []

    def draw_hand(self, _):
        """
        Draw cards from the deck for the player.
        """
        self.hand.append(_.pop())

    def return_hand(self):
        """
        Returns the player's hand cards.
        """
        return_hand = []
        for _ in self.hand:
            return_hand.append(_)
        return return_hand
