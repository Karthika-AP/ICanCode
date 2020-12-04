import xlrd
import mysql.connector 
import os
from django.conf import settings

basepath=str(settings.BASE_DIR)


def db(db):    
    yamlpath = '/ICanCode/media/Uploaded_Data/'+db+'.xlsx'
    path = basepath + yamlpath
    book = xlrd.open_workbook(path)
    sheet = book.sheet_by_name("Sheet1")
    
    database = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='test')
    cursor = database.cursor()
    cursor.execute("DROP TABLE IF EXISTS test.temps")
    sql = """CREATE TABLE test.temps (sino INT, month INT, day INT, temp_2 INT, temp_1 INT, average INT, actual INT, forecast_noaa INT, forecast_acc INT, forecast_under INT, friend INT)"""
    cursor.execute(sql)
    query = """INSERT INTO test.temps (sino, month, day, temp_2, temp_1, average, actual, forecast_noaa, forecast_acc, forecast_under, friend) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    for r in range(1, sheet.nrows):
        sino = sheet.cell(r,0).value
        month = sheet.cell(r,1).value
        day = sheet.cell(r,2).value
        temp_2 = sheet.cell(r,3).value
        temp_1 = sheet.cell(r,4).value
        average = sheet.cell(r,5).value
        actual = sheet.cell(r,6).value
        forecast_noaa = sheet.cell(r,7).value
        forecast_acc = sheet.cell(r,8).value
        forecast_under = sheet.cell(r,9).value
        friend = sheet.cell(r,10).value    
        values = (sino, month, day, temp_2, temp_1, average, actual, forecast_noaa, forecast_acc, forecast_under, friend)
        cursor.execute(query, values)


    cursor.close()
    database.commit()
    database.close()

