from django.conf.urls import url
from . import views
from .views import FileView

urlpatterns = [
    url(r'^resultdefect/$', views.resultdefect, name='resultdefect'),
    url(r'^upload/$', FileView.as_view(), name='resultdefect'),
    url(r'^defect/$', views.indexdefect,name='UsecaseA2_Dup_Defects'),
    url(r'^projectdefect/$', views.projectdefect,name='projectdefect'),
    url(r'^testcase/$', views.indextestcase, name='indextestcase'),
    url(r'^projecttestcase/$', views.projecttestcase, name='projecttestcase'),
    url(r'^resulttestcase/$', views.resulttestcase, name='resulttestcase'),
    url(r'^upload/$', FileView.as_view(), name='resulttestcase'),
    url(r'^submitdefect/$', views.submitdefect, name='submitdefect'),
    url(r'^submittestcase/$', views.submittestcase, name='submittestcase'),]

