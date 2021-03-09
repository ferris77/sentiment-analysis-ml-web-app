# -*- coding: utf-8 -*-
"""sentiment-analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RR_rbz0N3MdLh5NpfgtM6uNPfgEUcjiE

Vamos criar um modelo para analisar avaliações feitas por usuários a filmes conforme dataset do IMDB disponível em http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz.

Etapa 1: Acessar e extrair os dados do dataset

# Etapa 1

Criar um diretório chamado data para salvar os arquivos disponíveis no link. Baixar os arquivos no diretório criado usando o comando !wget -O (download and save under specific name) e descompactar usando !tar -zxf (unzip and extract from file).
"""

# Commented out IPython magic to ensure Python compatibility.
# %mkdir ../data
#!wget -O ../data/aclImdb_v1.tar.gz http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz
#!tar -zxf ../data/aclImdb_v1.tar.gz -C ../data

"""# Etapa 2

Preparar e preprocessar os dados. O dataset está dividido em dois subconjuntos de teste e treino. Cada subconjunto tem duas pastas, 'neg' e 'pos', de acordo com o tipo de avaliação.
"""

import os
import glob

test_neg_path = '/data/aclImdb/test/neg/'
test_neg_review = []
test_neg_sentiment = []

for filename in glob.glob(os.path.join(test_neg_path, '*.txt')):
  with open(os.path.join(os.getcwd(), filename), 'r') as f:
    test_neg_review.append(f.read())
    test_neg_sentiment.append(0)

test_pos_path = '/data/aclImdb/test/pos/'
test_pos_review = []
test_pos_sentiment = []

for filename in glob.glob(os.path.join(test_pos_path, '*.txt')):
  with open(os.path.join(os.getcwd(), filename), 'r') as f:
    test_pos_review.append(f.read())
    test_pos_sentiment.append(1)

train_neg_path = '/data/aclImdb/train/neg/'
train_neg_review = []
train_neg_sentiment = []

for filename in glob.glob(os.path.join(train_neg_path, '*.txt')):
  with open(os.path.join(os.getcwd(), filename), 'r') as f:
    train_neg_review.append(f.read())
    train_neg_sentiment.append(0)

train_pos_path = '/data/aclImdb/train/pos/'
train_pos_review = []
train_pos_sentiment = []

for filename in glob.glob(os.path.join(train_pos_path, '*.txt')):
  with open(os.path.join(os.getcwd(), filename), 'r') as f:
    train_pos_review.append(f.read())
    train_pos_sentiment.append(1)

from sklearn.utils import shuffle

data_train = train_pos_review + train_neg_review
data_test = test_pos_review + test_neg_review

labels_train = train_pos_sentiment + train_neg_sentiment
labels_test = test_pos_sentiment + test_neg_sentiment

train_X, train_y = shuffle(data_train, labels_train)
test_X, test_y = shuffle(data_test, labels_test)

print(f'IMDb review (combined): train = {len(train_pos_review)} pos and {len(train_neg_review)} neg \n'+
                                f'test = {len(test_pos_review)} pos and test = {len(test_neg_review)} neg.')

print(f'IMDb review (combined): train = {len(train_X)} test = {len(test_X)}.')

"""Agora que já temos os dois datasets para treino e teste, precisamos preprocessar os dados. Como é possível ver do exemplo impresso acima, alguns comentários terão formatação HTML ou alfanuméricos desnecessários. Vamos remover todos esses caracteres."""

import re

for i in range(len(train_X)):
  train_X[i] = re.sub('(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])', "", train_X[i])
  train_X[i] = re.sub('(<br\s*/><br\s*/>)|(\-)|(\/)', " ", train_X[i])
  test_X[i] = re.sub('(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])', "", test_X[i])
  test_X[i] = re.sub('(<br\s*/><br\s*/>)|(\-)|(\/)', " ", test_X[i])

"""Após limpar os datasets, vamos extrair as caracterísicas de cada review usando a abordagem com Bag-Of-Words."""

train_X[1]

train_y[1]

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import joblib

vectorizer = CountVectorizer(max_features=5000)

features_train = vectorizer.fit_transform(train_X).toarray()
features_test = vectorizer.transform(test_X).toarray()
vocabulary = vectorizer.vocabulary_

"""# Etapa 3

Vamos iniciar a criação do modelo de classificação, uma vez que já temos representação das características do dataset armazenadas.
"""

train_X, test_X = features_train, features_test

"""Vamos considerar as primeiras 10k reviews para validação e o restante para treino"""

import pandas as pd

val_X = pd.DataFrame(train_X[:10000])
train_X = pd.DataFrame(train_X[10000:])

val_y = pd.DataFrame(train_y[:10000])
train_y = pd.DataFrame(train_y[10000:])

import numpy as np
import pandas as pd
import re
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
import xgboost as xgb
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
import os

features_train = features_train[:20000]
features_train.shape

model = xgb.XGBClassifier(objective='reg:logistic')

#BOW_XGB_scores = cross_val_score(BOW_XGB, features_train, train_y, cv=3, n_jobs=-1)
#print(f"Averaged CV accuracy: {BOW_XGB_socores.mean()}")

model

# Commented out IPython magic to ensure Python compatibility.
# %time model.fit(train_X, train_y, eval_metric=["auc","error"], eval_set=[(train_X, train_y), (val_X, val_y)], verbose=False)

import joblib
joblib.dump(model, 'model.pkl')

test_X = pd.DataFrame(test_X)
test_y = pd.DataFrame(test_y)

from sklearn.metrics import classification_report

pred_test = model.predict(test_X)
pred_train = model.predict(train_X)

print('Train accuracy: ', accuracy_score(train_y, pred_train))
print('Test accuracy: ', accuracy_score(test_y, pred_test))

print('Classification Report:')
print(classification_report(test_y, pred_test))

test_review = 'As the main guy Boss Level, he delivered an outstanding performance. His blasé deadpan attitude was very funny - after all he is a guy who was just over it, starting each day, dying, rinse and repeat,'

test_review = re.sub('(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])', "", test_review)
test_review = re.sub('(<br\s*/><br\s*/>)|(\-)|(\/)', " ", test_review)
test_review

bow = [0] * len(vocabulary)
for word in test_review.split():
  if word in vocabulary:
    bow[vocabulary[word]] += 1
review_bow = bow

review_bow = pd.DataFrame(review_bow).T
review_bow

model.predict(review_bow)

# retrieve performance metrics
import matplotlib.pyplot as plt 
results = model.evals_result()
epochs = len(results['validation_0']['error'])
x_axis = range(0, epochs)
fig, ax = plt.subplots(1, 2, figsize=(15,5))
# plot auc
ax[0].plot(x_axis, results['validation_0']['auc'], label='Train')
ax[0].plot(x_axis, results['validation_1']['auc'], label='Test')
ax[0].legend()
ax[0].set_title('XGBoost AUC-ROC')
ax[0].set_ylabel('AUC-ROC')
ax[0].set_xlabel('N estimators')
# plot classification error
ax[1].plot(x_axis, results['validation_0']['error'], label='Train')
ax[1].plot(x_axis, results['validation_1']['error'], label='Test')
ax[1].legend()
ax[1].set_title('XGBoost Classification Error')
ax[1].set_ylabel('Classification Error')
ax[1].set_xlabel('N estimators')
plt.show()
plt.tight_layout()

