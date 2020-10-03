import cx_Oracle

def processETL(sessionid2,totalproject2_UPL):
    print('Extracting from DataBase')
    connstr = 'KPALANISAMY_DWH/S2y_at0PlY9A@prdap-dwdb.eng.vmware.com:1521/PRDAPD'
    conn = cx_Oracle.connect(connstr)
    cursor = conn.cursor()

    data1=[]
    for i in range(len(totalproject2_UPL)):
        cursor.execute("select PRD_JIRA_DWH.dwh_project.pkey from PRD_JIRA_DWH.dwh_project where prd_jira_dwh.dwh_project.pname='" + totalproject2_UPL[i] + "'")
        data = cursor.fetchall()     
        data1.append(data[0])
    
    data2=[item for t in data1 for item in t]
    conn.close()
    
    return data2

#print(processETL())

