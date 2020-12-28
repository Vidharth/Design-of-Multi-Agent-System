# -*- coding: utf-8 -*-
"""
Created on January 1 2020
@author: Hari Vidharth
"""


import itertools


class Poker:
    """
    Class defining poker rules, takes the player cards and the community cards
    as input for the class to be used by the individual check functions.
    """

    def __init__(self, communitycards, *player_cards):
        self.cardclass = ["♣", "♦", "♥", "♠"]
        self.rank = ["2", "3", "4", "5", "6", "7", "8", "9",
                "10", "J", "Q", "K", "A"]
        self.rrank = ["10", "J", "Q", "K", "A"]
        self.playercards = []
        self.communitycards = communitycards
        for items in player_cards:
            for item in items:
                self.playercards.append(item)
        # print(self.playercards)
        # print(self.communitycards)

    def royal_flush(self):
        """
        To check for a flush in the set, Takes the player cards and community
        cards as input, and checks for a flush among the players, and returns
        the players whose cards matches. Does not return any cards if
        multiple flush cards or no flush cards are detected.
        Also checks for the value of the cards are according to the self.rrank
        ["10", "J", "Q", "K", "A"] returns the player whose cards matches,
        combing it with the above flush result to check for a ROYAL FLUSH,
        returns the player if winner else returns None and moves to the next
        check function.
        """
        suit = []
        playercommunitycards = []
        player = []
        flushcount = []
        playercount = []
        flushplayercount = []
        for item in self.playercards:
            playercommunitycards.append(item+self.communitycards)
        # print(playercommunitycards)
        for items in playercommunitycards:
            for item in items:
                player.append(item.split("_")[1])
            suit.append(player)
            player = []
        # print(suit)
        for items in self.cardclass:
            for item in suit:
                flushcount.append(item.count(items))
            # print(flushcount)
            for position, item in enumerate(flushcount):
                if item >= 5:
                    playercount.append(position)
            # print(playercount)
            flushplayercount.append(playercount)
            playercount = []
            flushcount = []
        # print(flushplayercount)
        count = 0
        value = []
        for items in playercommunitycards:
            for item in items:
                player.append(item.split("_")[0])
            value.append(player)
            player = []
        # print(value)
        royal = []
        for pos, items in enumerate(value):
            for ranking in self.rrank:
                if ranking in items:
                    count += 1
            royal.append((pos, count))
            count = 0
        # print(royal)
        new_royal = []
        for items in royal:
            if items[1] == 5:
                new_royal.append(items[0])
        # print(new_royal)
        final_royal = []
        for item in new_royal:
            for items in flushplayercount:
                if item in items:
                    final_royal.append(item)
        for items in new_royal:
            return items

    def straight_flush(self):
        """
         To check for a flush in the set, Takes the player cards and community
         cards as input, and checks for a flush among the players, and returns
         the players whose cards matches. Does not return any cards if
         multiple flush cards or no flush cards are detected.
         Also checks for the value of the cards are according to the straight
         self.rank returns the player whose cards matches, combing it with the above
         flush result to check for a STRAIGHT FLUSH, returns the player if
         winner else returns None and moves to the next check function!
         """
        suit = []
        playercommunitycards = []
        player = []
        flushcount = []
        playercount = []
        flushplayercount = []
        for item in self.playercards:
            playercommunitycards.append(item+self.communitycards)
        # print(playercommunitycards)
        for items in playercommunitycards:
            for item in items:
                player.append(item.split("_")[1])
            suit.append(player)
            player = []
        # print(suit)
        for items in self.cardclass:
            for item in suit:
                flushcount.append(item.count(items))
            # print(flushcount)
            for position, item in enumerate(flushcount):
                if item >= 5:
                    playercount.append(position)
            # print(playercount)
            flushplayercount.append(playercount)
            playercount = []
            flushcount = []
        # print(flushplayercount)
        value = []
        for items in playercommunitycards:
            for item in items:
                player.append(item.split("_")[0])
            value.append(player)
            player = []
        # print(value)
        card_position = []
        playerp = []
        for items in value:
            for position, item in enumerate(self.rank):
                if item in items:
                    playerp.append(position)
            card_position.append(playerp)
            playerp = []
        # print(card_position)
        groups = []
        group = []
        for items in card_position:
            value1 = value2 = items[0]
            for item in items[1:]:
                if item == value2 + 1:
                    value2 = item
                else:
                    groups.append(value1 if value1 == value2 else
                                  (value1, value2))
                    value1 = value2 = item
            groups.append(value1 if value1 == value2 else (value1, value2))
            group.append(groups)
            groups = []
        # print(group)
        new_group = []
        player = []
        for items in group:
            for item in items:
                if type(item) is tuple:
                    player.append(item)
            new_group.append(player)
            player = []
        # print(new_group)
        straightplayer = []
        for pos, items in enumerate(new_group):
            if len(items) != 0:
                if items[0][-1] - items[0][0] == 4:
                    straightplayer.append(pos)
        # print(straightplayer)
        for item in straightplayer:
            for items in flushplayercount:
                if item in items:
                    return item
                else:
                    return None

    def four_of_a_kind(self):
        """
         To check for a four of a kind in the set, Takes the player cards and
         community cards as input, and checks for a four of a kind among the
         players, and returns the players whose cards matches. Does not return
         any cards if multiple or no four of a kinds are detected. Returns the
         player if winner else returns None and moves to the next check
         function.
         """
        value = []
        player = []
        playercommunitycards = []
        player = []
        for item in self.playercards:
            playercommunitycards.append(item+self.communitycards)
        # print(playercommunitycards)
        for items in playercommunitycards:
            for item in items:
                player.append(item.split("_")[0])
            value.append(player)
            player = []
        # print(value)
        new_value = []
        player = []
        for items in value:
            for value1, value2, value3, value4 in itertools.combinations(
                    items, 4):
                player.append((value1, value2, value3, value4))
            new_value.append(player)
            player = []
        four_of_a_kind = []
        player = []
        for items in new_value:
            for item in items:
                if (item[0] == item[1] and item[1] == item[2] and item[2] ==
                        item[3]):
                    player.append((item[0], item[1], item[2], item[3]))
            four_of_a_kind.append(player)
            player = []
        # print(four_of_a_kind)
        new_four_of_a_kind = []
        for pos, items in enumerate(four_of_a_kind):
            if len(items) >= 1:
                new_four_of_a_kind.append(pos)
        # print(new_four_of_a_kind)
        if len(new_four_of_a_kind) == 1:
            return new_four_of_a_kind[0]
        else:
            return None

    def full_house(self):
        """
        To check for a three of a kind in the set, Takes the player cards and
        community cards as input, and checks for a three of a kind among the
        players, and returns the players whose cards matches. Does not return
        any cards if multiple or no three of a kinds are detected. Returns the
        player if winner else returns None.
        Also to check for a pair in the set, Takes the player cards and
        community cards as input, and checks for the pairs among the
        players and returns the players value. Does not return any cards if
        multiple or no pair cards are detected, it is then directed to the
        next check function.
        """
        value = []
        player = []
        playercommunitycards = []
        player = []
        for item in self.playercards:
            playercommunitycards.append(item+self.communitycards)
        # print(playercommunitycards)
        for items in playercommunitycards:
            for item in items:
                player.append(item.split("_")[0])
            value.append(player)
            player = []
        # print(value)
        new_value = []
        player = []
        for items in value:
            for value1, value2, value3 in itertools.combinations(items, 3):
                player.append((value1, value2, value3))
            new_value.append(player)
            player = []
        three_of_a_kind = []
        player = []
        for items in new_value:
            for item in items:
                if item[0] == item[1] and item[1] == item[2]:
                    player.append((item[0], item[1], item[2]))
            three_of_a_kind.append(player)
            player = []
        # print(three_of_a_kind)
        new_three_of_a_kind = []
        for pos, items in enumerate(three_of_a_kind):
            if len(items) >= 1:
                new_three_of_a_kind.append(pos)
        # print(new_three_of_a_kind)
        playervalue = []
        communityvalue = []
        player = []
        for items in self.playercards:
            for item in items:
                player.append(item.split("_")[0])
            playervalue.append(player)
            player = []
        for item in self.communitycards:
            communityvalue.append(item.split("_")[0])
        # print(playervalue)
        # print(communityvalue)
        new_value = []
        player = []
        for pos, items in enumerate(playervalue):
            if items[0] == items[1]:
                player.append([pos, items[0]])
            for item in items:
                if item in communityvalue:
                    player.append([pos, item])
            new_value.append(player)
            player = []
        # print(new_value)
        pair_rank = []
        player = []
        for items in new_value:
            for item in items:
                for pos, ranking in enumerate(self.rank):
                    if ranking == item[1]:
                        player.append([pos, item])
                pair_rank.append(player)
                player = []
        pair_rank = sorted(pair_rank)
        # print(pair_self.rank)
        count = 0
        playercount = []
        player = []
        for items in pair_rank:
            for item in new_three_of_a_kind:
                if item == items[0][1][0]:
                    count += 1
            player.append(count)
            playercount.append(player)
            player = []
            count = 0
        # print(playercount)
        if len(playercount) == 1:
            for pos, items in enumerate(playercount):
                return pos
        else:
            return None

    def straight(self):
        """
         Checks for the value of the cards are according to the straight
         self.rank and returns the player whose cards matches, to check for a
         STRAIGHT, returns the player if winner else returns None and moves
         to the next check function.
         """
        playercommunitycards = []
        player = []
        for item in self.playercards:
            playercommunitycards.append(item+self.communitycards)
        # print(playercommunitycards)
        value = []
        for items in playercommunitycards:
            for item in items:
                player.append(item.split("_")[0])
            value.append(player)
            player = []
        # print(value)
        card_position = []
        playerp = []
        for items in value:
            for position, item in enumerate(self.rank):
                if item in items:
                    playerp.append(position)
            card_position.append(playerp)
            playerp = []
        # print(card_position)
        groups = []
        group = []
        for items in card_position:
            value1 = value2 = items[0]
            for item in items[1:]:
                if item == value2 + 1:
                    value2 = item
                else:
                    groups.append(value1 if value1 == value2 else
                                  (value1, value2))
                    value1 = value2 = item
            groups.append(value1 if value1 == value2 else (value1, value2))
            group.append(groups)
            groups = []
        # print(group)
        new_group = []
        player = []
        for items in group:
            for item in items:
                if type(item) is tuple:
                    player.append(item)
            new_group.append(player)
            player = []
        # print(new_group)
        straightplayer = []
        for pos, items in enumerate(new_group):
            if len(items) != 0:
                if items[0][-1] - items[0][0] == 4:
                    straightplayer.append(pos)
        # print(straightplayer)
        if len(straightplayer) == 1:
            return straightplayer[0]
        else:
            return None

    def flush(self):
        """
        To check for a flush in the set, Takes the player cards and community
        cards as input, and checks for a flush among the players, and returns
        the players and flush cards value. Does not return any cards if
        multiple flush cards or no flush cards are detected, and is then
        directed to the next check function.
        """
        suit = []
        playercommunitycards = []
        player = []
        flushcount = []
        playercount = []
        flushplayercount = []
        for item in self.playercards:
            playercommunitycards.append(item+self.communitycards)
        # print(playercommunitycards)
        for items in playercommunitycards:
            for item in items:
                player.append(item.split("_")[1])
            suit.append(player)
            player = []
        # print(suit)
        for items in self.cardclass:
            for item in suit:
                flushcount.append(item.count(items))
            # print(flushcount)
            for position, item in enumerate(flushcount):
                if item > 5:
                    playercount.append(position)
            # print(playercount)
            flushplayercount.append(playercount)
            playercount = []
            flushcount = []
        # print(flushplayercount)
        finalflush = []
        for items in flushplayercount:
            if len(items) == 1:
                finalflush.append(items)
        # print(finalflush)
        if len(finalflush) != 0:
            for items in finalflush:
                if len(items) == 1:
                    return items[0]
                else:
                    return None

    def three_of_a_kind(self):
        """
         To check for a three of a kind in the set, Takes the player cards and
         community cards as input, and checks for a three of a kind among the
         players, and returns the players whose cards matches. Does not return
         any cards if multiple or no three of a kinds are detected. Returns the
         player if winner else returns None and moves to the next check
         function.
         """
        value = []
        player = []
        playercommunitycards = []
        player = []
        for item in self.playercards:
            playercommunitycards.append(item+self.communitycards)
        # print(playercommunitycards)
        for items in playercommunitycards:
            for item in items:
                player.append(item.split("_")[0])
            value.append(player)
            player = []
        # print(value)
        new_value = []
        player = []
        for items in value:
            for value1, value2, value3 in itertools.combinations(items, 3):
                player.append((value1, value2, value3))
            new_value.append(player)
            player = []
        three_of_a_kind = []
        player = []
        for items in new_value:
            for item in items:
                if item[0] == item[1] and item[1] == item[2]:
                    player.append((item[0], item[1], item[2]))
            three_of_a_kind.append(player)
            player = []
        # print(three_of_a_kind)
        new_three_of_a_kind = []
        for pos, items in enumerate(three_of_a_kind):
            if len(items) >= 1:
                new_three_of_a_kind.append(pos)
        # print(new_three_of_a_kind)
        if len(new_three_of_a_kind) == 1:
            return new_three_of_a_kind[0]
        else:
            return None

    def two_pair(self):
        """
        To check for a two pair in the set, Takes the player cards and
        community cards as input, and checks for the two pairs among the
        players and returns the players value. Does not return any cards if
        multiple or no two pair cards are detected, it is then directed to the
        next check function.
        """
        playervalue = []
        communityvalue = []
        player = []
        for items in self.playercards:
            for item in items:
                player.append(item.split("_")[0])
            playervalue.append(player)
            player = []
        for item in self.communitycards:
            communityvalue.append(item.split("_")[0])
        # print(playervalue)
        # print(communityvalue)
        new_value = []
        player = []
        for pos, items in enumerate(playervalue):
            if items[0] == items[1]:
                player.append([pos, items[0]])
            for item in items:
                if item in communityvalue:
                    player.append([pos, item])
            new_value.append(player)
            player = []
        # print(new_value)
        final_value = []
        for items in new_value:
            if len(items) == 2:
                final_value.append(items[0][0])
        # print(final_value)
        if len(final_value) == 1:
            return final_value[0]
        else:
            return None

    def pair(self):
        """
        To check for the highest pair in the set, Takes the player cards and
        community cards as input, and checks for the pairs among the
        players and returns the players value. Does not return any cards if
        multiple or no pair cards are detected, it is then directed to the
        next check function.
        """
        playervalue = []
        communityvalue = []
        player = []
        for items in self.playercards:
            for item in items:
                player.append(item.split("_")[0])
            playervalue.append(player)
            player = []
        for item in self.communitycards:
            communityvalue.append(item.split("_")[0])
        # print(playervalue)
        # print(communityvalue)
        new_value = []
        player = []
        for pos, items in enumerate(playervalue):
            if items[0] == items[1]:
                player.append([pos, items[0]])
            for item in items:
                if item in communityvalue:
                    player.append([pos, item])
            new_value.append(player)
            player = []
        # print(new_value)
        pair_rank = []
        player = []
        for items in new_value:
            for item in items:
                for pos, ranking in enumerate(self.rank):
                    if ranking == item[1]:
                        player.append([pos, item])
                pair_rank.append(player)
                player = []
        pair_rank = sorted(pair_rank)
        # print(pair_self.rank)
        if len(pair_rank) == 1:
            return pair_rank[0][0][1][0]
        elif len(pair_rank) > 1:
            if pair_rank[-2][0][0] != pair_rank[-1][0][0]:
                return pair_rank[-1][0][1][0]
            else:
                return None
        else:
            return None

    def high_card(self):
        """
        To check the High card in the set, Takes the player cards as input
        (Just the players cards and excluding the community cards.), and checks
        for the high card among the players, and returns the players and high
        cards value. Does not return any cards if multiple high cards are
        detected, As the final check condition the loot is split equally among
        the winners with matching multiple high cards.
        """
        player = []
        value = []
        card_rank = []
        final_card_rank = []
        for items in self.playercards:
            for item in items:
                player.append(item.split("_")[0])
            value.append(player)
            player = []
        # print(value)
        for items in value:
            value1, value2 = items[0], items[1]
            for position, item in enumerate(self.rank):
                if item == value1:
                    player.append((position, value1))
                elif item == value2:
                    player.append((position, value2))
            if len(player) > 1:
                if player[0][0] > player[1][0]:
                    card_rank.append(player[0])
                elif player[0][0] < player[1][0]:
                    card_rank.append(player[1])
            else:
                card_rank.append(player[0])
            player = []
        # print(card_self.rank)
        new_card_rank = sorted(card_rank)
        # print(new_card_self.rank)
        for position, item in enumerate(card_rank):
            if new_card_rank[-1] == item:
                final_card_rank.append((position, item))
        # print(final_card_self.rank)
        if len(final_card_rank) == 1:
            return final_card_rank[0][0]
        else:
            return None
