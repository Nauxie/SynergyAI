from bs4 import BeautifulSoup
from collections import defaultdict
from operator import itemgetter
import numpy as np
import copy
import tensorflow as tf
from functools import partial
import itertools

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


def shuffle_batch(X, y, batch_size):
    for i in range(10):
        #print(n([y[i]]))
        #print(np.array([y[i]]).shape)
        print(np.array([X[i]]))
        yield np.array([X[i]]), np.array([y[i]])
        
    '''rnd_idx = np.random.permutation(len(X))
    n_batches = np.ma.size(X) // batch_size
    for batch_idx in np.array_split(rnd_idx, n_batches):
        X_batch, y_batch = X[batch_idx], y[batch_idx]
        yield X_batch, y_batch'''

def generate_troops(prob=[0.5, 0.2, 0.2, 0.07, 0.03]):
    troops = []
    for i in range(5):
        subset = np.random.choice([1, 2, 3, 4, 5], p=prob)
        troop = np.random.choice(levels[str(subset)])
        #while ' ' in troop:
            #troop = troop[:troop.index(' ')] + '_' + troop[troop.index(' ') + 1:]
        troops += [troop]
    return troops

def simulate_game():
    
    # make keys accessible w/ underscores
    for key in info:
        while ' ' in key:
            key_correct = key[:key.index(' ')] + '_' + key[key.index(' ') + 1:]
            info[key_correct] = info[key]
            del info[key]
            key = key_correct
            print(key_correct)
    
    
    y_tr = []
    fw = open('output.csv', 'w')

    content = []
    for i in range(10):
        subcont = []
