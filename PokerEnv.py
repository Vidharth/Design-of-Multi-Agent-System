# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 21:37:28 2019

@author: battu
"""
# The code for implementing the Cards, decks and flushes.
from PokerLib.Card import *
from PokerLib.Deck import *
from PokerLib.Player import *
from PokerLib.PokerRules import *

import numpy as np
import math
import random


# from PokerScore import *
# Defined Player Attributes that help in decision making
#Each score ranges from 0-100
default_attributes = {'caution':50,'greed':50,'bluff':50}

#List of actions available to players each round
action_dictionary = {'pre_flop':['CALL','RAISE','FOLD'],'flop':['CHECK','BET','RAISE','FOLD'],'turn':['CHECK','BET','RAISE','FOLD'],'river':['CHECK','BET','RAISE','FOLD']}

emotion_dictionary = {0:'fear',1:'happy',2:'no-emotion',3:'anger',4:'contempt',5:'normal'}
#Ranking used for score function
ranks = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':11,'Q':12,'K':13,'A':14}
#Gym Environment for Poker
class PokerEnvironment(object):
    '''
    A list of 'agents' is given to the environment as the game begins.
    A deck is built and randomly shuffled.
    Rest are initialization variables
    
    self.stage tells which round the game is currently in
    self.minimum_bet_amount is the minimum amount of bet a player has to place if he wants to bet.
    self.bets_placed is the array of bets placed by the player.
    self.folden_indexs tells which players have folded.
    self.pot is the total amount of bets placed by all players till the current round.
    self.community_cards is the community cards visible to agents till the current round.
    self.game_stats gives the game stats at the end of game
    
    '''
    def __init__(self,players_list):
        self.n_players = len(players_list)
        self.player_objects = players_list
        
        #Place to delcare or use emotions for dealer, if any.
        self.shuffler_emotion = None
        
        self.deck_object = Deck()
        self.deck_object.build_deck()
        self.player_emotions = []
        
        for i in range(random.randint(1,5)):
            self.deck_object.shuffle_deck()
        self.main_deck = self.deck_object.return_deck()
        self.stage = None
        self.minimum_bet_amount = 10
        self.bets_placed = []
        self.pointer = 0
        self.folden_indexes = []
        self.pot = 0
        self.community_cards = []
        self.game_done=0
        
        self.game_stats = {'players':[],'winner':0,'win_moves':0,'win_amount':0,'win_hand':0,'win_emotion':0,'win_e_power':0,'win_e_num':0}
        pass
    
    def reset(self):
        #Make each player draw 2 cards from deck, or deal 2 cards to each player.
        for i in range(self.n_players):    
            self.player_objects[i].player.draw_hand(self.main_deck)
            self.player_objects[i].player.draw_hand(self.main_deck)
            self.player_objects[i].hand = self.player_objects[i].player.return_hand()    
        pass
     
    #Tell each agent object the current stage of the game, this is a simple message function
    def set_stage(self):
        for i in range(self.n_players):
            self.player_objects[i].set_stage(self.stage)
                
    #Remove folden players form list
    def del_folden_index(self,a,b,index):
            del a[index]
            try:
                del b[index]
            except Exception as e:
                pass
            return a,b
        
    # This function interacts with agent for each round depending on the decision they make. 
    def get_player_actions(self):
        if self.game_done==1:
            return
        action_list = action_dictionary[self.stage]
        
        #Loop over each player
        for i in range(self.n_players):
            
            #Declare winner if all players folded
            if len(self.folden_indexes)+1 == self.n_players:
                for x in range(self.n_players):
                    if x not in self.folden_indexes:
                        self.winner(x)
            if self.game_done==1:
                break
            if i in self.folden_indexes:
                continue
            
            #Get action of each agent, send information to each agent
            if self.stage == 'pre_flop':
                action,raise_amount = self.player_objects[i].make_decision(self.bets_placed,i,None,self.minimum_bet_amount)
            else:
                action,raise_amount = self.player_objects[i].make_decision(self.bets_placed,i,self.community_cards,self.minimum_bet_amount)  
            action_str = action_list[action]
            if self.player_objects[i].current_coins<=0:
                action_str = "FOLD"
            self.player_objects[i].actions_taken[self.stage].append(action_str)
            
            #Based on the stage/round, change parameters of the game.
            if self.stage == 'flop' or self.stage == 'turn' or self.stage == 'river':
                if action_str == "CHECK":
                    try:
                        if self.bets_placed[i-1] > self.bets_placed[i]:
                            i=i-1
                            continue
                        else:
                            pass
                    except Exception as e:
                        if self.bets_placed[-1] > self.bets_placed[i]:
                            i=len(self.bets_placed)-1
                            continue
                        else:
                            pass
                if action_str == "BET":   
                    if len(self.bets_placed)>0:        
                        bet_amount  = self.minimum_bet_amount
                        self.pointer = i
                        try:
                            self.bets_placed[i] = bet_amount
                        except Exception as e:
                            self.bets_placed.append(bet_amount)
                        self.player_objects[i].current_coins -= bet_amount
                        self.minimum_bet_amount = bet_amount
                    else:
                        self.bets_placed.append(self.minimum_bet_amount)
                        self.player_objects[i].current_coins -= self.minimum_bet_amount
                        
                if action_str == "RAISE":
                    if len(self.bets_placed)>0:
                        bet_amount = raise_amount
                        self.pointer = i
                        try:
                            self.bets_placed[i] = bet_amount
                        except Exception as e:
                            self.bets_placed.append(bet_amount)
                        self.player_objects[i].current_coins -= bet_amount
                        self.minimum_bet_amount = bet_amount  
                    else:
                        self.bets_placed.append(raise_amount)
                        self.minimum_bet_amount = raise_amount 
                        self.player_objects[i].current_coins -= self.minimum_bet_amount  
                if action_str == "FOLD":
                    self.folden_indexes.append(i)
                    
                    try:
                        self.pot+=self.bets_placed[i]
                        self.bets_placed[i] = 0
                    except:
                        self.bets_placed.append(0)
                
            # Stage Preflop
            if self.stage == 'pre_flop':
                
                if action_str == 'CALL':   
                    if len(self.bets_placed)>0:     
                        bet_amount  = self.minimum_bet_amount
                        self.pointer = i
                        try:
                            self.bets_placed[i] = bet_amount
                        except Exception as e:
                            self.bets_placed.append(bet_amount)
                        self.player_objects[i].current_coins -= bet_amount
                        self.minimum_bet_amount = bet_amount     
                    else:
                        self.bets_placed.append(self.minimum_bet_amount)
                        self.player_objects[i].current_coins -= self.minimum_bet_amount
                if action_str == "RAISE":
                    if len(self.bets_placed)>0:
                        bet_amount = raise_amount
                        self.pointer = i
                        try:
                            self.bets_placed[i] = bet_amount
                        except Exception as e:
                            self.bets_placed.append(bet_amount)
                        self.player_objects[i].current_coins -= bet_amount
                        self.minimum_bet_amount = bet_amount   
                    else:
                        self.bets_placed.append(raise_amount)
                        self.minimum_bet_amount = raise_amount 
                        self.player_objects[i].current_coins -= self.minimum_bet_amount
                if action_str == "FOLD":
                    self.folden_indexes.append(i)
                    try:
                        self.pot+=self.bets_placed[i]
                        self.bets_placed[i] = 0
                    except:
                        self.bets_placed.append(0)
                        
        #Check if game is done, or else get maximum bet
        if self.game_done==1:
            return
        try:
            maximum = max(self.bets_placed)
        except:
            print("all folded")
            return
        
        #Rerun the round if all player bets are not the same.
        temp = self.bets_placed.copy()
        not_safe=0
        for x in range(len(temp)):
            if temp[x]==0:
                continue
            if temp[x]!=maximum:
                not_safe=1
                break
        if not_safe==1:
            self.get_player_actions()
   
    # High level implementation of pre flop round. 
    def pre_flop(self):
        
        self.stage = 'pre_flop'
        self.set_stage()
        self.get_player_actions()
        self.pot += sum(self.bets_placed)
        for i in range(len(self.bets_placed)):
            self.bets_placed[i] = 0  
        self.minimum_bet_amount = 10
        pass
    
    
    #High level implementation of Flop round.
    def flop(self):
        if self.game_done==1:
            return
        self.dealer = Player()
        self.dealer.draw_hand(self.main_deck)
        self.dealer.draw_hand(self.main_deck)
        self.dealer.draw_hand(self.main_deck)
        self.dealer.hand = self.dealer.return_hand()
        self.community_cards = self.dealer.hand
        
        self.stage = 'flop'
        self.set_stage()
        self.get_player_actions()
        self.pot += sum(self.bets_placed)
        for i in range(len(self.bets_placed)):
            self.bets_placed[i] = 0  
        self.minimum_bet_amount = 10
        pass
    
    #High level implementation of Turn round
    def turn(self):
        if self.game_done==1:
            return
        self.dealer.draw_hand(self.main_deck)
        self.community_cards = self.dealer.hand
        
        self.stage = 'turn'
        self.set_stage()
        self.get_player_actions()
        self.pot += sum(self.bets_placed)
        for i in range(len(self.bets_placed)):
            self.bets_placed[i] = 0    
        self.minimum_bet_amount = 10
        pass
    
    #High level implementation of River round.
    def river(self):
        if self.game_done==1:
            return
        self.dealer.draw_hand(self.main_deck)
        self.community_cards = self.dealer.hand
        
        self.stage = 'river'
        self.set_stage()
        self.get_player_actions()
        self.pot += sum(self.bets_placed)
        for i in range(len(self.bets_placed)):
            self.bets_placed[i] = 0
        self.minimum_bet_amount = 10
        pass
    
    #Shows hand cards, for debugging
    def show(self):
        for i in range(self.n_players):
            print(self.player_objects[i].hand)

    #The showdown where player hands are displayed, the winner is also declared here
    def showdown(self):
        self.stage='showdown'
        if self.game_done==1:
            return
        hands = []
        hand_indexes=[]
        for i in range(self.n_players):
            if i not in self.folden_indexes:
                hand_indexes.append(i)
                hands.append(list(self.player_objects[i].hand))
        
        #Use Poker API to get the best player hand
        p = Poker(self.community_cards,hands)
        rf = p.royal_flush()
        sf = p.straight_flush()
        fof = p.four_of_a_kind()
        fh = p.full_house()
        fl = p.flush()
        st = p.straight()
        tof = p.three_of_a_kind()
        tp = p.two_pair()
        pf = p.pair()
        hc = p.high_card()
        lst = [rf,sf,fof,fh,fl,st,tof,tp,pf,hc]
        
        #Complete the game
        for i in lst:
            if i!=None and self.game_done==0:
                self.winner(hand_indexes[i])
                break
        if self.game_done==0:
            self.winner(random.sample(hand_indexes,1)[0])
        pass
      
    #Record End game stats
    def winner(self,player_id):
        self.game_done=1
        for i in range(len(self.player_objects)):
            arr = [i,emotion_dictionary[self.player_objects[i].emotion],self.player_objects[i].emotion_power,self.player_objects[i].hand]
            self.game_stats['players'].append(arr)
        self.game_stats['winner'] = player_id
        self.game_stats['win_moves'] = self.player_objects[player_id].actions_taken
        self.game_stats['win_amount'] = self.pot
        self.game_stats['win_hand'] = self.player_objects[player_id].hand
        self.game_stats['community_cards'] = self.community_cards
        self.game_stats['win_emotion'] = emotion_dictionary[self.player_objects[player_id].emotion]
        self.game_stats['win_e_power'] = self.player_objects[player_id].emotion_power
        
        self.game_stats['win_e_num'] = self.player_objects[player_id].emotion
        self.game_stats['last_round'] = self.stage
        self.game_stats['debt'] = self.player_objects[player_id].current_coins
        pass


class Agent(object):
    '''Agent Class where each agent object is implemented, each agent object participates in the
    poker environment.
    Some attributes are:
    self.current_coins gives the coins that the agent is holding
    self.hand gives the current hand of the player
    self.stage stores the current stage of the game, (preflop,flop etc) in order to make decisions
    self.actions_taken stores the action history of each agent.
    self.available_actions gives the available actions for an agent in the particular self.stage
    self.emotion_power gives the power of the emotion of the agent
    self.emotion gives the current emotion of the agent
    self.player_attributes gives the attributes of the agent.
    
    
    '''
    #Each agent takes in the player object from PokerGame package and the amount of coins he has in the beginning.
    def __init__(self,player_object,coins,emotion,power):
        self.current_coins = coins
        self.player = player_object
        self.hand = None
        self.stage = None
        self.actions_taken = {}
         
        #The actions for each player
        self.available_actions = None
        self.emotion_power = power

        self.emotion = emotion
        self.player_attributes = default_attributes.copy()
        self.set_attributes()
    
    
    #Sets the stage and available actions of the agent. Received from the environment.
    def set_stage(self,stage):
        self.stage = stage
        self.available_actions = action_dictionary[self.stage]
        self.actions_taken[self.stage] = []
    
    #Here the attributes of each player are set based on their state of emotion.
    #The formulae below are used to initialize attribute values
    def set_attributes(self):
        base_value = 50
        if emotion_dictionary[self.emotion] == 'fear':
                    self.player_attributes['caution'] += self.emotion_power*base_value
                    self.player_attributes['greed'] -= self.emotion_power*(base_value/2)            
        if emotion_dictionary[self.emotion] == 'happy':
                    self.player_attributes['bluff'] += self.emotion_power*base_value
                    self.player_attributes['greed'] += self.emotion_power*(base_value/2)
                    self.player_attributes['caution'] -= self.emotion_power*(base_value/2)
        if emotion_dictionary[self.emotion] == 'no_emotion':
                    self.player_attributes['caution'] = 0
                    self.player_attributes['greed'] = 0
                    self.player_attributes['bluff'] = 0
        if emotion_dictionary[self.emotion] == 'anger':
                    self.player_attributes['greed'] += self.emotion_power*base_value
                    self.player_attributes['bluff'] += self.emotion_power*(base_value/2)
                    self.player_attributes['caution'] -= self.emotion_power*base_value
        if emotion_dictionary[self.emotion] == 'contempt':
                    self.player_attributes['greed'] -= self.emotion_power*base_value
                    self.player_attributes['caution'] += self.emotion_power*(base_value/2)
        
        
        
        
    #This is where the agent makes decisions based on the parameters given to it from the environment. Right now random decisions are made.    
    def make_decision(self, bets_placed,player_id,community_cards,minimum_bet_amount):
        
        #Self evaluation of score of hand
        score = self.calculate_score_of_hand(self.hand,community_cards)
        
        #Scores for each actions
        probabilities_actions = {}
        
        #Initialize scores to zero
        for i in range(len(self.available_actions)):
                probabilities_actions[i] = 0
        
        
        # Effect of bets on attributes
        # Attributes are changed by small amounts based on bets placed.
        try:
           previous_bet = bets_placed[player_id]
        except:
            previous_bet = minimum_bet_amount
        mean_bet=0
        count=0
        for x in bets_placed:
            if x==0:
                continue
            else:
                mean_bet+=x
                count+=1
        if count!=0:
            mean_bet = mean_bet/count
        if self.emotion!=2:
            caution_effect = 0
            greed_effect = 0
            bluff_effect = 0
            
            if minimum_bet_amount>previous_bet:
                caution_effect += 0.5
                greed_effect -= 0.5
            else:
                caution_effect -= 0.5
                greed_effect +=0.5
                bluff_effect += 0.5
            if mean_bet > previous_bet:
                caution_effect += 1
                greed_effect -= 0.5  
            else:
                caution_effect -= 1
                greed_effect += 0.5
                bluff_effect += 0.5
            self.player_attributes['caution'] += caution_effect
            self.player_attributes['greed'] += greed_effect
            self.player_attributes['bluff'] += bluff_effect

            #Initialize scores of each action based on emotions, these are small values.
            if self.stage == 'pre_flop':
                #Initialize probabilities based on attributes
                probabilities_actions[0] += (self.player_attributes['caution']*(score/1.5)  + self.player_attributes['greed']*(score/3) + self.player_attributes['bluff']*(score/3))/10
                probabilities_actions[1] += (-self.player_attributes['caution']*((1-score)/2) + self.player_attributes['greed']*(score/(1.1)) + self.player_attributes['bluff']*score)/10
                probabilities_actions[2] += (self.player_attributes['caution']*(1-score)/1.5)/10   
            else:
                probabilities_actions[0] += (self.player_attributes['caution']*(score/1.5) + self.player_attributes['bluff']*(score/3))/10
                probabilities_actions[1] += (self.player_attributes['caution']*(score/1.5)  + self.player_attributes['greed']*(score/3) + self.player_attributes['bluff']*(score/3))/10 
                probabilities_actions[2] += (-self.player_attributes['caution']*((1-score)/2) + self.player_attributes['greed']*(score/(1.1)) + self.player_attributes['bluff']*score)/10
                probabilities_actions[3] += (self.player_attributes['caution']*(1-score)/1.5)/10

        #Normal logical score based on current coins held       
        if self.stage == 'pre_flop':
            probabilities_actions[0] += (self.current_coins/100)
            probabilities_actions[1] += (self.current_coins/200)
            probabilities_actions[2] += 10 - (self.current_coins/100) + minimum_bet_amount/50
        else:
            median_coins = (500-self.current_coins)/60
            probabilities_actions[0] += median_coins
            probabilities_actions[1] += (self.current_coins/100)
            probabilities_actions[2] += (self.current_coins/200)
            probabilities_actions[3] += 10 - (self.current_coins/100) + minimum_bet_amount/50
            
        # Score of actions based on hand scores
        if self.stage == 'pre_flop':
                probabilities_actions[0] += score*30 +(random.random()*4-2)
                probabilities_actions[1] += score*30 +(random.random()*4-2)
                probabilities_actions[2] += (1-score)*20 +(random.random()*4-2)
        else:
                probabilities_actions[0] += score*10 +(random.random()*4-2)
                probabilities_actions[1] += score*30 +(random.random()*4-2)
                probabilities_actions[2] += score*30 +(random.random()*4-2)
                probabilities_actions[3] += (1-score)*20 +(random.random()*4-2)

        prob_array = [x[1] for x in probabilities_actions.items()]
        #Each agent can make only one move
        a = np.argmax(prob_array)
        
        #When raised, the minimum bet is doubled and the action and the amount are sent back to the environment
        return int(a),minimum_bet_amount*2
        pass
    
    
    def score_hand(self,cards):
        '''
        Gives the hand score for each agent.
        The score lies between 0-1
        Bonus score of +0.4 if all suits are same
        score is inversely proportional to the distance between card ranks.
        If the distance between card ranks is higher, the score is low and vice versa.
        score is directly proportional to the sum of card ranks, the higher the card ranks, the
        better the score
        '''
        hand = cards[0:2]
        try:
            community = cards[2:]
        except:
            community=None
        if community==None:
                community=[]
        score = 0
        frequence_suit = {"♣":0, "♦":0, "♥":0, "♠":0 }
        cumilative_ranks = ranks.copy()
        suits = [hand[0].split('_')[1],hand[1].split('_')[1]]
        for i in community:
            suits.append(i.split('_')[1])
        for i in suits:
            frequence_suit[i]+=1
        count=0
        for i in frequence_suit.keys():
            if frequence_suit[i]==0:
                count+=1
        if count>=3:
            score += 0.4       
        suit_score = max(frequence_suit.items(),key=lambda x: x[1])[1]
        score += math.exp(suit_score)/1500
        score += ((len(hand)+len(community))/7)*0.1
        ranking = [hand[0].split('_')[0],hand[1].split('_')[0]]
        for i in community:
            ranking.append(i.split('_')[0])
        rank_score = 0
        df = ranks.copy()
        rank_v = [math.log(df[i])/2.7 for i in ranking]
        mean_rank = np.mean(rank_v)
        distance_metric = [abs(i-mean_rank) for i in rank_v]
        rank_score = sum(distance_metric)
        if rank_score!=0:
            rank_score+=1/rank_score
        else:
            rank_score+=50
        rank_r = [df[i] for i in ranking]
        rank_score += sum(rank_r)
        score+=rank_score/100
        return score
    def calculate_score_of_hand(self,hand,community=None):
        if community==None:
            community=[]
        score = self.score_hand(hand+community)
        return score
#Testing area below, if needed