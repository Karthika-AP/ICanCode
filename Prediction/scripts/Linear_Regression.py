import math
import numpy as numpy
from . import common_utils
from pandas import DataFrame
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn import metrics
import os
import yaml
from django.conf import settings
from sklearn import ensemble


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

    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2, random_state = 0)
    print("x_train")
    print(x_train)
    print("x_test")
    print(x_test)
    print("y_train")
    print(y_train)
    print("y_test")
    print(y_test)
    
    lm = LinearRegression() # Linear Regression
    lm.fit(x_train, y_train)
    
    result=lm.predict(test_data)
    print(result)
    final_result=result.clip(0)
    print(final_result)

    # https://github.com/KhanradCoder/LearnMachineLearning/blob/master/1_Regression.ipynb
    
    return final_result


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
        print("graph_data")
        print(graph_data)
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
