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
    workbook = xlrd.open_workbook(path1 + file_name)

    test_ref = []
    summary = []
    description = []
    pname = []
    environment=[]
    assignee=[]
    priority=[]
    reporter=[]
    severity=[]
    try:
        pointSheets = workbook.sheet_names()
        listTestSheetNames = ['Sheet1']
        sheetName = None
        for i in listTestSheetNames:
            if (i in pointSheets):
                sheetName = i
        sheet = workbook.sheet_by_name(sheetName)  # open workdsheet by name
        num_rows = sheet.nrows  # gets the total number of rows in sheet
        num_cols = sheet.ncols  # gets the total number of columns in sheet
        g = globals()  # declare a global variable to create lists dynamically
        i = 0
        offsetRowIndex = 0  # set offset from where you can start reading. Set offset = 1 to skip headers

        DefectSummaryIDColumnIndex = None
        testCaseDescriptionColumnIndex = None
        testRefColumnIndex = None
        DefectProjectColumnIndex = None
        DefectEnvironmentColumnIndex = None
        DefectAssigneeColumnIndex = None
        DefectPriorityColumnIndex = None
        DefectReporterColumnIndex = None
        DefectSeverityColumnIndex = None

        listValuesToBeSearched = ['ID', 'SUMMARY', 'PNAME', 'ISSUETYPE', 'DESCRIPTION', 'ENVIRONMENT', 'ASSIGNEE', 'PRIORITY', 'REPORTER', 'SEVERITY']
        count = 0
        rowNumberHeader = 0
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
        listDefectSummary = ['SUMMARY']
        listTestDescription = ['DESCRIPTION']
        listTestRef = ['ID']
        listProject = ['PNAME']
        listEnvironment = ['ENVIRONMENT']
        listAssignee = ['ASSIGNEE']
        listPriority = ['PRIORITY']
        listReporter = ['REPORTER']
        listSeverity = ['SEVERITY']
        
        for colnum in range(num_cols):
            if (sheet.cell(rowNumberHeader, colnum).value in listTestDescription):
                testCaseDescriptionColumnIndex = colnum
            if (sheet.cell(rowNumberHeader, colnum).value in listDefectSummary):
                DefectSummaryIDColumnIndex = colnum
            if (sheet.cell(rowNumberHeader, colnum).value in listProject):
                DefectProjectColumnIndex = colnum
            if (sheet.cell(rowNumberHeader, colnum).value in listEnvironment):
                DefectEnvironmentColumnIndex = colnum
            if (sheet.cell(rowNumberHeader, colnum).value in listAssignee):
                DefectAssigneeColumnIndex = colnum
            if (sheet.cell(rowNumberHeader, colnum).value in listPriority):
                DefectPriorityColumnIndex = colnum
            if (sheet.cell(rowNumberHeader, colnum).value in listReporter):
                DefectReporterColumnIndex = colnum
            if (sheet.cell(rowNumberHeader, colnum).value in listSeverity):
                DefectSeverityColumnIndex = colnum
            if sheet.cell(rowNumberHeader, colnum).value in listTestRef:
                testRefColumnIndex = colnum
                offsetRowIndex = rowNumberHeader + 1
        listscombined = []
        for rownum in range(offsetRowIndex, num_rows):
          try:  
            i = i + 1
            g['depth_{0}'.format(i)] = []
            teststeps = []
            for colnum1 in range(num_cols):
                if sheet.cell_type(rownum, colnum1) not in (
                xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):  # check if cell is empty, if not then append it to list
                    if (colnum1 == testCaseDescriptionColumnIndex) or (colnum1 == DefectSummaryIDColumnIndex):
                        sentence = str(sheet.cell(rownum, colnum1).value)
                        stringSentence1 = sentence.encode('ascii', 'ignore')
                        stringSentence = stringSentence1.decode("utf-8")
                        cleantext=re.sub("[\[].*?[\]]","",stringSentence)
                        translator = str.maketrans('', '', string.punctuation)
                        punctuation_sentence = cleantext.translate(translator)
                        preprocessed_sentence = preProcessString(punctuation_sentence)
                        g['depth_{0}'.format(i)].append(preprocessed_sentence)
                        teststeps.append(preprocessed_sentence)
                    if (colnum1 == testRefColumnIndex):
                        sentence = sheet.cell(rownum, colnum1).value
                        test_ref.append(sentence)
                    if (colnum1 == DefectSummaryIDColumnIndex):
                        sentence = sheet.cell(rownum, colnum1).value
                        regex = re.compile(r'[\n\r\t]')
                        summary.append(sentence)
                    if (colnum1 == testCaseDescriptionColumnIndex):
                        sentence = sheet.cell(rownum, colnum1).value
                        regex = re.compile(r'[\n\r\t]')
                        description.append(sentence)
                    if (colnum1 == DefectProjectColumnIndex):
                        sentence = sheet.cell(rownum, colnum1).value
                        pname.append(sentence)
                    if (colnum1 == DefectEnvironmentColumnIndex):
                        sentence = sheet.cell(rownum, colnum1).value
                        environment.append(sentence)
                    if (colnum1 == DefectAssigneeColumnIndex):
                        sentence = sheet.cell(rownum, colnum1).value
                        sentence = sentence.replace('Unassigned','')
                        assignee.append(sentence)
                    if (colnum1 == DefectPriorityColumnIndex):
                        sentence = sheet.cell(rownum, colnum1).value
                        priority.append(sentence)
                    if (colnum1 == DefectReporterColumnIndex):
                        sentence = sheet.cell(rownum, colnum1).value
                        reporter.append(sentence)
                    if (colnum1 == DefectSeverityColumnIndex):
                        sentence = sheet.cell(rownum, colnum1).value
                        severity.append(sentence)
                else:
                    if (colnum1 == testRefColumnIndex):
                        sentence = sheet.cell(rownum, colnum1).value 
                        test_ref.append(sentence)
                    '''if (colnum1 == DefectSummaryIDColumnIndex):
                        sentence = sheet.cell(rownum, colnum1).value = 'NULL'
                        regex = re.compile(r'[\n\r\t]')
                        sentence = regex.sub(" ", sentence)
                        summary.append(sentence)
                    if (colnum1 == testCaseDescriptionColumnIndex):
                        sentence = sheet.cell(rownum, colnum1).value = 'NULL'
                        regex = re.compile(r'[\n\r\t]')
                        sentence = regex.sub(" ", sentence)
                        description.append(sentence)'''
            listscombined.append(g['depth_{0}'.format(i)])

          except KeyError:
             raise KeyError             
        # Loop to write all dynamically created Lists to text file

        joinedlist = []
        for i in listscombined:
            joinedlist.append(" ".join(i))
        
        return test_ref, summary, description, joinedlist, pname, environment, assignee, priority , reporter, severity
    except KeyError:
        raise KeyError
    except ValueError:
        raise ValueError
    except IndexError:
        raise IndexError
