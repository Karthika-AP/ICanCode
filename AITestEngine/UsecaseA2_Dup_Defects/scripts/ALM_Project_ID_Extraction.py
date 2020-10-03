import cx_Oracle

def processETL(sessionid2,totalprojectname_UPL,totalsubprojectname_UPL):
    print('Extracting from DataBase')
    dsn_tns = cx_Oracle.makedsn('10.166.27.26', 1521, 'STDYDB');
    conn = cx_Oracle.connect('sharath_io_ora', 'orapwd123', dsn_tns);
    cursor = conn.cursor()

    data1=[]
    for i in range(len(totalprojectname_UPL)):
        cursor.execute("select it_ops_it_ops_db0.all_lists.al_item_id from it_ops_it_ops_db0.all_lists where it_ops_it_ops_db0.all_lists.al_father_id =(select it_ops_it_ops_db0.all_lists.al_item_id from it_ops_it_ops_db0.all_lists where it_ops_it_ops_db0.all_lists.al_description='" + totalprojectname_UPL[i] + "') and it_ops_it_ops_db0.all_lists.al_description='" + totalsubprojectname_UPL[i] + "'")
        data = cursor.fetchall()     
        data1.append(data[0])
    
    data2=[item for t in data1 for item in t]
    conn.close()
    
    return data2

#print(processETL())

