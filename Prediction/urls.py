from django.conf.urls import url
from . import views
from .views import FileFieldView
urlpatterns = [
    url(r'^result/$', views.use, name="usecase_result"),  # Calls use method to predict and generate graph
    url(r'^details/$', views.details, name="details"),  # Calls details method to predict lcl, ucl
    url(r'^dbupdate/$',  FileFieldView.as_view(), name='simple_upload'),
    url(r'^db/$', views.db,name="db"),

    ]
