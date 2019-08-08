from bs4 import BeautifulSoup
from collections import defaultdict
from operator import itemgetter
import numpy as np
import tensorflow
import itertools
from copy import deepcopy


fr = open('C:/users/mnj/Downloads/under.html', 'r', encoding='utf8').read()
soup = BeautifulSoup(fr, "html.parser")


tags = soup('div class')
tiers = soup('u')
tags = soup('li')
container = []
for tag in tags:
    if not tag:
        continue
    info = list(filter(lambda st: st != '' and '<' not in st, str(tag).split()))
    if len(info) <= 5:
        extract = str(tag.contents[0]).strip()
        container.append(extract)
        if str(tag.contents[0]).strip() == 'Lich':
            break


synergies = dict()
levels = dict()

synergies['S Tier'] = container[:3]
synergies['A Tier'] = container[3:10]
synergies['B Tier'] = container[10:15]
synergies['C Tier'] = container[15:23]
levels['1'] = container[23:37]
levels['2'] = container[37:51]
levels['3'] = container[51:66]
levels['4'] = container[66:78]
levels['5'] = container[78:83]

fr = open('C:/users/mnj/Downloads/stats.html', 'r', encoding='utf8').read()
soup = BeautifulSoup(fr, "html.parser")

'''
tags = soup('u')
for tag in tags:
    print(tag.contents)'''


soup = BeautifulSoup(fr, "html.parser")
tags = soup('li') 
st = ""

collection = []
for tag in tags:
    if tag != None and str(tag.contents[0]).startswith('<strong>'):
        extract = ["Alliance 1", "Alliance 2", 'Alliance 3', 'Alliance 4', 'Health', 'DPS', 'Attack Range', 'Armor']
        
        for e in extract:
            
            if str(tag.contents[0]).find(e) != -1:
                collection.append(str(tag.contents[1]).strip())
                
            
            

info = {}
tags = soup('u')
i = 0
for tag in tags:
    if str(tag)[3:-4] == 'Puck' or str(tag)[3:-4] == 'Dragon Knight' or str(tag)[3:-4] == 'Lycan':
        info[str(tag)[3:-4]] = collection[i:i+8]
        i += 8
    else: 
        info[str(tag)[3:-4]] = collection[i:i+7]
        i += 7



l1 = []
for nm in levels:
    for si in levels[nm]:
        l1 += [si]

l2 = []
for key in l1:
    if 'Wind' in key:
        l2.append(key)
    if 'Nature' in key:
        l2.append(key)

st = ''
for ao in info:
    if 'Nature' in ao:
         st = ao
        
for m in l2:
    if 'Wind' in m:
        info[m] = info['Wind Ranger']
    else:
        info[m] = info[ao]

# give each hero a number for q-table access later on 
heroes_to_num = {}
for index, hero in enumerate(info.keys()): 
    heroes_to_num[hero.strip()] = index

num_to_heroes = {}
for index, hero in enumerate(info.keys()): 
    num_to_heroes[index] = hero

i = 0
synergies_to_num = {}
all_synergies = []

for tier in synergies:
    for synergy in synergies[tier]:
        synergies_to_num[synergy] = i
        all_synergies.append(synergies)
        i += 1

'''
add_syns = []
for key in synergies_to_num:
    add_syns.append(key[:-1])
for syn in add_syns:
    synergies_to_num[syn] = synergies_to_num[key]'''

from difflib import SequenceMatcher

# given a synergy which may not be in the dictionary, this tries to find the closest matching one
def similarity_function(access):
    # return the synergy string of which access most closely correlates to
    max_sim_synergy = ''
    max_ratio = 0

    for key in synergies_to_num:
        if SequenceMatcher(None, access, key).ratio() > max_ratio:
            max_ratio = SequenceMatcher(None, access, key).ratio()
            max_sim_synergy = key
        return max_sim_synergy



