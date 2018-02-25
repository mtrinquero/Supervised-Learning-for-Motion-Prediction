# Mark Trinquero
# AI for Robotics - Movement Predictor 

import os
import math
import pickle
import argparse
import numpy as np
import pandas as pd
from numpy import genfromtxt
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

test_idx_start = 1740
prod_idx_start = 1800

root = os.path.dirname(os.path.realpath(__file__))
unparsed_training_path = root + '/training_data.txt'
parsed_training_path = root + '/training.data'

parser = argparse.ArgumentParser(description="AI for Robotics - Movement Predictor")
parser.add_argument("input_file", type=str)
parser.add_argument("--test", help="Test mode", type=bool, default=False)
parser.add_argument("--pickle", help="Pickle training data", type=bool, default=False)
args = parser.parse_args()


def build_x_array(array, offset):
    # convert to pandas for vector processing
    df = pd.DataFrame(array)
    # add Euclidean distance
    df[2] = np.sqrt(((df[0]-df.shift(1)[0])**2) + ((df[1]-df.shift(1)[1])**2))
    # add heading
    df[3] = np.arctan2(df[1]-df.shift(1)[1], df[0]-df.shift(1)[0]) * 180 / math.pi
    # return df as numpy array
    if offset:
        return df[1:len(df)-1].values
    else:
        return df.values


def pickle_training_data():
    training_data = genfromtxt(fname=unparsed_training_path,dtype=float, delimiter=',')
    output = open(parsed_training_path, 'wb')
    pickle.dump(training_data, output)


if __name__ == '__main__':
    if args.pickle:
        pickle_training_data()
    idx_start = None
    if args.test:
        idx_start = test_idx_start
    else:
        idx_start = prod_idx_start
    training_input = open(parsed_training_path, 'rb')
    training_data = pickle.load(training_input)
    training_x = build_x_array(training_data, True)
    training_y = training_data[2:]
    test_data = genfromtxt(fname=args.input_file, dtype=float, delimiter=',')
    extra_training = test_data[:idx_start]
    enhanced_x = np.vstack((training_x, build_x_array(extra_training, True)))
    enhanced_y = np.vstack((training_y, extra_training[2:]))
    estimator = KNeighborsRegressor(n_neighbors=14, weights='distance', algorithm='brute')
    estimator.fit(enhanced_x, enhanced_y)
    test_x = build_x_array(test_data, False)[idx_start - 1]
    prediction = np.rint(estimator.predict(test_x))
    test_x = np.vstack((test_x, np.append(prediction, [0, 0])))
    # Calculate next 60 frames of movement
    for p in range(1, 60):
            test_x = build_x_array(test_x, offset=False)

            x_hat = test_x[p]

            y_hat = np.rint(estimator.predict(x_hat))

            prediction = np.vstack((prediction, y_hat))
            test_x = np.vstack((test_x, np.append(y_hat, [0, 0])))

    np.savetxt('prediction.txt', prediction, delimiter=',', fmt='%d')







