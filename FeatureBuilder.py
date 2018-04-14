#!/usr/bin/env python3

import argparse
import pandas as pd
import numpy as np

import xgboost as xgb

from sklearn.feature_extraction.text import CountVectorizer
from scipy.spatial.distance import hamming


def main():

    parser = argparse.ArgumentParser(
        description="Feature Builder")
    parser.add_argument("stances_dataset", metavar="stances_dataset",
                        help="Stances dataset.")
    parser.add_argument("bodies_dataset", metavar="bodies_dataset",
                        help="Bodies dataset.")
    parser.add_argument("output_file", metavar="output_file",
                        help="Output file.")
    args = parser.parse_args()

    df_stances = pd.read_csv(args.stances_dataset)
    df_bodies = pd.read_csv(args.bodies_dataset)

    df = pd.merge(df_stances, df_bodies, on="Body ID", how="left")

    for idx, row in df.iterrows():

        vec = CountVectorizer(binary=True)
        text = row["Headline"] + " " + row["articleBody"]
        vec.fit([text])

        print(vec.vocabulary_)

        heading = vec.transform([row["Headline"]])
        article = vec.transform([row["articleBody"]])

        assert(heading.shape == article.shape)

        # X = np.vstack((heading.toarray(), article.toarray()))
        # print(X)

        dist = hamming(heading.toarray(), article.toarray())
        print(dist)

        break


# dtrain = xgb.DMatrix(X_train, label=y_train)
# dtest = xgb.DMatrix(X_test, label=y_test)

# param = {
#     'max_depth': 3,  # the maximum depth of each tree
#     'eta': 0.3,  # the training step for each iteration
#     'silent': 1,  # logging mode - quiet
#     'objective': 'multi:softprob',  # error evaluation for multiclass training
#     'num_class': 3}  # the number of classes that exist in this datset
# num_round = 20  # the number of training iterations

# bst = xgb.train(param, dtrain, num_round)

# preds = bst.predict(dtest)


if __name__ == "__main__":
    main()
