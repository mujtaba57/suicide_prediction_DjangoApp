import os
import pickle

import joblib
import pandas as pd
from fyp_project.settings import MODEL_ROOT


def rfClassifier(data):
    UDataF = pd.DataFrame([[data]], columns=['text'])
    corpus = UDataF['text'].values
    vectorizer = joblib.load(os.path.join(MODEL_ROOT, 'RFvectorizer.joblib'))
    X = vectorizer.transform(corpus)

    Ucolumn = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
    loadModelData = pickle.load(open(os.path.join(MODEL_ROOT, 'Sucide_rfclassifier.pkl'), 'rb'))

    unseenPredictOutput = loadModelData.predict(Ucolumn)

    if unseenPredictOutput == 0:
        return "Non-Suicide"
    elif unseenPredictOutput == 1:
        return "Suicide"


def LRClassifier(data):
    UDataF = pd.DataFrame([[data]], columns=['text'])
    corpus = UDataF['text'].values
    vectorizer = joblib.load(os.path.join(MODEL_ROOT, 'LRvectorizer.joblib'))
    X = vectorizer.transform(corpus)

    Ucolumn = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
    loadModelData = pickle.load(open(os.path.join(MODEL_ROOT, 'LRClassifier.pkl'), 'rb'))

    unseenPredictOutput = loadModelData.predict(Ucolumn)

    if unseenPredictOutput == 0:
        return "Non-Suicide"
    elif unseenPredictOutput == 1:
        return "Suicide"


def GBClassifier(data):
    UDataF = pd.DataFrame([[data]], columns=['text'])
    corpus = UDataF['text'].values
    vectorizer = joblib.load(os.path.join(MODEL_ROOT, 'GBvectorizer.joblib'))
    X = vectorizer.transform(corpus)

    Ucolumn = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
    loadModelData = pickle.load(open(os.path.join(MODEL_ROOT, 'GBClassifier.pkl'), 'rb'))

    unseenPredictOutput = loadModelData.predict(Ucolumn)

    if unseenPredictOutput == 0:
        return "Non-Suicide"
    elif unseenPredictOutput == 1:
        return "Suicide"


def KNNClassifier(data):
    UDataF = pd.DataFrame([[data]], columns=['text'])
    corpus = UDataF['text'].values
    vectorizer = joblib.load(os.path.join(MODEL_ROOT, 'KNNvectorizer.joblib'))
    X = vectorizer.transform(corpus)

    Ucolumn = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
    loadModelData = pickle.load(open(os.path.join(MODEL_ROOT, 'KNNClassifier.pkl'), 'rb'))

    unseenPredictOutput = loadModelData.predict(Ucolumn)

    if unseenPredictOutput == 0:
        return "Non-Suicide"
    elif unseenPredictOutput == 1:
        return "Suicide"
