# -*- coding: utf-8 -*-
"""
Created on January 1 2020

@author: Hari Vidharth
"""


class Card:
    """
    Main card template to create all the card objects and returns the created card objects respectively.
    """

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def return_card(self):
        """
        Returns the created card object in the format CardRank_CardSuit.
        """
        return "{}_{}".format(self.value, self.suit)
