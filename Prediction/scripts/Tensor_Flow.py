# -*- coding: cp1252 -*-
import math
import numpy as numpy
from . import common_utils

from pandas import DataFrame
from sklearn.svm import SVR

import os
import yaml
from pandas import DataFrame
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd
from django.conf import settings

basepath=str(settings.BASE_DIR)
yamlpath = '/Prediction/scripts/'
path = basepath  + yamlpath
with open(path + 'uc1.yml', 'r') as ymlfile:
    cfg = yaml.load(ymlfile)


def predict_dc(tablename, col):


    "This function predicts actual value to be predicted"
    cnx = common_utils.getConnection()
    cols = col
    strColumns = ','.join(cols)
    query = "select " + strColumns + " from " + tablename + " "
    try:

        cursor = cnx.cursor()
        cursor.execute(query)
        data = DataFrame(cursor.fetchall())
        print(data)

    finally:
        cnx.close()

    train_dataset = data[:-1]
    print(train_dataset)
    test_dataset = data.drop(train_dataset.index)
    print(test_dataset)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    len1 = (len(test_dataset.columns))
    print(len1)

    train_stats = train_dataset.describe()
    train_stats.pop(len1 - 1)
    train_stats = train_stats.transpose()
    print(train_stats)
    train_labels = train_dataset.pop(len1 - 1)
    print(train_labels)
    test_labels = test_dataset.pop(len1 - 1)
    print(test_labels)

    def norm(x):
        return (x - train_stats['mean']) / train_stats['std']

    normed_train_data = norm(train_dataset)
    print("normed_train_data")
    print(normed_train_data)
    normed_test_data = norm(test_dataset)
    print("normed_test_data")
    print(normed_test_data)

    # print ("@@@@@@@@@@@@@@@@@@@@@@@@@@@2")
    # print (normed_test_data)
    def build_model():
        model = keras.Sequential([
            layers.Dense(64, activation=tf.nn.sigmoid, input_shape=[len(train_dataset.keys())]),
            layers.Dense(64, activation=tf.nn.sigmoid),
            layers.Dense(1)
        ])

        optimizer = tf.train.RMSPropOptimizer(0.001)

        model.compile(loss='mse',
                      optimizer=optimizer,
                      metrics=['mae', 'mse'])
        return model

    model = build_model()

    # print (model.summary())

    # example_batch = normed_train_data[:10]
    # example_result = model.predict(example_batch)
    # print (example_result)

    # Display training progress by printing a single dot for each completed epoch
    class PrintDot(keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs):
            if epoch % 100 == 0: a = 1  # print(epoch)
            b = 1  # print('', end='')

    EPOCHS = 1000

    history = model.fit(
        normed_train_data, train_labels,
        epochs=EPOCHS, validation_split=0.1, verbose=0,
        callbacks=[PrintDot()])

    hist = pd.DataFrame(history.history)
    hist['epoch'] = history.epoch
    hist.tail()

    model = build_model()

    # The patience parameter is the amount of epochs to check for improvement
    early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=50)

    history = model.fit(normed_train_data, train_labels, epochs=EPOCHS,
                        validation_split=0.2, verbose=0, callbacks=[early_stop, PrintDot()])

    loss, mae, mse = model.evaluate(normed_test_data, test_labels, verbose=0)

    print("Testing set Mean Abs Error: {:5.2f} units".format(mae))
    # print (normed_test_data)
    test_predictions = model.predict(normed_test_data).flatten()
    print("Actual Results:" + str(test_labels.values[0]))
    print("Predicted Result" + str(test_predictions))

    #test_predictions = [int(round(test_predictions/ test_dataset.pop(0), 0))]
    return test_predictions
#print(predict_dc())

def graph_data(tablename, col, predict_col):
    "This function generates graph data, ucl, lcl"
    cnx = common_utils.getConnection()
    cols = predict_col[1]
    query = "select " + cols + " from " + tablename + " "
    data1 = []
    data2 = []
    data3 = []
    data1_d = []
    data2_d = []
    data3_d = []
    ucl = []
    lcl = []
    rel = []
    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        for x in data:
            x = str(x)
            data1.append(x.replace(',', ''))
        for x in data1:
            x = str(x)
            data2.append(x.replace('(', ''))
        for x in data2:
            x = str(x)
            data3.append(x.replace(')', ''))
        length = len(data2)
        predic_rel = data2[length - 1]
        rel.append(predic_rel.replace(')', ''))
        rel1 = str(rel[0])
        red_id = int(rel1) + 1
        data3.append(red_id)
        Relid = data3[:]
        cols = predict_col[0]
        query = "select " + cols + " from " + tablename + " "
        cursor = cnx.cursor()
        cursor.execute(query)
        data_dd = cursor.fetchall()
        ucl1, lcl1 = predict_ucllcl(data_dd)
        for y in data_dd:
            y = str(y)
            data1_d.append(y.replace(',', ''))
        for y in data1_d:
            y = str(y)
            data2_d.append(y.replace('(', ''))
        for y in data2_d:
            y = str(y)
            data3_d.append(y.replace(')', ''))
        graph_data = data3_d[:]
    finally:
        cnx.close()
    predicted_result = predict_dc(tablename, col)
    predicted_result = str(predicted_result)
    pred = predicted_result.replace('[', '')
    pred1 = pred.replace(']', '')
    graph_data.append(pred1)
    for x in graph_data:
        ucl.append(ucl1)
        lcl.append(lcl1)
    return Relid, graph_data, ucl, lcl


def predict_ucllcl(mydata):
    "This function generates ucl, lcl"
    data_set = mydata
    i = len(data_set)
    average = numpy.mean(data_set, axis=0)
    s = [x - average for x in data_set]
    square = [x * x for x in s]
    avg_new = 0
    for x in square:
        avg_new = x + avg_new
    varience = avg_new / i
    sigma = math.pow(varience, 0.5)
    three_sigma = 3 * sigma
    ucl = average + three_sigma
    lcl = average - three_sigma
    ucl = int(numpy.round(ucl, 0))
    if lcl < 0:
        lcl = 0
    else:
        lcl = int(numpy.round(lcl))
    return ucl, lcl


def last_prediction(tablename, tablenamelp, predict_col):
    cnx = common_utils.getConnection()
    query = "select * from " + tablenamelp
    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
    finally:
        cnx.close()
    Rel_Id = []
    Actual = []
    Linear = []
    cols = predict_col[0]
    cnx = common_utils.getConnection()
    query = "select " + cols + " from " + tablename + " "
    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        data_data = cursor.fetchall()
    finally:
        cnx.close()
    
    i = 0
    print(data)
    for relid, actual, linear in data:
        if (i < (len(data))):
            Rel_Id.append(relid)
            Actual.append(actual)
            Linear.append(linear)
        i = i + 1
    return Rel_Id, Actual, Linear
