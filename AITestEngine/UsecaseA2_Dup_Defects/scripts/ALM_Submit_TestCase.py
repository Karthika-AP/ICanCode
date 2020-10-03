import yaml
import xlrd
from django.conf import settings
import re

basepath=settings.BASE_DIR
yamlpath = '/UsecaseA2_Dup_Defects/scripts/'
path = basepath + yamlpath
with open(path + 'UsecaseA2_Dup_Defects.yml', 'r') as ymlfile:
    cfg = yaml.load(ymlfile, yaml.Loader)



def ColumnSearch(idtoserach,filename,sessionid2):
  
    pathnew = basepath+cfg['paths']['fol']
    pathtest = pathnew + sessionid2 + '/testcaseupload/'

    columnlist=['QC Internal', 'Test Case Developer', 'Status', 'Test Case Priority', '1 Product', '2 Func Area','3 Component', 'Test Case Type', 'Fully Automatable?', 'Automation Level']

    list8=[]
    l2=[]
    for f in filename :
        c=0
        book = xlrd.open_workbook(pathtest+f)
        global rowref
        for sheet in book.sheets():
            if sheet.name == 'Sheet1':
                for row in range(sheet.nrows):
                    for column in range(sheet.ncols):
                        if (float(idtoserach) == sheet.cell(row, column).value):
                            if idtoserach not in l2:
                                l2.append(idtoserach)
                                c = c + 1
                                reqrow= row
          
            else:
                pass
            if c == 1:
                for i in columnlist:
                    for row in range(sheet.nrows):
                        for column in range(sheet.ncols):
                            if (i == sheet.cell(row, column).value):
                                reqcol=column
                                a=(sheet.cell(reqrow, reqcol).value)
                                try:
                                    float(a)
                                    list8.append(int(a))
                                except:
                                    regex = re.compile(r'[\n\r\t]')
                                    a = regex.sub(" ", a)
                                    list8.append(a)
                                
                return list8
            else:
                pass

