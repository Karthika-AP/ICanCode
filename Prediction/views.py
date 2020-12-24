# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.template import RequestContext
from django.urls import reverse
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.clickjacking import xframe_options_deny
import os
import yaml
import glob
from django.conf import settings
from .models import Document
from .forms import DocumentForm
from .forms import FileFieldForm
from .scripts import Linear_Regression, Tensor_Flow
from .scripts import db_datamanagement_fetch_db_data
from .scripts import db_datamanagement_insert_db_data

basepath=str(settings.BASE_DIR)
yamlpath = '/Prediction/scripts/'
path = basepath +  yamlpath
with open(path + 'uc1.yml', 'r') as ymlfile:
    cfg = yaml.load(ymlfile)


# Authenticate for the type of user
def in_group_a(username):
    return username.groups.filter(name__in=['admin', 'tester', 'manager']).exists()


# First page to be called
@xframe_options_deny
@login_required(login_url=cfg['urls']['login'])
@user_passes_test(in_group_a, login_url=cfg['urls']['denied'])
def metrics(request):
    with open(path + 'uc1.yml', 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    optionList = [cfg['DE']['module']]

    return render(request, cfg['urls']['metrics'], {'optionList': optionList})

# Module selection
def getparameters(Module_in):
    if (Module_in == cfg['DE']['module']):
        tn = cfg['DE']['tn']
        tncols = cfg['DE']['tncols']
        predict_cols = cfg['DE']['predict_cols']
        tn_lp = cfg['DE']['tn_lp']   
    return tn, tncols, predict_cols, tn_lp


@xframe_options_deny
@login_required(login_url=cfg['urls']['login'])
@user_passes_test(in_group_a, login_url=cfg['urls']['denied'])
def details(request):
    "Function to process basic details page"
    global graph_data, predicted_data, Relid, ucl, lcl, project_in, Module_in, Relid
    
    project_in = request.POST.get('project', False)
    Algorithm_in = request.POST.get('Algorithm', False)
    Module_in = request.POST.get('Module', False)
    
    if (Module_in == 'null'):
        return HttpResponseRedirect(cfg['urls']['metrics'])
    else:
        tn, tncols, predict_cols, tn_lp = getparameters(Module_in)  # Calls the function to get tablename, columns, prediction columns and last prediction table

    Relid, graph_data, ucl, lcl = Linear_Regression.graph_data(tn, tncols, predict_cols)

    context = {        
        "Algorithm_in": Algorithm_in,
        "Prediction_in": Module_in,
        "project_in": project_in,
        "ucl": ucl[0],
        "lcl": lcl[0],
    }
    return render(request, cfg['urls']['details'], context)


@xframe_options_deny
@login_required(login_url=cfg['urls']['login'])
@user_passes_test(in_group_a, login_url=cfg['urls']['denied'])
def use(request):
    "This function predicts and produces results"
    global graph_data, predicted_data, Relid, ucl, lcl
    module = ''
    
    Algorithm_in = request.POST.get('Algorithm', False)
    ucl_in = request.POST.get('UCL', False)
    lcl_in = request.POST.get('LCL', False)    
    tn, tncols, predict_cols, tn_lp = getparameters(Module_in)  # Calls the function to get tablename, columns, prediction columns and last prediction table
    Algorithm_Name = ''
    
    # Checks for which algorithm to be used
    if (Algorithm_in == '1'):
        predicted_data = Linear_Regression.predict_dc(tn, tncols)
        Relid, graph_data, ucl, lcl = Linear_Regression.graph_data(tn, tncols, predict_cols)
        Rel_Id, Actual, LastPrediction = Linear_Regression.last_prediction(tn, tn_lp, predict_cols)
        Algorithm_Name = 'Linear Regression'
    if (Algorithm_in == '2'):
        predicted_data = Tensor_Flow.predict_dc(tn, tncols)
        Relid, graph_data, ucl, lcl = Tensor_Flow.graph_data(tn, tncols, predict_cols, predicted_data)
        tn_lp1 = cfg['DE']['tn_lp1']
        Rel_Id, Actual, LastPrediction = Tensor_Flow.last_prediction(tn, tn_lp1, predict_cols)
        Algorithm_Name = 'Tensor Flow'
    
    rel_id = len(Relid)
    uclall = ucl[0]
    lclall = lcl[0]
    for n, i in enumerate(ucl):
        if i == (uclall):
            ucl[n] = ucl_in
    for n, i in enumerate(lcl):
        if i == (lclall):
            lcl[n] = lcl_in
    # Edit
    Relid_graph = []
    graph_data_graph = []
    ucl_graph = []
    lcl_graph = []
    accuracy = []
    length = len(Relid)
    last_predict = []
    i = length - 25
    j = 0
    k = 0
    for s in Relid:
        if (j >= i):
            Relid_graph.append(str(s))
        j = j + 1
    j = 0

    for s in graph_data:
        if (j >= i):
            if (j != (len(graph_data) - 1)):
                graph_data_graph.append(str(s))
        if (j < (len(graph_data) - (len(LastPrediction) + 1)) and j >= i):
            last_predict.append(str(s))
        elif (j >= (len(graph_data) - len(LastPrediction))):
            last_predict.append(str(LastPrediction[k]))
            k = k + 1
        j = j + 1
    j = 0
    for s in ucl:
        if (j >= i):
            ucl_graph.append(str(s))
        j = j + 1
    j = 0
    for s in lcl:
        if (j >= i):
            lcl_graph.append(str(s))
        j = j + 1
    last_predict.append(str(round(predicted_data[0], 2)))

    example = []
    for i in range(0, len(LastPrediction)):
        linear1 = LastPrediction[i]
        actual1 = Actual[i]
        if linear1>actual1:
        	a = ((actual1* 100)/linear1) 
        elif actual1>linear1:
                a = ((linear1* 100)/actual1) 
        else:a=100   
        accuracy.append(round(a, 2))
        example.append((Rel_Id[i], round(Actual[i],2), LastPrediction[i], round(a, 2)))
    
    predicted_data1 = predicted_data[0]

    print("graph data")
    print(len(graph_data_graph))
    print("last prediction")
    print(last_predict)
    print(len(last_predict))
    context = {
        "project_in": project_in,
        "Prediction_in": Module_in,
        "ucl_print": ucl_graph[0],
        "lcl_print": lcl_graph[0], 
        "Algorithm_Name":Algorithm_Name,

        "labels": Relid_graph,        
        "graph_data": graph_data_graph,
        "module": module,
        "ucl": ucl_graph,
        "lcl": lcl_graph,        
        "last_prediction": last_predict,

        "example": example,
        
        "predicted_data": round(predicted_data1, 2),
        "predicted_label": rel_id,
 
    }

    return render(request, cfg['urls']['use'], context)

@xframe_options_deny
@login_required(login_url='/ICanCode/login')
@user_passes_test(in_group_a, login_url='/ICanCode/denied')
def db(request):

    db_in = request.POST.get('db',False)

    if(db_in =='Digital Enablement'):
        db='digitalenablement'
        
    elif(db_in=='Personal Insurance') :
        db='personalinsurance'

    db_datamanagement_fetch_db_data.db(db)
    path= "/static/ICanCode/documents/Downloaded_Data/"+db+".xlsx"
    
    context = {
        "db_in" : db_in,
        "path": path,
               
        }
    return render(request,'Prediction/db.html', context)

@xframe_options_deny
@login_required(login_url='/ICanCode/login')
@user_passes_test(in_group_a, login_url='/ICanCode/denied')
def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        name='test-case.xlsm'
        file_name=fs.get_valid_name('test-case.xlsm')
        if(file_name==name):
            fs.delete(file_name)
        filename = fs.save('test-case.xlsm', myfile)
        uploaded_file_url = fs.url(filename)

    context = {
        'uploaded_file_url': uploaded_file_url,
        }
        
    return render(request, 'Prediction/dbupdate.html', context)


class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'Prediction/dbupdate.html'
    success_url = '#'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        basepath1=os.path.abspath('...').replace('\\','/')
        
        path= basepath1+'/ICanCode/media/Uploaded_Data'
        for filename in glob.glob(os.path.join(path, '*.xlsm')):
            if os.path.isfile(filename):
                os.unlink(filename)
        for filename in glob.glob(os.path.join(path, '*.xlsx')):
            if os.path.isfile(filename):
                os.unlink(filename)
        for filename in glob.glob(os.path.join(path, '*.csv')):
            if os.path.isfile(filename):
                os.unlink(filename)
        
        files = request.FILES.getlist('file_field')
        fs=FileSystemStorage()
        if form.is_valid():
            for f in files:
                filename=fs.save('Uploaded_Data/'+f.name,f)
                   
                if filename=="Uploaded_Data/digitalenablement.xlsx":
                    db='digitalenablement'
                    db_datamanagement_insert_db_data.db(db)
                elif filename=="Uploaded_Data/personalinsurance.xlsx":
                    db='personalinsurance'
                    db_datamanagement_insert_db_data.db(db)
                               
            return self.form_valid(form)
        
        else:
            return self.form_invalid(form)


