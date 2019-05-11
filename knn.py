# -*- coding: utf-8 -*-
"""Example of using kNN for outlier detection
"""
# Author: Yue Zhao <zhaoy@cmu.edu>
# License: BSD 2 clause

from __future__ import division
from __future__ import print_function

import os
import sys
import json
import pprint

# temporary solution for relative imports in case pyod is not installed
# if pyod is installed, no need to use the following line
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname("__file__"), '..')))

from pyod.models.knn import KNN
from pyod.utils.data import generate_data
from pyod.utils.data import evaluate_print
from pyod.utils.example import visualize



def str_to_num(string, form, maps):
    ik = f'{form}_iter'
    mk = f'{form}_map'
    rk = f'{form}_rmap'
    if string not in maps[rk]:
        maps[mk][maps[ik]] = string
        maps[rk][string] = maps[ik]
        maps[ik] += 1
    return maps[rk][string]


if __name__ == "__main__":
    contamination = 0.1  # percentage of outliers
    n_train = 200  # number of training points
    n_test = 100  # number of testing points

    # Generate sample data
    X_train, y_train, X_test, y_test = \
        generate_data(n_train=n_train,
                      n_test=n_test,
                      n_features=2,
                      contamination=contamination,
                      random_state=42)
    #print(X_train)
    #print(len(X_train))
    #print(y_train)
    #print(len(y_train))

    maps = {
            'cmd_iter': 1,
            'cmd_map': {},
            'cmd_rmap': {},
            'user_iter': 1,
            'user_map': {},
            'user_rmap': {},
            'id_iter': 1,
            'id_map': {},
            'id_rmap': {},
            }
    X_train = []
    X_test = []
    y_test = []
    y_train = []
    cmd_map = {}
    user_map = {}
    counter = 0
    with open('shell_beacon.json', 'r') as rfh:
        data = json.loads(rfh.read())
    for ev in data:
        counter += 1
        check = [
                str_to_num(ev['data']['user'], 'user', maps),
                str_to_num(ev['data']['cmd'], 'cmd', maps),
                str_to_num(ev['data']['id'], 'id', maps)
                ]
        if not counter % 5:
            X_test.append(check)
            y_test.append(0.0)
        else:
            X_train.append(check)
            y_train.append(0.0)
    #import pprint
    #pprint.pprint(maps)

    # train kNN detector
    clf_name = 'KNN'
    clf = KNN(radius=3)
    clf.fit(X_train)

    # get the prediction labels and outlier scores of the training data
    y_train_pred = clf.labels_  # binary labels (0: inliers, 1: outliers)
    y_train_scores = clf.decision_scores_  # raw outlier scores

    # get the prediction on the test data
    y_test_pred = clf.predict(X_test)  # outlier labels (0 or 1)
    found = 0
    for ind in range(len(y_test_pred)):
        if not y_test_pred[ind]:
            continue
        outlie = X_test[ind]
        user = maps['user_map'][outlie[0]]
        cmd = maps['cmd_map'][outlie[1]]
        id_ = maps['id_map'][outlie[2]]
        print(f'User: {user}; ID: {id_}, Cmd: {cmd}')
        found += 1
    print(f'Found: {found}')