x```
        for sub in range(5):
            

            synergy1_tier = np.random.randint(1, 4)
            syn1_left = np.random.randint(1, 3)
            syn2_tier = np.random.randint(1, 4)
            syn2_left = np.random.randint(1, 3)
            hero_level= np.random.randint(1, 2)
            if hero_level == '2':
                hero_left = np.random.randint(1, 6)
            else:
                hero_left = np.random.randint(1, 3)
            hero_tier = np.random.randint(1, 5)
            subcont += [[synergy1_tier, syn1_left, syn2_tier, syn2_left, hero_level, hero_left, hero_tier]]
            content.append(subcont)
            
            #fw.write(synergies_left + ', ' + synergy_tier + ', ' + hero_tier + ', ' + gold)
            #fw.write('\n')

        print(subcont)
        y_tr += [int(input('Choose which one(s) - synergy tier, how many left needed to upgrade, hero level, heroes to upgrade, hero tier\n'))]    
    #content
    #y_tr
    #print(y_tr.shape)
    input()

    X = tf.placeholder(shape=(1, 5, 7,), name='inputs', dtype=tf.float32)
    X_flat = tf.layers.flatten(X)
    y = tf.placeholder(shape=(1), name='outputs', dtype=tf.int32)

    n_inputs = 28 * 28  # MNIST
    n_hidden1 = 300
    n_hidden2 = 100
    n_outputs = 1

    he_init = tf.variance_scaling_initializer()

    
    training = tf.placeholder_with_default(False, shape=(), name='training')

    # avoid retyping in parameters
    my_batch_norm_layer = partial(tf.layers.batch_normalization, training=training, momentum=0.9)
    my_dense_layer = partial(tf.layers.dense, kernel_initializer=he_init)

    # layers
    #hidden1 = my_dense_layer(X, 150)
    #bn1 = tf.nn.elu(my_batch_norm_layer(hidden1))
    #hidden2 = my_dense_layer(bn1, n_hidden2, name="hidden2")
    #bn2 = tf.nn.elu(my_batch_norm_layer(hidden2))
    #logits = tf.layers.dense(bn2, 1, name='outputs')
    #logits_before_bn = my_dense_layer(bn2, name="outputs")
    #logits = my_batch_norm_layer(logits_before_bn)
    hidden1 = tf.layers.dense(X_flat, 200, kernel_initializer=he_init)
    hidden2 = tf.layers.dense(hidden1, 100, kernel_initializer=he_init)
    hidden3 = tf.layers.dense(hidden2, 50, kernel_initializer=he_init)
    logits = tf.layers.dense(hidden3, 5, kernel_initializer=he_init)
    
    print(logits.shape)
    input()

    with tf.name_scope("loss"):
        xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=y)
        loss = tf.reduce_mean(xentropy, name="loss")

    with tf.name_scope("train"):
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)
        training_op = optimizer.minimize(loss)

    '''with tf.name_scope("eval"):
        correct = tf.nn.in_top_k(logits, y, 1)
        accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))
        fw.close()'''

    init = tf.global_variables_initializer()
    saver = tf.train.Saver()

    n_epochs = 30
    batch_size = 1

    extra_update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)

    with tf.Session() as sess:
        init.run()
        for epoch in range(n_epochs):
            for X_batch, y_batch in shuffle_batch(content , y_tr, batch_size):
                sess.run([training_op, extra_update_ops], feed_dict={X: X_batch, y: y_batch})
            
            #accuracy_val = accuracy.eval(feed_dict={X: X_valid, y: y_valid})
            #print(epoch, "Validation accuracy:", accuracy_val)

        save_path = saver.save(sess, "./syn_ai_py.ckpt")

    '''
    gold = 1
    prob_per_tier = [0.5, 0.2, 0.15, 0.1, 0.05] # chance per hero tier
    health = 100
    troops = generate_troops(prob_per_tier)

    my_heroes = { troops[0] : info[troops[0]] }
    states = {troops[0] : [1, 1, 1] } # keep track of synergies and levels
    enemy_states = {'Axe' : [1, 1, 2]}
    
    print(my_heroes)
    their_heroes = {'Axe' : info['Axe']}


    while health > 0:
        
        troops = generate_troops(prob_per_tier)


        if troops[0] in my_heroes and troops[0] in states:
            states[troops[0]] = [i * 2 for i in states[troops[0]]]

        my_heroes[troops[0]] = info[troops[0]] 
        states = {troops[0] : [1, 1, 1] }
        
        # if there are 3 troops, then upgrade it to level 2
        if states[troops[0]][-1] == 3:
            lev = 2
        else:
            lev = 1

        # create a deep copy to use each round and make the values ints
        ai_heroes = copy.deepcopy(my_heroes)
        for hero in ai_heroes:
            for i in range(2, 7):
                print(ai_heroes[hero])

                # get rid of colons and useless characters which are in front of the stats like health
                while True:
                    try:
                        ai_heroes[hero][i] = int(ai_heroes[hero][i].strip().split('/')[lev-1])
                    except:
                        ai_heroes[hero][i] = ai_heroes[hero][i][1:]
                        print(ai_heroes[hero][i])
                        continue
                    break
                #ai_heroes[hero][i] = int(ai_heroes[hero][i].strip().split('/')[lev-1])

        print(ai_heroes)
        
        # copy old dictionary
        enemy_heroes = copy.deepcopy(their_heroes)
        for hero in enemy_heroes:
            for i in range(2, 7):
                enemy_heroes[hero][i] = int(enemy_heroes[hero][i].strip().split('/')[lev-1])

        # delete the items in the copied dictionary if the troops get eliminated, causing the round to end when all troops are gone
        while len(enemy_heroes.keys()) != 0:
            for hero in ai_heroes:
                enemy_heroes['Axe'][2] -= (ai_heroes[hero][3] - enemy_heroes['Axe'][-1])
                print(enemy_heroes)
            if enemy_heroes['Axe'][2] <= 0:
                del enemy_heroes['Axe']
        
        gold += 5 + int(gold * 0.1) 
        health -= 10
        '''


#simulate_game()
# fw = open('output.js', 'w')


# Number of discrete states / observations which will each have actions w/ different rewards
# 
# All possible actions - buy heroes, sell heroes, reroll, level up 
# States - # of gold, level 2 heroes, level 1 heroes, player level  
discrete_states = 80 * 60 * 10

actions = []

for i in range(7):
    possible = list(itertools.combinations([0, 1, 2, 3, 4, 5, 6, 7], i)) # possible actions 
    for poss in possible:
        actions.append(poss)

#print(actions)



q_table = {}
# q-table with all discrete states and their corresponding actions
for gold in range(80):
    for hero1 in range(60):
        for hero2 in range(3):
            for level in range(10):
                #q_table[(gold, hero1, hero2, level, act)] = [np.random.uniform(-1, 1) for i in range(len(actions))]
                q_table[(gold, hero1, hero2, level)] = [np.random.uniform(-1, 1) for i in range(60)]

n_episodes = 10000
epsilon = 0.9
EPS_DECAY = 0.9998
meta = ['Lich', 'Dragon Knight', 'Crystal Maiden', 'Lina', 'Puck']
LEARNING_RATE = 0.1
DISCOUNT = 0.95

print(levels['2'])
l1 = []
for nm in levels:
    for si in levels[nm]:
        l1 += [si]
print(set(l1) - set(info.keys()))

l2 = []
for key in l1:
    if 'Wind' in key:
        l2.append(key)
    if 'Nature' in key:
        l2.append(key)

print(l2)

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
    heroes_to_num[hero] = index

# create a game and game environment


'''
for episode in range(n_episodes):
    episode_reward = 0

    gold = 1
    lev = 1
    heroes = dict()

    #print(heroes_to_num)
    for value in heroes_to_num.values(): 
        heroes[value] = [0, 0, 0] # number of level 1 and 2 

    for rnd in range(35):
        BUY_PENALTY = 0
        reward =0 

        troops = generate_troops()

        hero_lev1, hero_lev2 = 0, 0
        # find number of level 1 and 2 heroes on the board
        
        for hero in heroes:
            hero_lev1 += [hero]
            for levs in heroes[hero]:
                hero_lev2 += [heroes[hero][lev]]
        obs = gold, lev, hero_lev1, hero_lev2

        available = []
        for troop in troops:
            available += heroes_to_num[troop]

        if np.random.random() > epsilon:
            action = np.argmax(q_table[obs][available])
        else:
            action = np.random.choice(available)
            #action = actions[np.random.randint(0, len(actions))]
            #print(action)
        
        #for num in action: # go and perform each of the individual action (buy unit 1, 2, etc.)
        # indent
        num = action
        if num < 90: #if 0 <= num <= 4:
            heroes[heroes_to_num[troops[num]]][0] += 1
            # upgrade level if 3 units
            if heroes[heroes_to_num[troops[num]]][0] == 3:
                heroes[heroes_to_num[troops[num]]][1] = 1
                heroes[heroes_to_num[troops[num]]][0] = 0
                if troops[num] in meta:
                    reward = 300
                else:
                    reward = 50
            else:
                if troops[num] in meta: 
                    reward = 75
            # subtract cost of troop
            for n in range(5):
                if troops[num] in levels[str(n + 1)]:
                    gold -= (n + 1)
                    BUY_PENALTY = -5 * (n + 1)
                    break
        
        if gold >= 50:
            if not gold < 70:
                gold += (5 + 5)
        else: 
            gold += 5 + int(gold * 0.1)

        new_hero_lev1, new_hero_lev2 = [], []
        '''
        '''
        # find number of level 1 and 2 heroes on the board
        for hero in heroes:
            new_hero_lev1 += heroes[hero][0] 
            new_hero_lev2 += heroes[hero][1]
        '''
        '''
        for hero in heroes:
            new_hero_lev1 += [hero]
            for levs in heroes[hero]:
                new_    hero_lev2 += [heroes[hero][lev]]


        new_obs = gold, lev, new_hero_lev1, new_hero_lev2

        # find action which maximizes q value / future rewards
        try:
            max_future_q = np.max(q_table[new_obs])
        except:
            print(rnd)
        # find current q-value (action is not always the best action)
        current_q = q_table[obs][num]

        PASS_PENALTY = - (rnd ** 1.5) # represented by inngame player damage 
        if reward == 300 or reward == 50:
            new_q = reward
        else: 
            # Determine the q-value by finding the maximum future reward and taking into account the current reward
            reward += PASS_PENALTY
            reward += BUY_PENALTY
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)

        q_table[obs][num] = new_q
        print(gold, heroes)
    epsilon *= EPS_DECAY
  

'''
# convert to json
'''
for li, hero in enumerate(info):
    contents = info[hero]
    fw.write('{\n')
    extract = ["Alliance 1", "Alliance 2", 'Alliance 3', 'Health', 'DPS', 'Attack Range', 'Armor']
    fw.write('\tid: ' + ' \'' + str(li) + '\',\n' )
    fw.write('\tname: ' + ' \'' + hero + '\'' + ',\n')
    fw.write('\ttype1: ' + '\'' + contents[0] + '\' ' + ',\n')
    fw.write('\ttype2: ' + '' + '\'' + contents[1] + '\' ' + ',\n')
    if not '/' in contents[2]:
        fw.write('\ttype3:' + '\'' + contents[2] + '\'' + ',\n')
        i = 0
    else:
        i = -1
    fw.write('\tHealth: ' + '\'' + contents[3 + i] + '\' ' + ',\n')
    fw.write('\tDPS: ' + '\'' + contents[4 + i] + '\' ' + ',\n')
    fw.write('\tAttack_Range: ' + '\'' +  contents[5 + i] + '\' ' + ',\n')
    fw.write('\tArmor: ' + '\'' + contents[6 + i] + '\' ' + ',\n')
    fw.write('}, \n')

'''