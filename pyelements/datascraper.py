from bs4 import BeautifulSoup
from collections import defaultdict
from operator import itemgetter
import numpy as np

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
collection = []
for tag in tags:
    if tag != None and str(tag.contents[0]).startswith('<strong>'):
        extract = ["Alliance 1", "Alliance 2", 'Alliance 3', 'Alliance 4', 'Health', 'DPS', 'Attack Range', 'Armor']
        for e in extract:
            
            if str(tag.contents[0]).find(e) != -1:
                collection.append(str(tag.contents[1]))
            

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

def generate_troops(prob):
    troops = []
    for i in range(5):
        subset = np.random.choice([1, 2, 3, 4, 5], p=prob)
        troop = np.random.choice(levels[str(subset)])
        troops += [troop]
    return troops


def simulate_game():
    gold = 1
    prob_per_tier = [0.5, 0.2, 0.15, 0.1, 0.05]
    health = 100

    print(generate_troops(prob_per_tier))
    while health > 0:
        #print(generate_troops(prob_per_tier))
        health -= 10

#simulate_game()
fw = open('output.js', 'w')
for key in info:
    fw.write(str(info))
    '''
    st = ''
    for var in info[key]:
        st += str(var + ', ')
    out = key + ': ' + st
    fw.write(out + '\n')
    '''
fw.close()
