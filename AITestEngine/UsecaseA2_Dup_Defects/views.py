# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST
import requests
from xlrd import XLRDError
from requests.auth import HTTPBasicAuth
from django.utils.datastructures import MultiValueDictKeyError
from urllib.error import HTTPError
from django.db import IntegrityError
from requests import ConnectionError
from rest_framework.views import APIView
from .serializers import FileSerializer, FileSerializer1
from pathlib import Path
import os
import glob
import ntpath
import shutil, errno
import re
import yaml
import xml.etree.cElementTree as ET
import logging
logger = logging.getLogger(__name__)


from .scripts import ALM_ProjectScripts, ALM_ProjectDisplay_VTAP_SERVICE_3, ALM_testcasefiling_new, ALM_testcaseread_post_new, ALM_Clustering, ALM_Submit_TestCase, ALM_Project_ID_Extraction

from .scripts import JIRA_ProjectScripts, JIRA_ProjectDisplay_VTAP_SERVICE_4, JIRA_testcasefiling_new, JIRA_testcaseread_post_new, JIRA_Clustering, JIRA_Project_Key_Extraction

basepath=settings.BASE_DIR


yamlpath = '/UsecaseA2_Dup_Defects/scripts/'
path = basepath + yamlpath
with open(path + 'UsecaseA2_Dup_Defects.yml', 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

class FileView(APIView):
  parser_classes = (MultiPartParser, FormParser)
  def post(self, request, *args, **kwargs):
    try:
      a=request.data['filetype']
      s=request.data['file']
      print(s)
    

      if a=='Defects':
          file_serializer = FileSerializer(data=request.data)
          if file_serializer.is_valid():
                      
            request.session.cycle_key()
            sessionid1 = request.session.session_key
            sessionid2 = sessionid1[26:]

            path2=basepath+'/AITestEngine/media/Defects/'
            for filename in glob.glob(os.path.join(path2, '*.xlsx')):
              filename1 = str(ntpath.basename(filename))
              if str(s)==str(filename1):
                if os.path.isfile(filename):
                  os.unlink(filename)

            path = basepath + cfg['paths']['fol']
            sessionfol = os.path.join(path, sessionid2 + 'k')
            try:
                os.makedirs(sessionfol)
                textfol = os.path.join(path, sessionid2 + '/textprocessed')
                tcupload = os.path.join(path, sessionid2 + '/testcaseupload')
                os.makedirs(textfol)
                os.makedirs(tcupload)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    # directory already exists
                    pass
                else:
                    print(e)
            # Removing a directory
            try:
                shutil.rmtree(sessionfol)
            except OSError as e:
                print(e)
            print(sessionid2)            
            file_serializer.save()
            print(file_serializer.data)
            response = JsonResponse(file_serializer.data, status=status.HTTP_201_CREATED)
            
            b=request.data['project_id']
            response=resultdefect(request,b,sessionid2,s)
            
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Credentials"] = "true"
            response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
            response["Access-Control-Max-Age"] = "3600"
            response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
            return response
          else:
            response = JsonResponse(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Credentials"] = "true"
            response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
            response["Access-Control-Max-Age"] = "3600"
            response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
            return response
          
      if a=='TestCase':
          file_serializer = FileSerializer1(data=request.data)
          if file_serializer.is_valid():

            request.session.cycle_key()
            sessionid1 = request.session.session_key
            sessionid2 = sessionid1[26:]

            path2=basepath+'/AITestEngine/media/TestCase/'
            for filename in glob.glob(os.path.join(path2, '*.xlsx')):
              filename1 = str(ntpath.basename(filename))
              if str(s)==str(filename1):
                if os.path.isfile(filename):
                  print('deleting')
                  os.unlink(filename)
            
            path= basepath+cfg['paths']['fol']
            sessionfol= os.path.join(path, sessionid2+'k')
            try:
                os.makedirs(sessionfol)
                textfol=os.path.join(path, sessionid2+'/textprocessed')
                tcupload = os.path.join(path, sessionid2 + '/testcaseupload')
                os.makedirs(textfol)
                os.makedirs(tcupload)
            except OSError as e:
                if e.errno != errno.EEXIST:
                #directory already exists
                    pass
                else:
                    print(e)
            #Removing a directory
            try:
                shutil.rmtree(sessionfol)
            except OSError as e:
                print(e)
            
            file_serializer.save()
            response = JsonResponse(file_serializer.data, status=status.HTTP_201_CREATED)

            b=request.data['project_id']
            response=resulttestcase(request,b,sessionid2,s)
            
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Credentials"] = "true"
            response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
            response["Access-Control-Max-Age"] = "3600"
            response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
            return response
          else:
            response = JsonResponse(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Credentials"] = "true"
            response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
            response["Access-Control-Max-Age"] = "3600"
            response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
            return response
        
    except MultiValueDictKeyError:
        context = {
            "message": "Please upload the file and click Save"
        }
        response = JsonResponse(context, status=status.HTTP_412_PRECONDITION_FAILED , safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response



@ensure_csrf_cookie
@csrf_exempt
@require_GET
def indexdefect(request):
  try:
    request.session.cycle_key()
    sessionid1 = request.session.session_key
    sessionid2 = sessionid1[26:]
    
    folder_path = basepath + cfg['paths']['fol']
    if os.path.getsize(folder_path) > 5000 * 1:
        for file_object in os.listdir(folder_path):
            file_object_path = os.path.join(folder_path, file_object)
            if os.path.isfile(file_object_path):
                if 'zip.zip' in file_object:
                    pass
                else:
                    print('Deleting file' + file_object)
                    os.unlink(file_object_path)
            else:
                print('Deleting' + file_object)
                shutil.rmtree(file_object_path)

    data = JIRA_ProjectScripts.processETL(sessionid2)

    dictdata1=[list(elem) for elem in data]

    ProjectData=[]
    for i,j in dictdata1:
      ProjectData.append(dict(project_id=i, project_name=j))            

    response = JsonResponse(ProjectData, safe=False)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
    response["Access-Control-Max-Age"] = "3600"
    response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
    return response
  except HTTPError:
        context = {
            "message": "Internal Server Error 500. Please check with Tools Team"
        }
        response = JsonResponse(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
  except IntegrityError:
        context = {
            "message": "400 BAD REQUEST. Please check with Tools Team"
        }
        response = JsonResponse(context, status=status.HTTP_400_BAD_REQUEST, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
  except ConnectionError:
        context = {
            "message": "Global Protect Connection Error"
        }
        response = JsonResponse(context, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response

@ensure_csrf_cookie
@csrf_exempt
@require_GET
def indextestcase(request):
  try:
    request.session.cycle_key()
    sessionid1 = request.session.session_key
    sessionid2 = sessionid1[26:]

    folder_path = basepath+cfg['paths']['fol']
    if os.path.getsize(folder_path) > 5000*1: 
        for file_object in os.listdir(folder_path):
            file_object_path = os.path.join(folder_path, file_object)
            if os.path.isfile(file_object_path):
                if 'zip.zip' in file_object:
                    pass
                else:
                    print ('Deleting file' + file_object)
                    os.unlink(file_object_path)
            else:
                print ('Deleting' + file_object)
                shutil.rmtree(file_object_path)
                
    data = ALM_ProjectScripts.processETL(sessionid2)


    dictdata1=[list(elem) for elem in data]
    
    ProjectData=[]
    for i,j in dictdata1:            
        ProjectData.append(dict(project_id=i, project_name=j))

    response = JsonResponse(ProjectData, safe=False)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
    response["Access-Control-Max-Age"] = "3600"
    response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
    return response

  except HTTPError:
        context = {
            "message": "Internal Server Error 500. Please check with Tools Team"
        }
        response = JsonResponse(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
  except IntegrityError:
        context = {
            "message": "400 BAD REQUEST. Please check with Tools Team"
        }
        response = JsonResponse(context, status=status.HTTP_400_BAD_REQUEST, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
  except ConnectionError:
        context = {
            "message": "Global Protect Connection Error"
        }
        response = JsonResponse(context, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response


@ensure_csrf_cookie
@csrf_exempt
@require_POST
def projectdefect(request):
  try:
    global projectname
    projectname=''
    
    request.session.cycle_key()
    sessionid1 = request.session.session_key
    sessionid2 = sessionid1[26:]

    if request.method=='POST':
        json_data=json.loads(request.body)
        for data in json_data:
            if(data=='project_id'):
                projectid = json_data[data]

    data = JIRA_ProjectScripts.processETL(sessionid2)

    for i in data:
      if (int(projectid)==int(i[0])):
        projectname=i[1]
        break

    project = projectname   

    selected_project=JIRA_ProjectDisplay_VTAP_SERVICE_4.processETL(project)
    print(selected_project)

    if selected_project== 'No Duplicates match':
        context = {
            "message": "No Duplicate Match Found Above 75%"
        }
        response = JsonResponse(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
    elif selected_project== 'Model progress':
        context = {
            "message": "Model is in Progress. Please try after sometime"
        }
        response = JsonResponse(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
    else:
      print("hey")

      ProjectResult=[]
      for i,j,k,l,m,n,o,p,q,r,s,t,u,v,w in selected_project:
        ProjectResult.append(dict(si_no=i, pro_defect_id=j, pro_link=k, pro_summary=l, project_name=m, pro_issuetype=n, pro_description=o, pro_issue_num=p, project_key=q, pro_status=r, pro_priority=s, matching_percentage=t, matching_pro_id=u, matching_link=v, matching_issue_num=w))
                     
      response = JsonResponse(ProjectResult, safe=False)
      response["Access-Control-Allow-Origin"] = "*"
      response["Access-Control-Allow-Credentials"] = "true"
      response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
      response["Access-Control-Max-Age"] = "3600"
      response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
      return response
  
  except HTTPError:
        context = {
            "message": "Internal Server Error 500. Please check with Tools Team"
        }
        response = JsonResponse(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
  except IntegrityError:
        context = {
            "message": "400 BAD REQUEST. Please check with Tools Team"
        }
        response = JsonResponse(context, status=status.HTTP_400_BAD_REQUEST, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
  except ConnectionError:
        context = {
            "message": "Global Protect Connection Error"
        }
        response = JsonResponse(context, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
  
@ensure_csrf_cookie
@csrf_exempt
@require_POST
def projecttestcase(request):
  try:
    global projectname
    projectname=''
    
    request.session.cycle_key()
    sessionid1 = request.session.session_key
    sessionid2 = sessionid1[26:]
    
    if request.method=='POST':
        json_data=json.loads(request.body)
        for data in json_data:
            if(data=='project_id'):
                projectid = json_data[data]

    data = ALM_ProjectScripts.processETL(sessionid2)
    
    for i in data:
      if (int(projectid)==int(i[0])):
        projectname=i[1]
        break

    project = projectname
    selected_project=ALM_ProjectDisplay_VTAP_SERVICE_3.processETL(project)

    print(selected_project)

    if selected_project== 'No Duplicates match':
        context = {
            "message": "No Duplicate Match Found Above 75%"
        }
        response = JsonResponse(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
    elif selected_project== 'Model progress':
        context = {
            "message": "Model is in Progress. Please try after sometime"
        }
        response = JsonResponse(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response

    else:

      ProjectResult=[]
      for i,j,k,l,m,n,o,p,q,r,s in selected_project:
          ProjectResult.append(dict(si_no=i, pro_test_id=j, pro_test_name=k, pro_test_description=l, project_name=m, pro_step_description=n, pro_sprint_name=o, pro_status=p, pro_priority=q, matching_percentage=r, matching_test_id=s))
          

      response = JsonResponse(ProjectResult, safe=False)
      response["Access-Control-Allow-Origin"] = "*"
      response["Access-Control-Allow-Credentials"] = "true"
      response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
      response["Access-Control-Max-Age"] = "3600"
      response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
      return response
  except HTTPError:
        context = {
            "message": "Internal Server Error 500. Please check with Tools Team"
        }
        response = JsonResponse(context,status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
  except IntegrityError:
        context = {
            "message": "400 BAD REQUEST. Please check with Tools Team"
        }
        response = JsonResponse(context, status=status.HTTP_400_BAD_REQUEST, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
  except ConnectionError:
        context = {
            "message": "Global Protect Connection Error"
        }
        response = JsonResponse(context, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response  


@ensure_csrf_cookie
@csrf_exempt
@require_POST
def resultdefect(request, b, sessionid2, s):
    global projectname
    projectname=''
   
    path = basepath + cfg['paths']['fol']
    pathtest = path + sessionid2 + '/testcaseupload/'
    try:
      filepaths = []   
      for filename in glob.glob(os.path.join(basepath+'/AITestEngine/media/Defects/'+str(s))):
          files = shutil.copy(filename, pathtest)        
      
      filepaths.append(files)

      projectid = b
      
      print("hey Defect Project ID")
      print(projectid)

      data = JIRA_ProjectScripts.processETL(sessionid2)
      for i in data:
        if (int(projectid)==int(i[0])):
          projectname=i[1]
          break

      project = projectname

      print("Hey Defect Project Name")
      print(project)

      #project = 'Skyline Phase 2'

      totaltestref_UPL = []
      totaltestcase2_UPL = []
      totaltestdecrip2_UPL = []
      totalproject2_UPL = []
      totalenviron2_UPL = []
      totalassignee2_UPL = []
      totalpriority2_UPL = []
      totalreporter2_UPL = []
      totalseverity2_UPL = []
      
      for filename in glob.glob(os.path.join(pathtest, '*.xlsx')):
          filename = str(ntpath.basename(filename))
          print(filename)
          test_ref2, testname2, objective2, joinedlist2, pname2, environment2, assignee2, priority2, reporter2, severity2 = JIRA_testcaseread_post_new.readTestCasesFromExcelFile(filename, sessionid2)
          if test_ref2.__len__() == 0:
                  print('#####   Null Object    #####')
                  raise IndexError
          for i in test_ref2:
              totaltestref_UPL.append(i)
          for j in testname2:
              totaltestcase2_UPL.append(j)
          for k in objective2:
              totaltestdecrip2_UPL.append(k)
          for m in pname2:
              totalproject2_UPL.append(m)
          for n in environment2:
              totalenviron2_UPL.append(n)
          for o in assignee2:
              totalassignee2_UPL.append(o)
          for p in priority2:
              totalpriority2_UPL.append(p)
          for q in reporter2:
              totalreporter2_UPL.append(q)
          for r in severity2:
              totalseverity2_UPL.append(r)

          print("hey severity")
          print(totalseverity2_UPL)
          print(len(totalseverity2_UPL))


      #path='/root/MODEL_DONT_OPEN/JIRA/'
      path='C:/Users/147777/Documents/'
      
      projectpath=os.path.join(path, project)
      txtfol=os.path.join(projectpath+'/txtfile/')
      modelfol=os.path.join(projectpath+'/model/')
      excelfol=os.path.join(projectpath+'/excel/')
      processedfol=os.path.join(projectpath+'/processed/')
      savedfol=os.path.join(projectpath+'/savedfol/')


      totaltestref_DB, totalprojectkey_DB, totalissuenum_DB, joinedlist1, pathlocationnew = JIRA_Clustering.cluster(project,joinedlist2)

      #Removing duplicate id and get text and id out of all txt files    
      listsnew=[]
      filename4=[]
      for j in range(len(pathlocationnew)):
          lists=[]
          filename3=[]
          filename5=''
          i=0
          for clus in pathlocationnew[j]:             
              for filename1 in glob.glob(clus):
                  texts=''
                  with open(filename1, 'r') as f:
                      text = f.readlines()
                      for l in text:                                                       
                          filename2=Path(filename1).name
                          filename5=filename2.replace('.txt','')
                          if filename5 != str(totaltestref_UPL[j]):
                              filename3.append(filename5)                              
                              texts = texts + ' ' + l
                              lists.append(texts)
                                
                  i=i+1
          filename4.append(filename3)
          listsnew.append(lists)
        
        
      for i in range(len(filename4)):
        filename4[i].extend(totaltestref_UPL)
        filename4[i].remove(totaltestref_UPL[i])
      for i in range(len(listsnew)):
        listsnew[i].extend(joinedlist2)
        listsnew[i].remove(joinedlist2[i])

      for i in totaltestref_UPL:
          totaltestref_DB.append(i)

      finalresult = JIRA_testcasefiling_new.optimize(sessionid2, joinedlist2, totaltestref_DB, totaltestref_UPL, filename4, listsnew)
 
      maxindexlist = []
      maxvaluelist = []

      for i in finalresult:
          maxindexlist.append(i.index(max(i)))
          maxvaluelist.append(max(i))


      jira_project_key_upload = JIRA_Project_Key_Extraction.processETL(sessionid2,totalproject2_UPL)
      print(jira_project_key_upload)

      boolvalue=False
      totalfinallists = []
      repeatTC = []
      for i in range(len(totaltestref_UPL)):

        if ((totaltestref_UPL[i]!= totaltestref_DB[maxindexlist[i]])and(maxvaluelist[i]>=0)):
          ka = []
          ka.append(int(totaltestref_UPL[i]))
          ka.append(totaltestcase2_UPL[i])
          ka.append(totaltestdecrip2_UPL[i])
          ka.append(str(jira_project_key_upload[i]))
          ka.append(int(totaltestref_DB[maxindexlist[i]]))
          ka.append(int(maxvaluelist[i]))
          ka.append(totalenviron2_UPL[i])
          ka.append(totalassignee2_UPL[i])
          ka.append(totalpriority2_UPL[i])
          ka.append(totalreporter2_UPL[i])
          ka.append(totalseverity2_UPL[i])
          
          if ((totaltestref_DB[maxindexlist[i]]) not in totaltestref_UPL):
              ka.append('https://jira.eng.vmware.com/browse/'+str(totalprojectkey_DB[maxindexlist[i]])+'-'+str(int(totalissuenum_DB[maxindexlist[i]])))
          else:
              ka.append('Refer Uploaded File')              
          if (totaltestref_DB[maxindexlist[i]] not in totaltestref_UPL):
              ka.append(totalprojectkey_DB[maxindexlist[i]])         
          else:
              ka.append('no key')              
          ka.append(boolvalue)
          if((set((totaltestref_UPL[i],totaltestref_DB[maxindexlist[i]])) not in repeatTC)):
              repeatTC.append(set((totaltestref_UPL[i],totaltestref_DB[maxindexlist[i]])))
              totalfinallists.append(ka)

      newdata = [list(item) for item in totalfinallists]
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


      FinalResult=[]
      for i,j,k,q,l,m,r,s,t,u,v,n,o,p in newdata2:
        FinalResult.append(dict(upload_defect_id=i, upload_summary=j, upload_description=k, upload_project_key=q, match_defect_id=l, match_percentage=m, environment=r, assignee=s, priority=t, reporter=u, severity=v, match_link=n, match_project_key=o, check=p))    

      response = JsonResponse(FinalResult, safe=False)
      response["Access-Control-Allow-Origin"] = "*"
      response["Access-Control-Allow-Credentials"] = "true"
      response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
      response["Access-Control-Max-Age"] = "3600"
      response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
      return response
    
    except KeyError:
        context = {
            "message": "Please upload excel file in acceptable format"
        }
        response = JsonResponse(context, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response    
    except IndexError:
      
        context = {
            "message": "Please upload excel file in acceptable format with proper column names / column values"
        }
        return JsonResponse(context, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response    
    except TypeError:
        context = {
            "message": "Please upload excel file in acceptable format with proper column names"
        }
        response = JsonResponse(context, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
    
    except AttributeError:
        context = {
            "message": "Please upload excel file in acceptable format with proper column names"
        }
        response = JsonResponse(context, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
    except ValueError:
        context = {
            "message": "Please make sure all Mandatory column names/values and Test Case Numbering are Entered"
        }
        response = JsonResponse(context, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
    
    except XLRDError:
        context = {
            "message": "Please make sure to upload intended excel files in acceptable format with correct sheet name"
        }
        response = JsonResponse(context, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
    except UnboundLocalError:
        context = {
            "message": "Please make sure to upload excel file with .xlsx file extension with specified format"
        }
        response = JsonResponse(context, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response    
    except RuntimeError:
        context = {
            "message": "Please upload correct format of the file"
        }
        response = JsonResponse(context, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
    except FileNotFoundError:
        context = {
            "message": "Model is in Progress. Please try after some time"
        }
        response = JsonResponse(context, status = status.HTTP_404_NOT_FOUND, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
    except HTTPError:
        context = {
            "message": "Internal Server Error 500. Please check with Tools Team"
        }
        response = JsonResponse(context,status = status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
    except IntegrityError:
        context = {
            "message": "400 BAD REQUEST. Please check with Tools Team"
        }
        response = JsonResponse(context, status = status.HTTP_400_BAD_REQUEST, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
    except ConnectionError:
        context = {
            "message": "Global Protect Connection Error"
        }
        response = JsonResponse(context, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response 

global sessionid2
@ensure_csrf_cookie
@csrf_exempt
@require_POST
def resulttestcase(request, b, sessionid2, s):
    global projectname
    projectname=''   
    try:
      path= basepath+cfg['paths']['fol']  
      pathtest=path+ sessionid2 + '/testcaseupload/'
      filepaths = [] 
      for filename in glob.glob(os.path.join(basepath+'/AITestEngine/media/TestCase/'+str(s))):
          files = shutil.copy(filename, pathtest)

      filepaths.append(files)

      projectid = b
      print("hey Test Case Project ID")
      print(projectid)
    
      data = ALM_ProjectScripts.processETL(sessionid2)
      for i in data:
        if (int(projectid)==int(i[0])):
          projectname=i[1]
          break

      project = projectname
      print("Hey Test Case Project Name")
      print(project)

      #project = 'Skyline Phase 2 (SP2)'

      totaltestref_UPL=[]
      totaltestcase_UPL=[]
      totaltestdescrip_UPL=[]
      totalprojectname_UPL=[]
      totalsubprojectname_UPL=[]
      
      for filename in glob.glob(os.path.join(pathtest, '*.xlsx')):
          filename=str(ntpath.basename(filename))
          test_ref2,testname2,description2,project_name2,sub_project_name2,joinedlist2=ALM_testcaseread_post_new.readTestCasesFromExcelFile(filename,sessionid2)
          if test_ref2.__len__() == 0:
                  print('#####   Null Object    #####')
                  raise IndexError
          for i in test_ref2:
              totaltestref_UPL.append(i)
          for j in testname2:
              totaltestcase_UPL.append(j)
          for k in description2:
              totaltestdescrip_UPL.append(k)
          for m in project_name2:
              totalprojectname_UPL.append(m)
          for n in sub_project_name2:
              totalsubprojectname_UPL.append(n)

      #pathnew='/root/MODEL_DONT_OPEN/ALM/'
      pathnew='C:/Users/147777/Documents/'
      
      projectpath=os.path.join(pathnew, project)
      txtfol=os.path.join(projectpath+'/txtfile/')
      modelfol=os.path.join(projectpath+'/model/')
      excelfol=os.path.join(projectpath+'/excel/')
      processedfol=os.path.join(projectpath+'/processed/')
      savedfol=os.path.join(projectpath+'/savedfol/')

      totaltestref_DB, sprint_name, totalproname_DB, joinedlist1, pathlocationnew = ALM_Clustering.cluster(project,joinedlist2)

      #Removing duplicate id and get text and id out of all txt files    
      listsnew=[]
      filename4=[]
      for j in range(len(pathlocationnew)):
          lists=[]
          filename3=[]
          filename5=''
          i=0
          for clus in pathlocationnew[j]:             
              for filename1 in glob.glob(clus):
                  texts=''
                  with open(filename1, 'r') as f:
                      text = f.readlines()
                      for l in text:                                                       
                          filename2=Path(filename1).name
                          filename5=filename2.replace('.txt','')
                          if filename5 != str(totaltestref_UPL[j]):
                              filename3.append(filename5)                              
                              texts = texts + ' ' + l
                              lists.append(texts)
                              
                  i=i+1
          filename4.append(filename3)
          listsnew.append(lists)

      for i in range(len(filename4)):
        filename4[i].extend(totaltestref_UPL)
        filename4[i].remove(totaltestref_UPL[i])
      for i in range(len(listsnew)):
        listsnew[i].extend(joinedlist2)
        listsnew[i].remove(joinedlist2[i])

      for i in totaltestref_UPL:
          totaltestref_DB.append(i)

      finalresult=ALM_testcasefiling_new.optimize(sessionid2, joinedlist2, totaltestref_DB, totaltestref_UPL, filename4, listsnew) 

      maxindexlist = []
      maxvaluelist = []

      for i in finalresult:
          maxindexlist.append(i.index(max(i)))
          maxvaluelist.append(max(i))

      alm_projectid_submit = ALM_Project_ID_Extraction.processETL(sessionid2,totalprojectname_UPL,totalsubprojectname_UPL)

      boolvalue=False
      totalfinallists=[]
      repeatTC=[]
      testid=[]      

      for i in range(len(totaltestref_UPL)):
            if ((totaltestref_UPL[i]!=totaltestref_DB[maxindexlist[i]])and(maxvaluelist[i]>=0)):
              ka=[]
              ka.append(int(totaltestref_UPL[i]))            
              ka.append(totaltestcase_UPL[i])
              ka.append(totaltestdescrip_UPL[i])
              ka.append(int(totaltestref_DB[maxindexlist[i]]))
              ka.append(int(maxvaluelist[i]))
              ka.append(totalproname_DB[1])
              ka.append(int(alm_projectid_submit[i]))
              #sample=1265
              #ka.append(int(sample))
              ka.append(boolvalue)
              if((set((totaltestref_UPL[i],totaltestref_DB[maxindexlist[i]])) not in repeatTC)):
                  repeatTC.append(set((totaltestref_UPL[i],totaltestref_DB[maxindexlist[i]])))
                  testid.append(int(totaltestref_UPL[i]))
                  totalfinallists.append(ka)
                  
      path= basepath+cfg['paths']['fol']
      pathtest = path + sessionid2 + '/testcaseupload/'

      filenamelist=[]
      b=[]

      for filename in glob.glob(os.path.join(pathtest, '*.xlsx')):
            filename=str(ntpath.basename(filename))
            filenamelist.append(filename)
            TotalValues=[]
            for searchid in testid:
              Values=ALM_Submit_TestCase.ColumnSearch(searchid,filenamelist,sessionid2)
              TotalValues.append(Values)
          
      newdata = [list(item) for item in totalfinallists]
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

      FinalResult=[]
      for i,j,k,l,m,n,o,p in newdata2:
          FinalResult.append(dict(upload_test_id=i, upload_testname=j, upload_testdescription=k, match_test_id=l, match_percentage=m, db_project_name=n, db_project_id=o, check=p))

      FileFinalResult=[]
      for c,d,e,f,g,h,i,j,k,m in TotalValues:
          FileFinalResult.append(dict(qc_internal=c, test_case_developer=d, status=e, test_case_priority=f, product=g, functional_area=h, component=i, testcasetype=j, Fully_automatable=k, Automation_level=m))


      def Merge(a,b):
        return b.update(a)
      finallist=[]
      
      for i in range(len(FinalResult)):
            team={}
            finaldict={}
            team=FinalResult[i].update(FileFinalResult[i])
            finaldict=FinalResult[i]
            finallist.append(finaldict)

      
      response = JsonResponse(finallist, safe=False)
      response["Access-Control-Allow-Origin"] = "*"
      response["Access-Control-Allow-Credentials"] = "true"
      response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
      response["Access-Control-Max-Age"] = "3600"
      response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
      return response
    
    except KeyError:
        context = {
            "message": "Please upload excel file in acceptable format"
        }
        response = JsonResponse(context, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response    
    except IndexError:
        context = {
            "message": "Please upload excel file in acceptable format with proper column names / column values"
        }
        return JsonResponse(context, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response    
    except TypeError:
        context = {
            "message": "Please upload excel file in acceptable format with proper column names"
        }
        response = JsonResponse(context, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
    
    except AttributeError:
        context = {
            "message": "Please upload excel file in acceptable format with proper column names"
        }
        response = JsonResponse(context, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
    except ValueError:
        context = {
            "message": "Please make sure all Mandatory column names/values and Test Case Numbering are Entered"
        }
        response = JsonResponse(context, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
    
    except XLRDError:
        context = {
            "message": "Please make sure to upload intended excel files in acceptable format with correct sheet name"
        }
        response = JsonResponse(context, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
    except UnboundLocalError:
        context = {
            "message": "Please make sure to upload excel file with .xlsx file extension with specified format"
        }
        response = JsonResponse(context, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response    
    except RuntimeError:
        context = {
            "message": "Please upload correct format of the file"
        }
        response = JsonResponse(context, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
    except FileNotFoundError:
        context = {
            "message": "Model is in Progress. Please try after sometime"
        }
        response = JsonResponse(context, status = status.HTTP_404_NOT_FOUND, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
    except HTTPError:
        context = {
            "message": "Internal Server Error 500. Please check with Tools Team"
        }
        response = JsonResponse(context, status = status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
    except IntegrityError:
        context = {
            "message": "400 BAD REQUEST. Please check with Tools Team"
        }
        response = JsonResponse(context, status = status.HTTP_400_BAD_REQUEST, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
    except ConnectionError:
        context = {
            "message": "Global Protect Connection Error"
        }
        response = JsonResponse(context, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response 
    


@ensure_csrf_cookie
@csrf_exempt
@require_POST
def submitdefect(request):
  try:
    b=[]
    Id=[]
    self=[]
    IssueKey=[]
    nodupli=[]
    dupli=[]
    if request.method=='POST':
          json_data=json.loads(request.body)
          '''a1= json_data
          for i in range(len(a1)):
            if a1[i]["upload_defect_id"] not in dupli:
              dupli.append(a1[i]["upload_defect_id"])
              nodupli.append(a1[i])
          a=nodupli'''
          a=json_data
            
          for i in range(len(a)):
              if a[i]["check"]== True:                
                  print("heyyyyyyyyyyyyyyyyyy")
                  data={
                    "fields":{
                        "project":
                        {
                            "key":a[i]["upload_project_key"]
                            },
                        "summary":a[i]["upload_summary"],
                        "description":a[i]["upload_description"],
                        "environment":a[i]["environment"],
                        "issuetype":{
                            "name":"Bug"
                            },
                        "assignee":{
                             "name":a[i]["assignee"]
                             },
                        "priority":{
                             "name":a[i]["priority"]
                             },
                        "reporter":{
                             "name":a[i]["reporter"]
                             },
                        "customfield_10231":{
                             "value":a[i]["severity"]
                             }
                        }
                      
                    }
                  url = 'https://jira.eng.vmware.com/rest/api/2/issue'
                  response = requests.post(url, json=data, auth=HTTPBasicAuth('svc.vtapuser', '@J@ag1h.iB^99@YTXr5'))
                  print(response)
                  print("response text")
                  print(response.text)
                  #response = requests.post(url, json=data, auth=HTTPBasicAuth('kpalanisamy', 'Nttdata@12345'))
                  data= json.loads(response.text)
                  finalData =[]
                  Id.append(data['id'])
                  IssueKey.append(data['key'])
                  self.append(data['self'])
                  url='https://jira.eng.vmware.com/browse/'+str(IssueKey)
                  b.append(a[i])
    context={
              #"Id": Id,
              "IssueKey": IssueKey,
              #"self": self,
              "message": "The Selected Defects are Submitted"
              }
                
     

    response = JsonResponse(context, safe=False)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
    response["Access-Control-Max-Age"] = "3600"
    response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
    return response

  except KeyError:
        context = {
            "message": "No Access to Submit the Defects to Project Name in Uploaded File"
        }
        response = JsonResponse(context, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
  except OSError:
        context = {
            "message": "OS Error - Please try again"
        }
        response = JsonResponse(context, status = status.HTTP_503_SERVICE_UNAVAILABLE, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
  except HTTPError:
        context = {
            "message": "Internal Server Error 500. Please check with Tools Team"
        }
        response = JsonResponse(context, status = status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
  except IntegrityError:
        context = {
            "message": "400 BAD REQUEST. Please check with Tools Team"
        }
        response = JsonResponse(context, status = status.HTTP_400_BAD_REQUEST, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
  except ConnectionError:
        context = {
            "message": "Global Protect Connection Error"
        }
        response = JsonResponse(context, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response 

@ensure_csrf_cookie
@csrf_exempt
@require_POST
def submittestcase(request):
  try:
    nodupli=[]
    dupli=[]
    if request.method=='POST':
          json_data=json.loads(request.body)
          '''a1= json_data
          for i in range(len(a1)):
            if a1[i]["upload_test_id"] not in dupli:
              dupli.append(a1[i]["upload_test_id"])
              nodupli.append(a1[i])
          a=nodupli'''
    a=json_data

    b=[]
    Values=[]
    errormessage=[]
    for i in range(len(a)):
      if a[i]["check"]== True:
        testid=[]
        if a[i]["upload_testname"]:
          testid.append(a[i]["upload_testname"])
        if a[i]["upload_testdescription"]:
          testid.append(a[i]["upload_testdescription"])
        if a[i]["qc_internal"]:
          testid.append(a[i]["qc_internal"])
        if a[i]["test_case_developer"]:
          testid.append(a[i]["test_case_developer"])
        if a[i]["status"]:
          testid.append(a[i]["status"])
        if a[i]["test_case_priority"]:
          testid.append(a[i]["test_case_priority"])
        if a[i]["product"]:
          testid.append(a[i]["product"])
        if a[i]["functional_area"]:
          testid.append(a[i]["functional_area"])
        if a[i]["component"]:
          testid.append(a[i]["component"])
        if a[i]["testcasetype"]:
          testid.append(a[i]["testcasetype"])
        if a[i]["Fully_automatable"]:
          testid.append(a[i]["Fully_automatable"])
        if a[i]["db_project_id"]:
          testid.append(a[i]["db_project_id"])
        if a[i]["Automation_level"]:
          testid.append(a[i]["Automation_level"])
        Values = testid
         
        Field_Names = ['name', 'description', 'subtype-id', 'owner', 'status', 'user-template-09', 'user-template-12', 'user-template-01', 'user-template-02', 'user-template-08', 'user-template-04', 'parent-id', 'user-template-03']
        results = ET.Element("Entity", Type='test')
        result = ET.SubElement(results,"Fields")
        for k in range(len(Field_Names)):
          FN="Field Name='"+str(Field_Names[k]) +"'"
          person = ET.SubElement(result,"Field",Name=str(Field_Names[k]))
          student = ET.SubElement(person,"Value")
          student.text = str(Values[k])
          results.append(result)
               
        tree = ET.ElementTree(results)
        tree.write('test.xml')
        file = open('test.xml','r')
        data = file.readlines()

        headers = {'Content-Type': 'application/xml','APIKey':'c2NoaWtrYWphbGFzaDpTYWlzYW1hcnRoYS0x'} # set what your server accepts
        host ='https://quality-api.eng.vmware.com/QCIntgr2/rest/rest.php/domains/IT_OPS/projects/IT_OPS/tests'
        amlStr = """ """
        xmlStr = ET.tostring(results).decode()
        response = requests.post(host, data=xmlStr, headers=headers, verify=False)        
              
        root = ET.fromstring(response.content)
        id=[]
        for field in root.iter('Field'):
          for value in field.iter('Value'):
            if(field.get('Name') == 'id'):
              m=value.text
              b.append(m)
        
        root1 = ET.fromstring(response.content)
        for field1 in root1.iter('WSRestException'):
          for value1 in field1.iter('Description'):
            excep=value1.text
            errormessage.append(excep)

    if not b:
      b.append("Duplicates Found : The Selected TestCases are already present in ALM. Please try again with different Test Name")

    if not errormessage:
      errormessage.append("No Duplicates : The Selected TestCase are submitted to ALM")

    context={
            "IssueKey": b,
            "Duplicates": errormessage,
            }

    response = JsonResponse(context, safe=False)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
    response["Access-Control-Max-Age"] = "3600"
    response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
    return response
  except OSError:
        context = {
            "message": "OSError - Please try again"
        }
        response = JsonResponse(context, status = status.HTTP_503_SERVICE_UNAVAILABLE, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
  except HTTPError:
        context = {
            "message": "Internal Server Error 500. Please check with Tools Team"
        }
        response = JsonResponse(context, status = status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
  except IntegrityError:
        context = {
            "message": "400 BAD REQUEST. Please check with Tools Team"
        }
        response = JsonResponse(context, status = status.HTTP_400_BAD_REQUEST, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response
  except ConnectionError:
        context = {
            "message": "Global Protect Connection Error"
        }
        response = JsonResponse(context, safe=False)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
        response["Access-Control-Max-Age"] = "3600"
        response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
        return response 
    