class UnderlordSimulator:
    def __init__(self):
        self.pieces_to_num = heroes_to_num
        self.num_to_pieces = num_to_heroes
        self.synergies_to_num = synergies_to_num
        self.piece_stats = info
        self.gold = 1
        self.lev = 1
        self.xp = 1
        self.inventory = dict()
        self.iter = 0
        for value in heroes_to_num.values(): 
            self.inventory[value] = [0, 0, 0] # number of level 1, 2, and 3 troops
        self.exp_needed = [2, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40] # experience needed to level up
        self.synergy_inventory = dict()
        for n in range(i):
            self.synergy_inventory[n] = 0
        self.existing = {}
        self.rnd = 1

    # returns level of a piece
    def get_lev(self, piece_name):
        for lev in levels.keys():
            if piece_name in levels[lev]:
                return int(lev)

    def generate_troops(self, prob):
        troops = []
        for i in range(5):
            subset = np.random.choice([1, 2, 3, 4, 5], p=prob)
            troop = np.random.choice(levels[str(subset)])
            troops += [troop]
        return troops
    

    # simulate each round so we can have a recursive min-max
    def rnd_sim(self, pieces, state, depth, max_depth=3):
        combs = []

        init_state = (self.gold, self.inventory, self.synergy_inventory) # we don't want to override these between each run
        state_vals = [0]
        # available_pieces = input('What pieces are in the store?')
        # available_pieces = available_pieces.split(',')

        # for each of the available pieces in the shop, calculate the game state value if they were to be bought
        for piece in pieces:
            '''if self.inventory[self.pieces_to_num[piece]] == [0, 0, 0] and self.rnd >= 11:
                state_vals += [0]
                continue'''


            self.gold = init_state[0]
            # these are mutable - account for this when altering self.inventory with a deepcoopy
            self.inventory = deepcopy(init_state[1])
            self.synergy_inventory = deepcopy(init_state[2])
            

            piece = piece.strip() # remove white space
            # self.gold -= self.get_lev(piece) # subtact the cost of the piece
            

            if self.gold < 50:
                self.gold += (5 + int((self.gold * 0.1)))
            else:
                self.gold += 5

            # calculate the state    
            # find the combination of pieces which give the maximum state value (accounting for synergies, player level, piece level, etc.)
            max_pieces = self.lev

            
            # merge level 1 pieces to level 2 if enough
            if self.inventory[self.pieces_to_num[piece]][0] < 2: # if the amt of level 1 pieces is less than 3, increment by 1
                self.inventory[self.pieces_to_num[piece]][0] += 1
            else:
                self.inventory[self.pieces_to_num[piece]][0] = 0
                self.inventory[self.pieces_to_num[piece]][1] = 1
            
                # do same but from level 2 to level 3
                if self.inventory[self.pieces_to_num[piece]][1] < 2: 
                    self.inventory[self.pieces_to_num[piece]][1] += 1
                else:
                    self.inventory[self.pieces_to_num[piece]][1] = 0
                    self.inventory[self.pieces_to_num[piece]][2] = 1

            if depth != max_depth:
                returned_vals = self.rnd_sim(self.generate_troops([1.0, 0, 0, 0, 0]), 0, depth + 1)
                state_vals += [returned_vals]
                # we have a list of 5 state values
                #combs.append()
            else: 

                # go through all combinations of heroes 
                simplified_inventory = []
                # get the hero number representations for each of the pieces we have 
                for item in self.inventory:
                    if self.inventory[item] != [0, 0, 0]:
                        for n in range(self.inventory[item][0]):
                            simplified_inventory.append(item)
                        for n in range(self.inventory[item][1]):
                            simplified_inventory.append(item)
                
                
                # go through the set of each pieces in the inventory that may be placed on the board and calculate which will max the state
                for pieces_on_board in itertools.combinations(simplified_inventory, max_pieces):
                    # how can this be decreasing / so far from predicted
                    state_val = 0
                    
                    if self.pieces_to_num[piece] not in pieces_on_board: # check unique combinations only
                        continue
                    if self.existing.get(pieces_on_board, -1) != -1:
                        continue
                    
                        

                    self.iter += 1
                    
                    synergy_count = 0
                    in_board = []

                    for board_piece in pieces_on_board: # duplicate pieces on board
                        in_board.append(board_piece)
                        if board_piece not in in_board:
                            synergy1 = self.piece_stats[self.num_to_pieces[board_piece]][0]
                            synergy2 = self.piece_stats[self.num_to_pieces[board_piece]][1]
                            

                            # add in case for heroes with 3 or more synergies ***
                            # 1 synergy per unique piece (so only consider it the first time and then forget about it)

                            self.synergy_inventory[self.synergy_inventory.get(self.synergies_to_num[similarity_function(synergy1)])] += 1
                            self.synergy_inventory[self.synergy_inventory.get(self.synergies_to_num[similarity_function(synergy2)])] += 1
                        

                    for synergy in self.synergy_inventory:
                        #if self.synergy_inventory[synergy] // 3 == 1: # if you have 3 of the same kind
                        if self.synergy_inventory.get(synergy, similarity_function(self.num_to_pieces[synergy])) // 3 == 1:
                            state_val += 5
                        #if self.synergy_inventory[synergy] // 6 == 1:
                        if self.synergy_inventory.get(synergy, similarity_function(self.num_to_pieces[synergy])) // 6 == 1:
                            state_val += 15
                        if self.synergy_inventory.get(synergy, similarity_function(self.num_to_pieces[synergy])) // 9 == 1:
                            state_val += 40

                    # factor in level of the pieces on the board
                    for board_piece in pieces_on_board:
                        for i in range(3):
                            if i == 1: 
                                state_val += (self.inventory[self.pieces_to_num[piece]][i]) * 5
                            if i == 2:
                                state_val += (self.inventory[self.pieces_to_num[piece]][i]) * 10
                    
                    self.existing[pieces_on_board] = 0 

                    # factor in amount of gold
                    state_val += (self.gold / 2)
    
                    
                    state_vals += [state_val] # append the predicted state val for each hero
                    # we have a list of 5 state values
                    
        
        # return the best state val out of the pieces presented
        if depth == 1:
            max_val = 0
            max_index = 0 
            for i, val in enumerate(state_vals):
                if val > max_val:
                    max_val = val
                    max_index = i 
                    
            print(state_vals)
            self.gold = init_state[0]
            self.inventory = init_state[1]
            self.synergy_inventory = init_state[2]
            #print(combs)
            return max(state_vals), max_index, combs
        
        return sum(state_vals) / len(state_vals) # max(state_vals)


    def game_sim(self):
        
        for rnd in range(1, 35):
        
            self.rnd = rnd
            print('Round', rnd )
            available_pieces = input('What pieces are in the store?')
            available_pieces = available_pieces.split(',')
            #available_pieces = self.generate_troops([0.2, 0.2, 0.2, 0.2, 0.2])
            if rnd <= 7: 
                state_val, index, comb = self.rnd_sim(available_pieces, 0, 1, 5)
            else:
                state_val, index, comb  = self.rnd_sim(available_pieces, 0, 1)
                
            #print('Buy', available_pieces[index])
            self.xp += 1
            if self.xp == self.exp_needed[self.lev - 1]:
                self.lev += 1
                self.xp = 0

            index -= 1

            self.inventory[self.pieces_to_num[available_pieces[index]]][0] += 1
            if self.inventory[self.pieces_to_num[available_pieces[index]]][0] == 3:
                self.inventory[self.pieces_to_num[available_pieces[index]]][1] += 1
                self.inventory[self.pieces_to_num[available_pieces[index]]][0] = 0

                if self.inventory[self.pieces_to_num[available_pieces[index]]][1] == 3:
                    self.inventory[self.pieces_to_num[available_pieces[index]]][1] = 0
                    self.inventory[self.pieces_to_num[available_pieces[index]]][2] = 1

            #combs = itertools.combinations(simplified_inventory, self.lev)
        
            #pieces_on_board = set(comb)
            
            # calculate the synergies each round
            for syn in self.synergy_inventory:
                self.synergy_inventory[syn] = 0

            # why aren't combinations being added

            #for pce in pieces_on_board: 
                '''synergy1 = self.piece_stats[self.num_to_pieces[self.pieces_to_num[pce]][0]]
                #synergy2 = self.piece_stats[self.num_to_pieces[self.pieces_to_num[available_pieces[index]]]][1]
                synergy2 = self.piece_stats[self.num_to_pieces[self.pieces_to_num[pce]][1]]

                # only count 1 synergy per unique piece
                self.synergy_inventory[self.synergy_inventory.get(self.synergies_to_num[similarity_function(synergy1)])] += 1
                self.synergy_inventory[self.synergy_inventory.get(self.synergies_to_num[similarity_function(synergy2)])] += 1'''

            #synergy1 = self.piece_stats[self.num_to_pieces[self.pieces_to_num[pce]][0]]
            synergy1 = self.piece_stats[self.num_to_pieces[self.pieces_to_num[available_pieces[index]]]][0]
            synergy2 = self.piece_stats[self.num_to_pieces[self.pieces_to_num[available_pieces[index]]]][1]

            # only count 1 synergy per unique piece
            self.synergy_inventory[self.synergy_inventory.get(self.synergies_to_num[similarity_function(synergy1)])] += 1
            self.synergy_inventory[self.synergy_inventory.get(self.synergies_to_num[similarity_function(synergy2)])] += 1

            print('Total permutations checked: ', self.iter)
            print('Max state value: ', state_val)
            if rnd == 10:
                print(self.inventory)
                print(self.synergy_inventory)
            
        '''
        if self.gold < 50:
            self.gold += (5 + (gold * 0.1))
        else:
            gold += 5
        '''

print(synergies_to_num)
game_instance = UnderlordSimulator()
game_instance.game_sim()

# make sure that the indices for all the regex synergies are not 22
# make sure that their is only 1 synergy per unique piece
# use threads for quick computation