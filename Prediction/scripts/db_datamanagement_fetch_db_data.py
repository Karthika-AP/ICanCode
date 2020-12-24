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
        sheet.write('B1','no_of_req')
        sheet.write('C1','int_testcases')
        sheet.write('D1','uat_testcases')
        sheet.write('E1','mo_testcases')
        sheet.write('F1','prod_testcases')
        sheet.write('G1','no_of_browsers')
        sheet.write('H1','effort_to_fix_defect')
        sheet.write('I1','complexity_of_defect_fix')
        sheet.write('J1','design_review_comments')
        sheet.write('K1','cost_to_fix_defect')
        sheet.write('L1','impact_of_defect_fix')
        sheet.write('M1','bg_severity')
        sheet.write('N1','bg_priority')
        sheet.write('O1','defect_count')
        a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p = 1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14
        
        for sino, no_of_req, int_testcases, uat_testcases, mo_testcases, prod_testcases, no_of_browsers, effort_to_fix_defect, complexity_of_defect_fix, design_review_comments, cost_to_fix_defect, impact_of_defect_fix, bg_severity, bg_priority, defect_count in data:
                sheet.write(a, b, sino)
                sheet.write(a, c, no_of_req)
                sheet.write(a, d, int_testcases)
                sheet.write(a, e, uat_testcases)
                sheet.write(a, f, mo_testcases)
                sheet.write(a, g, prod_testcases)
                sheet.write(a, h, no_of_browsers)
                sheet.write(a, i, effort_to_fix_defect)
                sheet.write(a, j, complexity_of_defect_fix)
                sheet.write(a, k, design_review_comments)
                sheet.write(a, l, cost_to_fix_defect)
                sheet.write(a, m, impact_of_defect_fix)
                sheet.write(a, n, bg_severity)
                sheet.write(a, o, bg_priority)
                sheet.write(a, p, defect_count)
                a=a+1

        workbook.close()
        cursor.close()
        database.commit()
        database.close()
