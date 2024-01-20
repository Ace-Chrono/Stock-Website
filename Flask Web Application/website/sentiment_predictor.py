##Exit powershell if giving that weird error where only f5 works
from scraper import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
##from wordcloud import WordCloud, STOPWORDS
import nltk
import re
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
import plotly.express as px
##Tensorflow
import tensorflow as tf
from keras.preprocessing.text import one_hot,Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Flatten, Embedding, Input, LSTM, Conv1D, MaxPool1D, Bidirectional, Dropout
from keras.models import Model
from keras.utils import to_categorical

import string
string.punctuation

def remove_punc(message):
    Test_punc_removed = [char for char in message if char not in string.punctuation]
    Test_punc_removed_join = ''.join(Test_punc_removed)

    return Test_punc_removed_join

def preprocess(text):
    nltk.download("stopwords")
    stop_words = stopwords.words('english')
    stop_words.extend(['from', 'subject', 're', 'edu', 'use','will','aap','co','day','user','stock','today','week','year', 'https'])
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) >= 2 and token not in stop_words:
            result.append(token)
            
    return result

def predict_stock_sentiment(ticker):
    stock_df = pd.read_csv(r"C:\Users\richa_0\OneDrive\Documents\Stock Sentiment CSV's\stock_sentiment.csv")
    stock_df.isnull().sum()
    stock_df['Text Without Punctuation'] = stock_df['Text'].apply(remove_punc)
    stock_df['Text Without Punc & Stopwords'] = stock_df['Text Without Punctuation'].apply(preprocess)
    list_of_words = []
    for i in stock_df['Text Without Punc & Stopwords']:
        for j in i:
            list_of_words.append(j)
            
    total_words = len(list(set(list_of_words)))
    X = stock_df['Text Without Punc & Stopwords']
    y = stock_df['Sentiment']
    #from sklearn.model_selection import train_test_split
    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1)
    X_train = X
    X_test = getBloombergHeadlines(ticker)
    y_train = y
    tokenizer = Tokenizer(num_words = total_words) 
    tokenizer.fit_on_texts(X_train)
    train_sequences = tokenizer.texts_to_sequences(X_train)
    test_sequences = tokenizer.texts_to_sequences(X_test)
    padded_train = pad_sequences(train_sequences, maxlen = 29, padding = 'post', truncating = 'post')
    padded_test = pad_sequences(test_sequences, maxlen = 29, padding = 'post', truncating = 'post')
    y_train_cat = to_categorical(y_train, 2)
    model = Sequential()
    model.add(Embedding(total_words, output_dim = 512))
    model.add(LSTM(256))
    model.add(Dense(128, activation = 'relu'))
    model.add(Dropout(0.3))
    model.add(Dense(2,activation = 'softmax'))
    model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['acc'])
    model.fit(padded_train, y_train_cat, batch_size = 32, validation_split = 0.2, epochs = 2)
    pred = model.predict(padded_test)
    percent_positive = 0.0
    list_amount = 0
    for i in pred:
        for j in i:
            percent_positive += j[1]
            list_amount += 1
    percent_positive /= list_amount
    
    return percent_positive




    



