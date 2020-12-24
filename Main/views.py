from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.clickjacking import xframe_options_deny
import os
import yaml
from django.conf import settings

basepath=str(settings.BASE_DIR)

yamlpath = '/ICanCode/media/'
path = basepath + yamlpath
with open(path + 'Main.yml', 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)


@xframe_options_deny
@login_required(login_url=cfg['urls']['login'])
def index(request):
    return render(request, cfg['urls']['home'])

def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=cfg['UN'], password=cfg['PA'])
    print(user)
    if user is not None and user.is_active:
        auth.login(request, user)
        request.session.cycle_key()
        return HttpResponseRedirect(cfg['urls']['AI'])
    else:
        return HttpResponseRedirect("login")


def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect(cfg['urls']['login'])

@xframe_options_deny
@login_required(login_url=cfg['urls']['login'])
def denied(request):
    return render(request, cfg['urls']['denied'])
