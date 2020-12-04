import os
import mysql.connector 
from xlsxwriter.workbook import Workbook
from django.conf import settings

basepath=str(settings.BASE_DIR)

def db(db):
        database = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='test')
        cursor = database.cursor()
        
        query = """SELECT * FROM test.temps"""
        cursor.execute(query)
        yamlpath = '/Main/static/ICanCode/documents/Downloaded_Data/'+db+'.xlsx'
        path = basepath + yamlpath
        workbook = Workbook(path)
        sheet = workbook.add_worksheet('Sheet1')
        sheet.write('A1','sino')
        data=list(cursor.fetchall())
        length=len(data)
        sheet.write('A1','sino')
        sheet.write('B1','month')
        sheet.write('C1','day')
        sheet.write('D1','temp_2')
        sheet.write('E1','temp_1')
        sheet.write('F1','average')
        sheet.write('G1','actual')
        sheet.write('H1','forecast_noaa')
        sheet.write('I1','forecast_acc')
        sheet.write('J1','forecast_under')
        sheet.write('K1','friend')
        a,b,c,d,e,f,g,h,i,j,k,l = 1,0,1,2,3,4,5,6,7,8,9,10
        
        for sino, month, day, temp_2, temp_1, average, actual, forecast_noaa, forecast_acc, forecast_under, friend in data:
                sheet.write(a, b, sino)
                sheet.write(a, c, month)
                sheet.write(a, d, day)
                sheet.write(a, e, temp_2)
                sheet.write(a, f, temp_1)
                sheet.write(a, g, average)
                sheet.write(a, h, actual)
                sheet.write(a, i, forecast_noaa)
                sheet.write(a, j, forecast_acc)
                sheet.write(a, k, forecast_under)
                sheet.write(a, l, friend)
                a=a+1

        workbook.close()
        cursor.close()
        database.commit()
        database.close()
