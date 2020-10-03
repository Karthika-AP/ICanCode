import xlrd
import string
from django.conf import settings
from nltk.corpus import stopwords
import re
import yaml
basepath=settings.BASE_DIR
yamlpath = '/UsecaseA2_Dup_Defects/scripts/'
path = basepath + yamlpath
with open(path + 'UsecaseA2_Dup_Defects.yml', 'r') as ymlfile:
    cfg = yaml.load(ymlfile, yaml.Loader)

stop_words = set(stopwords.words("english"))


def preProcessString(sentence):
    "This function returns the preprocessed string"
    processed_sentence = [j for j in sentence.lower().split() if j not in stop_words]
    untokenized_sentence = "".join([" " + j if not j.startswith("'") and j not in string.punctuation else j for j in processed_sentence]).strip()
    translator = str.maketrans('', '', string.punctuation)
    untokenized_sentence1 = untokenized_sentence.translate(translator)
    return untokenized_sentence1


def readTestCasesFromExcelFile(file_name,sessionid2):
    "This function reads testcases from excel file and writes it to text file"    
    path1= basepath+cfg['paths']['fol']+ sessionid2 + '/testcaseupload/'
    workbook = xlrd.open_workbook(path1+file_name)
    test_ref = []
    testname = []
    objective = []
    project_name = []
    sub_project_name = []
    pointSheets = workbook.sheet_names()
    try:
        listTestSheetNames = ['Sheet1']
        sheetName = None
        for i in listTestSheetNames:
            if (i in pointSheets):
                sheetName = i

        sheet = workbook.sheet_by_name(sheetName)  # open workdsheet by name
        # initialize parameters for reading
        num_rows = sheet.nrows  # gets the total number of rows in sheet
        num_cols = sheet.ncols  # gets the total number of columns in sheet

        g = globals()  # declare a global variable to create lists dynamically
        i = 0
        offsetRowIndex = None  # set offset from where you can start reading. Set offset = 1 to skip headers

        # index value of test step column        
        testStepColumnIndex = None
        testCaseDescriptionColumnIndex = None
        testCaseNameColumnIndex = None
        testCaseColumnIndex = None
        testRefColumnIndex = None
        testProjectNameColumnIndex = None
        testSubProjectNameColumnIndex = None
        
        listValuesToBeSearched = ['Test_ID', 'Test Name', 'Objective', 'Pre-Conditions (Design Steps)', 'Step Name (Design Steps)', 'Procedure (Design Steps)', 'QC Internal', 'Test Case Developer', 'Status', 'Test Case Priority', '1 Product', '2 Func Area', '3 Component', 'Test Case Type', 'Fully Automatable?', 'parent-id', 'Automation Level', 'Project (Parent Folder)', 'Project (Sub Folder)']
        count = 0
        rowNumberHeader = None
        for rownum1 in range(num_rows):
            row = sheet.row(rownum1)
            for colnum1 in range(num_cols):
                if (row[colnum1].value in listValuesToBeSearched):
                    count = count + 1
                if (count >= 3):
                    rowNumberHeader = rownum1
                    break
            else:
                continue
            break

        listTestSteps = ['Step Name (Design Steps)']
        listTestCase = ['Test Name']
        listTestCasename = ['Objective']
        listTestDescription = ['Procedure (Design Steps)']
        listTestCaseId = ['Test_ID']
        listTestRef= ['Test_ID']
        listTestProjectName = ['Project (Parent Folder)']
        listTestSubProjectName = ['Project (Sub Folder)']

        for colnum in range(num_cols):
            if sheet.cell(rowNumberHeader, colnum).value in listTestSteps:
                testStepColumnIndex = colnum
            if sheet.cell(rowNumberHeader, colnum).value in listTestDescription:
                testCaseDescriptionColumnIndex = colnum
            if sheet.cell(rowNumberHeader, colnum).value in listTestCasename:
                testCaseNameColumnIndex = colnum
            if sheet.cell(rowNumberHeader, colnum).value in listTestCase:
                testCaseColumnIndex = colnum
            if sheet.cell(rowNumberHeader, colnum).value in listTestCaseId:
                testCaseIDColumnIndex = colnum
            if sheet.cell(rowNumberHeader, colnum).value in listTestRef:
                testRefColumnIndex = colnum
                offsetRowIndex = rowNumberHeader + 1
            if sheet.cell(rowNumberHeader, colnum).value in listTestProjectName:
                testProjectNameColumnIndex = colnum
            if sheet.cell(rowNumberHeader, colnum).value in listTestSubProjectName:
                testSubProjectNameColumnIndex = colnum
        listscombined = []
        for rownum in range(offsetRowIndex, num_rows):
            try:
                 if sheet.cell(rownum, testStepColumnIndex).value =='Step 1':
                        i = i + 1
                        g['depth_{0}'.format(i)] = []

                        for colnum1 in range(num_cols):
                           if sheet.cell_type(rownum, colnum1) not in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):  # check if cell is empty, if not then append it to list
                              if (colnum1 == testCaseColumnIndex) or (colnum1 == testCaseDescriptionColumnIndex) or (colnum1 == testCaseNameColumnIndex):
                                 sentence = sheet.cell(rownum, colnum1).value
                                 stringSentence1 = sentence.encode('ascii', 'ignore')
                                 stringSentence2 = stringSentence1.decode("utf-8")
                                 cleanr = re.compile('<.*?>')
                                 stringSentence = re.sub(cleanr, '', stringSentence2)
                                 translator = str.maketrans('','',string.punctuation)
                                 punctuation_sentence = stringSentence.translate(translator)
                                 preprocessed_sentence = preProcessString(punctuation_sentence)
                                 g['depth_{0}'.format(i)].append(preprocessed_sentence)
                              if (colnum1 == testRefColumnIndex):
                                 sentence = sheet.cell(rownum, colnum1).value
                                 test_ref.append(sentence)
                              if (colnum1 == testCaseColumnIndex):
                                 sentence = sheet.cell(rownum, colnum1).value
                                 regex = re.compile(r'[\n\r\t]')
                                 sentence = regex.sub(" ", sentence)
                                 testname.append(sentence)
                              if (colnum1 == testCaseNameColumnIndex):
                                 sentence = sheet.cell(rownum, colnum1).value
                                 regex = re.compile(r'[\n\r\t]')
                                 sentence = regex.sub(" ", sentence)
                                 objective.append(sentence)
                              if (colnum1 == testProjectNameColumnIndex):
                                 sentence = sheet.cell(rownum, colnum1).value
                                 project_name.append(sentence)
                              if (colnum1 == testSubProjectNameColumnIndex):
                                 sentence = sheet.cell(rownum, colnum1).value
                                 sub_project_name.append(sentence)
                           else:
                              if (colnum1 == testRefColumnIndex):
                                 sentence = sheet.cell(rownum, colnum1).value
                                 test_ref.append(sentence)
                              '''if (colnum1 == testCaseColumnIndex):
                                 sentence = sheet.cell(rownum, colnum1).value = 'NULL'
                                 regex = re.compile(r'[\n\r\t]')
                                 sentence = regex.sub(" ", sentence)
                                 testname.append(sentence)
                              if (colnum1 == testCaseNameColumnIndex):
                                 sentence = sheet.cell(rownum, colnum1).value = 'NULL'
                                 regex = re.compile(r'[\n\r\t]')
                                 sentence = regex.sub(" ", sentence)
                                 objective.append(sentence)'''
                        listscombined.append(g['depth_{0}'.format(i)])                         
                 elif sheet.cell(rownum, testStepColumnIndex).value !='Step 1':
                        for colnum1 in range(num_cols):
                           if sheet.cell_type(rownum, colnum1) not in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):  # check if cell is empty, if not then append it to list
                              if (colnum1 == testCaseColumnIndex) or (colnum1 == testCaseDescriptionColumnIndex) or (colnum1 == testCaseNameColumnIndex):
                                 sentence = sheet.cell(rownum, colnum1).value
                                 stringSentence1 = sentence.encode('ascii', 'ignore')
                                 stringSentence2 = stringSentence1.decode("utf-8")
                                 cleanr = re.compile('<.*?>')
                                 stringSentence = re.sub(cleanr, '', stringSentence2)
                                 translator = str.maketrans('','',string.punctuation)
                                 punctuation_sentence = stringSentence.translate(translator)
                                 preprocessed_sentence = preProcessString(punctuation_sentence)
                                 g['depth_{0}'.format(i)].append(preprocessed_sentence)
            except KeyError:
                raise KeyError

        joinedlist=[]
        for i in listscombined:
            joinedlist.append(" ".join(i))
        return test_ref, testname, objective, project_name, sub_project_name, joinedlist
    
    except KeyError:
        raise KeyError    
    except IndexError:
        raise IndexError
    except TypeError:
        raise TypeError
    
