import mysql.connector
import re
import os
import glob

def processETL(project):

    #path='/root/MODEL_DONT_OPEN/ALM/'
    path='C:/Users/147777/Documents/'
    projectpath=os.path.join(path, project)
    txtfol=os.path.join(projectpath+'/txtfile/')
    modelfol=os.path.join(projectpath+'/model/')
    excelfol=os.path.join(projectpath+'/excel/')
    processedfol=os.path.join(projectpath+'/processed/')
    savedfol=os.path.join(projectpath+'/savedfol/')
    
    cnx1 = mysql.connector.connect(user='vmware', password='Vmware@123',host='10.152.122.15',database='VTAP')
    cursor = cnx1.cursor()
    cursor.execute("SELECT * FROM VTAP.New_ALM where VTAP.New_ALM.project_name ='" + project + "'")
    data = list(cursor.fetchall())
    row_count = cursor.rowcount
    if row_count == 0 and os.listdir(modelfol):
        newdata2 = 'No Duplicates match'
        return newdata2
    elif row_count == 0 and not os.listdir(modelfol):
        newdata2 = 'Model progress'
        return newdata2
    else:
        data1=[]
        for i in data:
            data1.append(i)
        cnx1.close()

        newdata = [list(item) for item in data1]
        newdata2=[]
        for i in newdata:
            singlelist=[]
            for j in i:
                regex = re.compile(r'[\n\r\t\"]')
                a = regex.sub("", str(j))
                cleanr = re.compile('<.*?>')
                cleantext = re.sub(cleanr, '', a)
                cleantext1=re.sub("[\[].*?[\]]","",cleantext)
                singlelist.append(cleantext1)
            newdata2.append(singlelist)

       
        return newdata2

#print(processETL())

