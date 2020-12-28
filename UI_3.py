import sys
import random
import itertools
import time
import pickle

try:
    from PokerEnv import *
except Exception as e:
    print(e)
    s = input()

# Load the input data from the user
f  = open("players_e.pickle",'rb')
player_emotions = pickle.load(f)
f.close()

f  = open("players_p.pickle",'rb')
player_powers = pickle.load(f)
f.close()

#Create a list of players and assign the emotions to them
players_list = []
for i in range(len(player_powers)):
    p = Player()
    try:
        a = Agent(p,1000,player_emotions[i],player_powers[i])
    except Exception as e:
        print(e)
        s = input()
    players_list.append(a)

count=0
#Here is a list of Players, along with their emotions and the power of their emotions
for i in players_list:
    print("Player ID:",count,", Emotion:",emotion_dictionary[i.emotion],", Emotion Power:",i.emotion_power)
    count+=1

# The game starts from here
s = input("press 'y' to continue:")
try:
    #API Usage, create an environment with player list
    env = PokerEnvironment(players_list)
    #Give hand cards to each player
    env.reset()
    print("Game has begun:")
    print("Here are each player hands:")
    for i in range(len(player_powers)):
        print("ID:",i,env.player_objects[i].hand)
    
    #Run Preflop round
    env.pre_flop()
    print("Pre Flop round Done!")
    print("Actions taken by each player:")
    for i in range(len(player_powers)):
        print("ID:",i,"Actions:",env.player_objects[i].actions_taken[env.stage])
    s = input("press 'y' to continue:")
    
    #Run Flop round
    env.flop()
    print("Flop Round Done!")
    print("Actions taken by each player:")
    for i in range(len(player_powers)):
        print("ID:",i,"Actions:",env.player_objects[i].actions_taken[env.stage])
    s = input("press 'y' to continue:")
    
    #Run Turn round
    env.turn()
    print("Turn round Done!")
    print("Actions taken by each player:")
    for i in range(len(player_powers)):
        print("ID:",i,"Actions:",env.player_objects[i].actions_taken[env.stage])
    s = input("press 'y' to continue:")
    
    #Run River round
    env.river()
    print("River Round Done!")
    print("Actions taken by each player:")
    for i in range(len(player_powers)):
        print("ID:",i,"Actions:",env.player_objects[i].actions_taken[env.stage])
    s = input("press 'y' to continue:")
    print("Showdown!")
    
    #The showdown
    env.showdown()
    print("Game has ended, here are the stats!")
    s = input("press 'y' to continue:")
    
    #Display the game stats.
    for i in env.game_stats:
        if i == 'players' or i=='winner' or i=='win_e_num' or i=='debt':
            continue
        print(i,":",env.game_stats[i])
    s = input("press 'y' to continue:")
except Exception as e:
    print(e)
    s = input("press 'y' to continue:")
