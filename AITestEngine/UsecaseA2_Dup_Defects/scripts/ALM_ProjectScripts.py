from django.conf import settings
import yaml
import mysql.connector

basepath=settings.BASE_DIR

yamlpath = '/UsecaseA2_Dup_Defects/scripts/'
path = basepath + yamlpath
with open(path + 'UsecaseA2_Dup_Defects.yml', 'r') as ymlfile:
    cfg = yaml.load(ymlfile, yaml.Loader)

def processETL(sessionid2):
    cnx1 = mysql.connector.connect(user='vmware', password='Vmware@123',host='10.152.122.15',database='VTAP')
    cursor = cnx1.cursor()
    cursor.execute("SELECT VTAP.New_ALM_Project_List.ID, VTAP.New_ALM_Project_List.TS_USER_TEMPLATE_12 FROM VTAP.New_ALM_Project_List order by VTAP.New_ALM_Project_List.TS_USER_TEMPLATE_12")
    data = list(cursor.fetchall())
    cnx1.close()
    return data
