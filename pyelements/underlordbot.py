from bs4 import BeautifulSoup
from collections import defaultdict
from operator import itemgetter
import numpy as np
import copy
import tensorflow as tf
from functools import partial

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

def generate_troops(prob):
    troops = []
    for i in range(5):
        subset = np.random.choice([1, 2, 3, 4, 5], p=prob)
        troop = np.random.choice(levels[str(subset)])
        while ' ' in troop:
            troop = troop[:troop.index(' ')] + '_' + troop[troop.index(' ') + 1:]
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