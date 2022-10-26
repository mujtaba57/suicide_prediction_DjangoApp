import os
import pickle

import joblib
import pandas as pd
from fyp_project.settings import MODEL_ROOT


def get_prediction_rf(data, model_number):
    UDataF = pd.DataFrame([[data]], columns=['text'])
    corpus = UDataF['text'].values
    vectorizer = joblib.load(os.path.join(MODEL_ROOT, 'vectorizer.joblib'))
    X = vectorizer.transform(corpus)

    Ucolumn = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
    loadModelData = pickle.load(open(os.path.join(MODEL_ROOT, 'Sucide_rfclassifier.pkl'), 'rb'))

    unseenPredictOutput = loadModelData.predict(Ucolumn)

    if unseenPredictOutput == 0:
        return "Non-Suicide"
    elif unseenPredictOutput == 1:
        return "Suicide"



