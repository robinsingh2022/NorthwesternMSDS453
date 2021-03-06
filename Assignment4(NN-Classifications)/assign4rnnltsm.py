# -*- coding: utf-8 -*-
"""Assign4RNNLTSM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qA_dARoPAuUeTIrZZsxRyZnJT1r8VC07

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

from nltk.stem import PorterStemmer
ps=PorterStemmer()
def stemming(token_txt):
  text=[ps.stem(word) for word in token_txt]
  return text

df['stemmed']=df['noStopwords'].apply(lambda x: stemming(x))
df.head()

def cleanWords(text):
  txt="".join([p for p in text if p not in string.punctuation])
  tokens=re.split("\W+",txt)
  txt=[ps.stem(word) for word in tokens if word not in stopwords]

def listToString(s): 
    
    # initialize an empty string
    str1 = " " 
    
    # return string  
    return (str1.join(s))

df['string']=df['stemmed'].apply(lambda x: listToString(x))
df.head()

def removeNum(txt):
  result = ''.join([i for i in txt if not i.isdigit()])
  return result

df['Nonum']=df['string'].apply(lambda x: removeNum(x))

df = df.sample(frac=1).reset_index(drop=True)

df=df[:20000]



df

from collections import Counter
def counter_word(text):
  count=Counter()
  for i in text.values:
    for word in i.split():
      count[word]+=1
  return count

text=df.Nonum

text



print(df.Nonum.map(lambda x: len(x)).max())

def countWordlen(lst):
    count = 0
    for i in lst: # loop over the items of the list
        if len(i) >= 150: # if the len the items (words) equals 3 increment count by 1
            count = count + 1
    return count

countWordlen(list(text))

counter=counter_word(text)

counter

len(counter)

num_words=len(counter)

max_length=175

text

from keras.preprocessing.text import Tokenizer
tokenizer = Tokenizer(num_words=num_words)
tokenizer.fit_on_texts(text)

word_index=tokenizer.word_index
word_index

sequences=tokenizer.texts_to_sequences(text)

sequences[0]

from keras.preprocessing.sequence import pad_sequences
padded=pad_sequences(sequences,maxlen=max_length,padding='post',truncating='post')

padded[0]

padded.shape

y=df['category']



from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

yLE = le.fit_transform(y)

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D, Conv1D, MaxPooling1D
import pickle

yLE = np.asarray( tf.keras.utils.to_categorical(yLE))

yLE

from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.optimizers import Adam

model=Sequential()

model.add(Embedding(num_words,64,input_length=max_length))
model.add(LSTM(128,dropout=0.1))
model.add(Dense(64,activation='relu'))
model.add(Dense(32,activation='relu'))
model.add(Dense(16,activation='relu'))
model.add(Dense(5,activation='sigmoid'))
optimizer=Adam(learning_rate=3e-4)
model.compile(loss='categorical_crossentropy',optimizer=optimizer,metrics=['accuracy'])

model.summary()

from sklearn.model_selection import train_test_split
trainX, testX, trainy, testy = train_test_split(padded, yLE, test_size=0.25, random_state=1000)

history=model.fit(trainX, trainy, epochs=20, validation_data=(testX,testy))

yLE.shape

trainX.shape

trainy.shape

