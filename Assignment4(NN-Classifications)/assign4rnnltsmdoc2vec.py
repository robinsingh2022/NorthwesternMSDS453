# -*- coding: utf-8 -*-
"""Assign4RNNLTSMDoc2Vec.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XyZUykI1mf1TfPqRwJV5VV8xdHeWI0kF

##INGEST
"""



import numpy as np
import pandas as pd
import string

df=pd.read_json('News_Category_Dataset_v2.json',lines=True)

"""##PREPROCESSING"""



lis=[ 'WORLD NEWS',
       'SPORTS', 'MONEY',
       'WOMEN','SCIENCE']

df=df.loc[df['category'].isin(lis)]
df=df.reset_index(drop=True)

df

df["text"] = df["headline"] + df["short_description"]



lis=[ 'WORLD NEWS',
       'SPORTS', 'MONEY',
       'WOMEN','SCIENCE']

df=df.loc[df['category'].isin(lis)]
df=df.reset_index(drop=True)

df["text"] = df["headline"] + df["short_description"]

df['text'][1]

def removePunct(txt):
  txt_nopunct="".join([c for c in txt if c not in string.punctuation])
  return txt_nopunct

df['textClean']=df['text'].apply(lambda x:removePunct(x))
df.head()

import re

def tokenize(txt):
  tokens=re.split('\W+',txt)
  return tokens

df['textCleanToken']=df['textClean'].apply(lambda x:tokenize(x.lower()))
df.head()

import nltk
nltk.download('stopwords')
stopwords=nltk.corpus.stopwords.words('english')

def removeStopwords(txt):
  txt_clean=[word for word in txt if word not in stopwords]
  return txt_clean

df['noStopwords']=df['textCleanToken'].apply(lambda x: removeStopwords(x))
df.head()

#from nltk.stem import PorterStemmer
#ps=PorterStemmer()
#def stemming(token_txt):
#  text=[ps.stem(word) for word in token_txt]
#  return text

#df['stemmed']=df['noStopwords'].apply(lambda x: stemming(x))
#df.head()

def cleanWords(text):
  txt="".join([p for p in text if p not in string.punctuation])
  tokens=re.split("\W+",txt)
  txt=[ps.stem(word) for word in tokens if word not in stopwords]

def listToString(s): 
    
    # initialize an empty string
    str1 = " " 
    
    # return string  
    return (str1.join(s))

df['string']=df['noStopwords'].apply(lambda x: listToString(x))
df.head()

def removeNum(txt):
  result = ''.join([i for i in txt if not i.isdigit()])
  return result

df['Nonum']=df['string'].apply(lambda x: removeNum(x))

df = df.sample(frac=1).reset_index(drop=True)

df



"""##DOC2VEC"""

from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from nltk.tokenize import word_tokenize

import nltk


nltk.download('punkt')
tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(df['Nonum'])]

tagged_data

max_epochs = 100
vec_size = 75
alpha = 0.025

model = Doc2Vec(size=vec_size,
                alpha=alpha, 
                min_alpha=0.00025,
                min_count=1,
                dm =1)
  
model.build_vocab(tagged_data)

for epoch in range(max_epochs):
    print('iteration {0}'.format(epoch))
    model.train(tagged_data,
                total_examples=model.corpus_count,
                epochs=model.iter)
    # decrease the learning rate
    model.alpha -= 0.0002
    # fix the learning rate, no decay
    model.min_alpha = model.alpha

model.save("d2v.model")
print("Model Saved")



nnvec=model.docvecs.vectors_docs

nnvecdf = pd.DataFrame(nnvec)

y=df['category']

import tensorflow as tf
x=nnvecdf.values

"""##LE and TRAIN/TEST SPLIT"""

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

yLE = le.fit_transform(y)

yLE = np.asarray( tf.keras.utils.to_categorical(yLE))

yLE

from sklearn.model_selection import train_test_split
trainX, testX, trainy, testy = train_test_split(x, yLE, test_size=0.25, random_state=1000)

trainX

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D, Conv1D, MaxPooling1D
import pickle

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
# transform data
trainX = scaler.fit_transform(trainX)

testX = scaler.fit_transform(testX)

from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.optimizers import Adam

model=Sequential()

model.add(Embedding(2,64,input_length=vec_size))
model.add(LSTM(128,dropout=0.1))
model.add(Dense(5,activation='sigmoid'))
optimizer=Adam(learning_rate=3e-4)
model.compile(loss='categorical_crossentropy',optimizer=optimizer,metrics=['accuracy'])

history=model.fit(trainX, trainy, epochs=20, validation_data=(testX,testy))

