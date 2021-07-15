from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^get_followup_by_search', views.get_followup_by_search),
    url(r'^update_followup_intention', views.update_followup_intention),



]