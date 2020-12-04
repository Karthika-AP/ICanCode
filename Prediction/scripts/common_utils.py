import mysql.connector
import yaml
import os
from django.conf import settings

basepath=str(settings.BASE_DIR)

yamlpath = '/Prediction/scripts/'
path = basepath  + yamlpath
with open(path + 'uc1.yml', 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

def getConnection():
    cnx = mysql.connector.connect(user=cfg['mysql']['user'], password=cfg['mysql']['password'],
                                  host=cfg['mysql']['host'], database=cfg['mysql']['database'])
    return cnx
