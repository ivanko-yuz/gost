
import pandas as pd
import csv

import glob
import os
import numpy as np
import keras
from keras.layers import Input, Activation, Dense, BatchNormalization,Dropout
from keras.models import Model, Sequential
from keras.callbacks import ModelCheckpoint,Callback
import keras.backend as K
from keras.optimizers import SGD

from managers.csvManager import csv_run


def genreToVector(genre):
    genres = ['POP', 'CLASSIC', 'UNKNOWN', 'ROCK', 'Metal']
    vector = [0] * len(genres)
    vector[genres.index(genre)] = 1
    return vector


def vectorToGenre(vector):
    genres = ['POP', 'CLASSIC', 'UNKNOWN', 'ROCK', 'Metal']
    genre = genres[np.where(vector==1)[0][0]]
    return genre

def euclideanDistance(instance1, instance2, length):
	distance = 0
	for x in range(length):
		distance += pow((instance1[x] - instance2[x]), 2)
	return math.sqrt(distance)
 
def getNeighbors(trainingSet, testInstance, k):
	distances = []
	length = len(testInstance)-1
	for x in range(len(trainingSet)):
		dist = euclideanDistance(testInstance, trainingSet[x], length)
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors


def getResponse(neighbors):
	classVotes = {}
	for x in range(len(neighbors)):
		response = neighbors[x][-1]
		if response in classVotes:
			classVotes[response] += 1
		else:
			classVotes[response] = 1
	sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]


def subfinder(mylist, pattern):
    result = []
    ansv = False
    for i in range(0,len(mylist)):   
        print('Checking the {0} song for similar interval'.format(i))
        for j in range(len(mylist.iloc[i]) - len(pattern)):            
            if list(pattern) == list(mylist.iloc[i][j:j + len(pattern)]):
                 ansv = True
        if ansv == True:
            result.append(mylist.iloc[i])
            ansv = False
            break
    return result


def KNN():
    trainingSet=[]
    testSet=[]
    split =0.9
    
    numbers=[]
    for x in range(len(df)-1):
        if random.random() < split:
            trainingSet.append(df.loc[x,:])
        else:
            testSet.append(df.loc[x,:])
            numbers.append(x)
    
    print ('Train set: ' + repr(len(trainingSet)))
    print ('Test set: ' + repr(len(testSet)))
    
    predictions=[]
    k = 5
    for x in range(len(testSet)):
    	neighbors = getNeighbors(trainingSet, testSet[x], k)
    	result = getResponse(neighbors)
    	predictions.append(result)
    	print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1])+' song: '+dfname.iat[numbers[x],0]+' author: '+dfauthor.iat[numbers[x],0])
    
    
    df = pd.concat([dfhashes, dfstyle], axis=1, join='inner')
    df_hashes_names = pd.concat([dfhashes_set, dfname_set] , axis=1)
    
    df_hashes_names=df_hashes_names.fillna(0)
    
    trainingSet=[]
    testSet=[df_hashes_names.loc[10,:],df_hashes_names.loc[6,:]]
    for x in range(len(df_hashes_names)-1):
        trainingSet.append(df_hashes_names.loc[x,:])
    
    predictions=[]
    k = 5
    for x in range(len(testSet)):
        neighbors = getNeighbors(trainingSet, testSet[x], k)
        print('> search for ' + repr(testSet[x][-1]))
        for i in range(len(neighbors)):
            print('closest=' + str(neighbors[i][-1]))

def neural_network():
    model = Sequential()
    model.add(Dense(units=5215*2, activation='sigmoid', input_dim=5215))
    model.add(Dense(units=1000, activation='sigmoid'))
    
    #model.add(Dropout(0.1))
    model.add(Dense(units=5, activation='softmax'))
    
    sgd = SGD(lr=0.01, momentum=0.9, decay=0, nesterov=True)
    adam = keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
    
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    
    model.summary()
    
    genre_train_str = np.array(df_full['Genre'])
    genre_train = np.array(list(map(genreToVector, genre_train_str)))
    
    data_train_nonorm = np.array(dfhashes)
    data_train = [0]*len(data_train_nonorm)
    
    for i in range(len(data_train_nonorm)):
        data_train[i] = data_train_nonorm[i]/float(max(data_train_nonorm[i]))
         
    data_train = np.array(data_train)
    
    model.fit(data_train, genre_train, epochs=200, batch_size=5)
    
    
    end_result = model.evaluate(x_train, y_train, batch_size=1)
    print(loss_and_metrics)
    
    
    count_t = 0
    count_f = 0
    
    for line in range(0,71):
        print(dfgenre.iloc[[line]].values[0][0])
        classes = model.predict(np.array(dfhashes.iloc[[line]]))
        vector = np.zeros(5)
        vector[np.where(classes == max(max(classes)))[1][0]] = 1
        print(vectorToGenre(vector))
        
        if vectorToGenre(vector) == dfgenre.iloc[[line]].values[0][0]:
            print('True')
            count_t += 1  
        else :
            print('False')
            count_f += 1
        print()
    
    print('# of true : ' + str(count_t))
    print('# of false : ' + str(count_f))

def shazam_algoithm():
    i_love_this_song = df_full.iloc[6][1000:2000]
    print('We are trying to predict result for this song' + str(df_full.iloc[6]['Author'])
          + ' - '+ str(df_full.iloc[6]['Title']) 
          + 'and genre of song is '+  str(df_full.iloc[6]['Genre']))
    
    ans = subfinder(df_full, df_full.iloc[6][1000:2000])
    
    ans = pd.DataFrame(ans)
    print(str(ans['Author'].values[0]) +' - '+ str(ans['Title'].values[0]) +'and genre of song is '+  str(ans['Genre'].values[0]))

def slm_run():

    df, df_full, dfauthor, dfauthor_set, dfgenre_set, dfhashes, dfhashes_set, dfname_set, dfstyle = csv_run()

    KNN()

    neural_network()

    shazam_algoithm()

