# -*- coding: cp1252 -*-
import math
import numpy as numpy
from . import common_utils
import os
import yaml
from pandas import DataFrame
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Dense
import pandas 
from django.conf import settings
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras import *

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
        data = DataFrame(cursor.fetchall(), columns=cols)
        print(data)
    finally:
        cnx.close()
    X = data[cols[:-1]]  # Gets the corelated data of past
    Y = data[cols[-1]]  # Gets the last column (the item to predict)
    print(X)
    print("***")
    print(Y)
    
    print("test_data")
    test_data = data[cols[:-1]][-1:]  # Stores the last row except the value to be predicted
    print(test_data)    
    test_data_new= test_data.to_numpy(dtype='int', na_value=0)

    model = Sequential()
    model.add(Dense(16, activation='relu', input_shape=(14,)))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X, Y, epochs=30, callbacks=[EarlyStopping(patience=3)])
    result=model.predict(test_data_new.reshape(1,14), batch_size=1).flatten()
    model.save('saved_model.h5')

    '''old_model = load_model('saved_model.h5')
    result = old_model.predict(test_data_new.reshape(1,14), batch_size=1)'''
  
    print(result)
    final_result=result.clip(0)
    print(final_result)

    # https://stackoverflow.com/questions/58150670/evaluation-of-an-ann-linear-regression-model
    
    return final_result


def graph_data(tablename, col, predict_col, predicted_data):
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
    predicted_result = str(predicted_data)
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
