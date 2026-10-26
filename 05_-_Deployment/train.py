#!/usr/bin/env python
"""Train, evaluate, and save a customer churn prediction model."""

import pandas as pd
import numpy as np


from sklearn.metrics import roc_auc_score
from sklearn.model_selection import KFold, train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

import pickle


NUMERICAL = ['tenure', 'monthlycharges', 'totalcharges']

CATEGORICAL = [
    'gender',
    'seniorcitizen',
    'partner',
    'dependents',
    'phoneservice',
    'multiplelines',
    'internetservice',
    'onlinesecurity',
    'onlinebackup',
    'deviceprotection',
    'techsupport',
    'streamingtv',
    'streamingmovies',
    'contract',
    'paperlessbilling',
    'paymentmethod',
]


def load_data():
    """Load the churn dataset and normalize its columns and values."""
    data_url = 'https://raw.githubusercontent.com/k-candidate/mlbookcamp-code/master/chapter-03-churn-prediction/WA_Fn-UseC_-Telco-Customer-Churn.csv'

    df = pd.read_csv(data_url)

    # Normalize names and categorical values so feature keys are consistent.
    df.columns = df.columns.str.lower().str.replace(' ', '_')

    categorical_columns = list(df.dtypes[df.dtypes == 'str'].index)

    for c in categorical_columns:
        df[c] = df[c].str.lower().str.replace(' ', '_')

    # Blank total charges are treated as zero.
    df.totalcharges = pd.to_numeric(df.totalcharges, errors='coerce')
    df.totalcharges = df.totalcharges.fillna(0)

    # Encode churn as a binary target.
    df.churn = (df.churn == 'yes').astype(int)

    return df


def train_model(df):
    """Fit and return a preprocessing-and-classification pipeline."""
    y_train = df.churn
    train_dict = df[CATEGORICAL + NUMERICAL].to_dict(orient='records')

    pipeline = make_pipeline(
        DictVectorizer(sparse=False),
        LogisticRegression(
            solver='liblinear',
            C=1.0,
            max_iter=1000,
            random_state=42
        )
    )

    pipeline.fit(train_dict, y_train)

    return pipeline


def cross_validate_model(df, n_splits=5):
    """Return ROC AUC scores from shuffled K-fold validation."""
    kfold = KFold(n_splits=n_splits, shuffle=True, random_state=1)
    scores = []

    for train_idx, val_idx in kfold.split(df):
        df_train = df.iloc[train_idx]
        df_val = df.iloc[val_idx]

        pipeline = train_model(df_train)
        val_dict = df_val[CATEGORICAL + NUMERICAL].to_dict(orient='records')
        y_pred = pipeline.predict_proba(val_dict)[:, 1]

        auc = roc_auc_score(df_val.churn, y_pred)
        scores.append(auc)

    return scores


def save_model(pipeline, output_file):
    """Serialize the fitted pipeline to a binary file."""
    with open(output_file, 'wb') as f_out:
        pickle.dump(pipeline, f_out)



# Keep the test set out of cross-validation and model fitting for an unbiased final evaluation.
df = load_data()
df_full_train, df_test = train_test_split(df, test_size=0.2, random_state=1)

scores = cross_validate_model(df_full_train)
print('5-fold CV AUC: %.3f +- %.3f' % (np.mean(scores), np.std(scores)))

# Refit on all development data before evaluating and saving the final model.
pipeline = train_model(df_full_train)
test_dict = df_test[CATEGORICAL + NUMERICAL].to_dict(orient='records')
y_pred = pipeline.predict_proba(test_dict)[:, 1]
test_auc = roc_auc_score(df_test.churn, y_pred)
print('Test AUC: %.3f' % test_auc)

save_model(pipeline, 'model.bin')

print('Model saved to model.bin')
