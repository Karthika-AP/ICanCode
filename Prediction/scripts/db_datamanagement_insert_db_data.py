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
    sql = """CREATE TABLE test.temps (sino INT, no_of_req INT, int_testcases INT, uat_testcases INT, mo_testcases INT, prod_testcases INT, no_of_browsers INT, effort_to_fix_defect INT, complexity_of_defect_fix INT, design_review_comments INT, cost_to_fix_defect INT, impact_of_defect_fix INT, bg_severity INT, bg_priority INT, defect_count INT)"""
    cursor.execute(sql)
    query = """INSERT INTO test.temps (sino, no_of_req, int_testcases, uat_testcases, mo_testcases , prod_testcases, no_of_browsers, effort_to_fix_defect, complexity_of_defect_fix, design_review_comments, cost_to_fix_defect, impact_of_defect_fix, bg_severity, bg_priority, defect_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    for r in range(1, sheet.nrows):
        sino = sheet.cell(r,0).value
        no_of_req = sheet.cell(r,1).value
        int_testcases = sheet.cell(r,2).value
        uat_testcases = sheet.cell(r,3).value
        mo_testcases = sheet.cell(r,4).value
        prod_testcases = sheet.cell(r,5).value
        no_of_browsers = sheet.cell(r,6).value
        effort_to_fix_defect = sheet.cell(r,7).value
        complexity_of_defect_fix = sheet.cell(r,8).value
        design_review_comments = sheet.cell(r,9).value
        cost_to_fix_defect = sheet.cell(r,10).value
        impact_of_defect_fix = sheet.cell(r,11).value
        bg_severity = sheet.cell(r,12).value
        bg_priority = sheet.cell(r,13).value
        defect_count = sheet.cell(r,14).value 
        values = (sino, no_of_req, int_testcases, uat_testcases, mo_testcases , prod_testcases, no_of_browsers, effort_to_fix_defect, complexity_of_defect_fix, design_review_comments, cost_to_fix_defect, impact_of_defect_fix, bg_severity, bg_priority, defect_count)
        cursor.execute(query, values)

    cursor.close()
    database.commit()
    database.close()

