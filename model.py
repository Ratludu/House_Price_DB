import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold
from sklearn.linear_model import ElasticNet

df = pd.read_csv("all_perth_310121.csv")

df = df[["BEDROOMS", "BATHROOMS", "GARAGE","PRICE"]]

df = df.dropna()

df = pd.get_dummies(df)

X,y = df.drop(columns = ["PRICE"]), df["PRICE"]

model = ElasticNet(alpha=0.1, l1_ratio=0.5)

cv = RepeatedKFold(n_splits=10, n_repeats=1, random_state=1)

model.fit(X,y)

def price_prediction(bedrooms, bathrooms, garage):
    return model.predict([[bedrooms, bathrooms, garage]])




