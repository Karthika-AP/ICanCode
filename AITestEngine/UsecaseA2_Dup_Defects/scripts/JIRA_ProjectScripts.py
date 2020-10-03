
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
    cursor.execute("SELECT VTAP.New_JIRA_Project_List.ID, VTAP.New_JIRA_Project_List.PNAME FROM VTAP.New_JIRA_Project_List where VTAP.New_JIRA_Project_List.BUSNIESS_IT='Y' order by VTAP.New_JIRA_Project_List.PNAME")
    data = list(cursor.fetchall())
    cnx1.close()
    return data
