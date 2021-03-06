# -*- coding: utf-8 -*-
"""Copy of Alt Assign2MSDS453.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18ltVc770XSGsnRIkW4umU1WtjTU5PJrQ
"""

import numpy as np
import pandas as pd
import string

df=pd.read_json('News_Category_Dataset_v2.json',lines=True)

df

df=df.iloc[range(0,2000)]

somevalues=['CRIME', 'ENTERTAINMENT', 'WORLD NEWS',  'POLITICS','SPORTS', 'BUSINESS', 'TRAVEL', 'MEDIA', 'TECH', 'SCIENCE']

df=df.loc[df['category'].isin(somevalues)]

df=df.reset_index(drop=True)

def removePunct(txt):
  txt_nopunct="".join([c for c in txt if c not in string.punctuation])
  return txt_nopunct

df['textClean']=df['short_description'].apply(lambda x:removePunct(x))
df

df['category'].isnull().values.any()

import re

def tokenize(txt):
  tokens=re.split('\W+',txt)
  return tokens

df['textCleanToken']=df['textClean'].apply(lambda x:tokenize(x.lower()))
df.head()

df.index

import nltk
nltk.download('stopwords')
stopwords=nltk.corpus.stopwords.words('english')
stopwords[:10]

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

df.head()

"""##CountVec"""

from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer()
X=cv.fit_transform(df['Nonum'])
print(X.shape)

df2=pd.DataFrame(X.toarray(),columns=cv.get_feature_names())
df2.head()

scorep1=X.nnz / float(X.shape[0])
scorep1

scorep1/float(X.shape[1])

"""##TF-IDF"""

from sklearn.feature_extraction.text import TfidfVectorizer
tv=TfidfVectorizer()
X=tv.fit_transform(df['Nonum'])
print(X.shape)

df3=pd.DataFrame(X.toarray(),columns=tv.get_feature_names())

df3.head()

scorep1=X.nnz / float(X.shape[0])
scorep1

"""##Doc2Vec"""

from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

from nltk.tokenize import word_tokenize

import nltk


nltk.download('punkt')
tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(df['Nonum'])]

tagged_data

max_epochs = 100
vec_size = 200
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

print(model.docvecs['1'])

len(model.docvecs['5'])

model.docvecs['5']

similar_doc = model.docvecs.most_similar('1')
print(similar_doc)

similar_doc2 = model.docvecs.most_similar('2')
print(similar_doc2)



"""##Random Forest"""

df

df2=df2.dropna()

df3=df3.dropna()

df['category']

df2['category']=df['category']

df2['category'].isnull().values.any()

df3['category']=df['category']

df3

"""##RandomForest

###Countvector
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(df2.drop(['category'],axis='columns'),df2.category,test_size=0.2)

rfcmodel=RandomForestClassifier()
rfcmodel.fit(x_train,y_train)

x_train

rfcmodel.score(x_test,y_test)

"""###TF-IDF"""

x_train, x_test, y_train, y_test = train_test_split(df3.drop(['category'],axis='columns'),df3.category,test_size=0.2)

rfcmodel=RandomForestClassifier()
rfcmodel.fit(x_train,y_train)

rfcmodel.score(x_test,y_test)

"""###Doc2Vec"""

nnvec=model.docvecs.vectors_docs

nnvec

nnvecdf = pd.DataFrame(nnvec)

nnvecdf['category'] = df['category']

nnvecdf['category'].isnull().values.any()

nnvecdf=nnvecdf.dropna()

nnvecdf['category'].isnull().values.any()

x_train, x_test, y_train, y_test = train_test_split(nnvecdf.drop(['category'],axis='columns'),nnvecdf.category,test_size=0.2)

rfcmodel=RandomForestClassifier()
rfcmodel.fit(x_train,y_train)

rfcmodel.score(x_test,y_test)

