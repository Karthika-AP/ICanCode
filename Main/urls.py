from django.conf.urls import url
from . import views
from Prediction import views as pre

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^denied$', views.denied, name='denied'),
    
    url(r'^Prediction/$', pre.metrics, name='Prediction'),
    url(r'^result/$', pre.use,name="usecase_result"),
    url(r'^details/$', pre.details,name="details"),
]
