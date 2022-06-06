# !/user/bin/python3
# coding=utf-8
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'get_rtms_by_search',views.get_rtms_by_search),
    url(r'get_all_rtms_data', views. get_all_rtms_data),
    url(r'files_upload', views.files_upload, name='files_upload'),
    url(r'add_rtms_treatment', views.add_rtms_treatment),
    url(r'', views.get_all_rtms_data)
]
