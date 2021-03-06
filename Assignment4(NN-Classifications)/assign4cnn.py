# -*- coding: utf-8 -*-
"""Assign4CNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bObK8Oa3pDZdcu9L0raV-ITwxEj0xgCg

##Ingest
"""

import numpy as np
import pandas as pd
import string

df=pd.read_json('News_Category_Dataset_v2.json',lines=True)

"""##Preprocessing"""



df['category'].unique()

lis=[ 'WORLD NEWS',
       'SPORTS', 'MONEY',
       'WOMEN','SCIENCE']

df=df.loc[df['category'].isin(lis)]

df=df.reset_index(drop=True)

df["text"] = df["headline"] + df["short_description"]

df['text'][1]

df

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

df



from collections import Counter
Counter(df['category'])

"""##TF-IDF"""

from sklearn.feature_extraction.text import TfidfVectorizer
tv=TfidfVectorizer()
X=tv.fit_transform(df['Nonum'])
print(X.shape)

df3=pd.DataFrame(X.toarray(),columns=tv.get_feature_names())

df3.head()

categories=df['category']

"""#CNN"""

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D, Conv1D, MaxPooling1D
import pickle

x=df3.values

y=categories.values

y

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

yLE = le.fit_transform(y)

yLE

yLE = np.asarray( tf.keras.utils.to_categorical(yLE))

yLE

from sklearn.model_selection import train_test_split
trainX, testX, trainy, testy = train_test_split(x, yLE, test_size=0.25, random_state=1000)

trainX.shape

from tensorflow.keras import regularizers

np.amax(trainX)

max_features =29535
embedding_dim =256


model = tf.keras.Sequential()
model.add(tf.keras.layers.Embedding(2, embedding_dim, 
                                    embeddings_regularizer = regularizers.l2(0.0005)))                                    

model.add(tf.keras.layers.Conv1D(128,3, activation='relu',\
                                 kernel_regularizer = regularizers.l2(0.0005),\
                                 bias_regularizer = regularizers.l2(0.0005)))                               


model.add(tf.keras.layers.GlobalMaxPooling1D())

model.add(tf.keras.layers.Dropout(0.5))

model.add(tf.keras.layers.Dense(5, activation='sigmoid',\
                                kernel_regularizer=regularizers.l2(0.001),\
                                bias_regularizer=regularizers.l2(0.001),))
                               
model.summary()


model.summary()
model.compile(loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True), optimizer='Nadam', metrics=["CategoricalAccuracy"])

epochs = 3
# Fit the model using the train and test datasets.
history = model.fit(trainX, trainy,validation_data= (testX,testy),epochs=epochs )